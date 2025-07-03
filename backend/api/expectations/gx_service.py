from api.models import ExpectationSuite, ValidationResult, DataAsset
from typing import Dict, Any,List
from fastapi import HTTPException
import great_expectations as gx
from api.expectations.expectation import InExpectationSuite,ValidationResultBase
from api.utils.expectation_desc import generate_expectation_description
from datetime import timedelta, datetime
from great_expectations.validator.validator import Validator

async def get_expectation_by_dataassetId(data_asset_id: int) -> List[ExpectationSuite]:
    """
    @description: 根据数据资产ID获取所有关联的期望套件
    @param {int} data_asset_id: 数据资产的ID
    @returns {List[ExpectationSuite]}: 期望套件列表，如果数据资产不存在则返回空列表
    """
    # 检查数据资产是否存在
    data_asset = await DataAsset.get_or_none(id=data_asset_id)
    if not data_asset:
        return []
    # 获取与该数据资产关联的所有期望套件
    expectation_suites = await ExpectationSuite.filter(data_asset=data_asset).all()

    return expectation_suites
async def creat_expectation_suite(dataassetId: int, expecation: InExpectationSuite):
    """
    @description: 创建一个期望套件，并为每个期望生成中文描述，整体描述存入 description 字段
    @param {int} dataassetId: 数据资产ID
    @param {InExpectationSuite} expecation: 包含 suite_json 的 Pydantic 模型
    @returns {ExpectationSuite | None}: 创建的期望套件对象或 None
    """
    data_asset = await DataAsset.get_or_none(id=dataassetId)
    if not data_asset:
        return None

    # 提取期望列表

    expectations = expecation.suite_json.get("expectations", [])
    # 生成所有期望的描述
    descriptions = []
    for exp in expectations:
        try:
            desc = generate_expectation_description(exp)
            descriptions.append(desc)
        except ValueError as e:
            descriptions.append("未知期望描述")
    # 合并成一条总描述（可选）
    full_description = "；".join(descriptions) if descriptions else "无有效期望描述"
    # 创建并保存期望套件，description 单独传入
    suite = await ExpectationSuite.create(
        data_asset=data_asset,
        type_id=expecation.type_id,
        suite_json=expecation.suite_json,
        description=full_description
    )

    return suite
async def execute_validation(validator: Validator,expectation_suite: ExpectationSuite):
    try:
        expectations_list = expectation_suite.suite_json.get("expectations", [])
        for exp in expectations_list:
            expectation_type = exp.get("expectation_type")
            kwargs = exp.get("kwargs", {})
            if not hasattr(validator, expectation_type):
               raise ValueError(f"Unknown expectation type: {expectation_type}")
            expectation_func = getattr(validator, expectation_type)
            expectation_func(**kwargs)
            print(f"Applying expectation: {expectation_type} with kwargs: {kwargs}")
        # 执行验证
        results = validator.validate()
        return results.to_json_dict()
    except Exception as e:
        error_message = f"Error during Great Expectations validation: {str(e)}"
        print(error_message)
        if "connection" in str(e).lower():
            raise HTTPException(status_code=500, detail=f"数据库连接失败: {str(e)}")
        elif "table" in str(e).lower() or "relation" in str(e).lower():
            raise HTTPException(status_code=500, detail=f"表不存在或无法访问: {str(e)}")
        elif "syntax" in str(e).lower() or "sql" in str(e).lower():
            raise HTTPException(status_code=500, detail=f"SQL查询语法错误: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"验证失败: {str(e)}")
async def execute_all_validations_for_data_asset(data_asset_id: int):

    data_asset = await DataAsset.get_or_none(id=data_asset_id).prefetch_related('datasource')
    datasource=data_asset.datasource
    expectation_suites = await ExpectationSuite.filter(data_asset=data_asset).all()
    if not expectation_suites:
        return {"message": f"No expectation suites found for DataAsset with id {data_asset_id}", "results": []}
    all_results = []
    context = gx.get_context()
    data_source = context.data_sources.add_postgres( name=f"datasource_{data_asset.id}", connection_string=datasource.url)
    table_asset = data_source.add_table_asset(table_name=data_asset.name, name=f"data_asset_{data_asset.id}")
    batch_request = table_asset.build_batch_request()
    try:
        for suite in expectation_suites:
            validator = context.get_validator(
                batch_request=batch_request,
                create_expectation_suite_with_name=f"suite_{suite.id}"
            )
            result_json = await execute_validation(validator,suite)
            result_json["description"] = suite.description
            success = result_json.get("success", False)
            result = await save_validation_result(
                expectation_suite_id=suite.id,
                data_asset_id=data_asset_id,
                success=success,
                result_json=result_json
            )

            all_results.append( ValidationResultBase(
                                     id=result.id,
                                     expectation_suite_id=suite.id,
                                     success=success,
                                     validation_time=result.validation_time))
    except HTTPException as e:
            all_results.append({
                "dataasset": data_asset_id,
                "success": False,
                "error": str(e.detail)
            })
    return all_results
async def save_validation_result(expectation_suite_id: int, data_asset_id: int, success: bool,
                             result_json: Dict[str, Any]):
    """
    @description: 保存新的验证结果记录，而不是更新已有记录
    @param {int} expectation_suite_id: 期望套件ID
    @param {int} data_asset_id: 数据资产ID
    @param {bool} success: 验证是否成功
    @param {Dict[str, Any]} result_json: 验证结果的原始JSON数据
    @returns {ValidationResult | None}: 创建的验证结果对象或 None
    """
    expectation_suite = await ExpectationSuite.get_or_none(id=expectation_suite_id)
    data_asset = await DataAsset.get_or_none(id=data_asset_id)
    if not data_asset or not expectation_suite:
        return None

    # 总是创建新记录
    result = await ValidationResult.create(
        expectation_suite=expectation_suite,
        data_asset=data_asset,
        success=success,
        result_json=result_json
    )
    
    return result


async def get_latest_validation_result(expectation_suites: List[ExpectationSuite]) -> List[ValidationResult]:
    """
    @description: 获取指定期望套件列表中每个套件的最新验证结果
    @param {List[ExpectationSuite]} expectation_suites: 期望套件对象列表
    @returns {List[ValidationResult]}: 每个期望套件对应的最新验证结果列表，如果某个套件没有验证结果则不包含在返回列表中
    """
    if not expectation_suites:
        return []
    # 提取期望套件ID列表
    suite_ids = [suite.id for suite in expectation_suites]
    # 为每个期望套件查询其最新的验证结果
    latest_results = []
    for suite_id in suite_ids:
        # 查询该期望套件的最新验证结果（按验证时间降序排列，取第一个）
        latest_result = await ValidationResult.filter(
            expectation_suite_id=suite_id
        ).order_by('-validation_time').first()
        
        if latest_result:
            latest_results.append(latest_result)
    
    return latest_results

async def get_all_validation_results(assetId: int)-> List[ValidationResult]:
    """
    @description: 获取指定数据资产 (data_asset_id) 的所有验证结果记录
    @param {int} assetId: 数据资产ID
    @returns {List[ValidationResultBase]}: 所有与该数据资产关联的验证结果列表
    """
    fifteen_days_ago = datetime.utcnow() - timedelta(days=15)
    validate_results = await ValidationResult.filter(
        data_asset_id=assetId,
        validation_time__gte=fifteen_days_ago
    ).limit(200)
    if not validate_results:
        return []
    return validate_results










