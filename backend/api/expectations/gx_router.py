from fastapi import APIRouter, HTTPException
from typing import List
from api.expectations.gx_service import creat_expectation_suite, execute_all_validations_for_data_asset, get_expectation_by_dataassetId, get_latest_validation_result,get_all_validation_results
from api.expectations.expectation import InExpectationSuite,ValidationResultBase,ValidationResultDetail

gx_router = APIRouter()

#获取某数据集的全部期望
@gx_router.get("/dataasset/{dataAssetId}/expectation",response_model=List[InExpectationSuite])
async def get_expectation(dataAssetId: int):
    suites =await get_expectation_by_dataassetId(dataAssetId)
    if not suites:
        return []
    return suites
#增加期望
@gx_router.post("/dataasset/{dataAssetId}/expectation")
async def create(dataAssetId: int, inExpecationSuite:InExpectationSuite):
    suite = await creat_expectation_suite(dataAssetId, inExpecationSuite)
    if not suite:
        raise HTTPException(status_code=404, detail=f"DataAsset with id {dataAssetId} not found.")
    return {"message": "Expectation Suite saved successfully", "suite_id": suite.id}
#执行验证
@gx_router.post("/dataasset/{dataAssetId}/validate")
async def validate_data(dataAssetId: int):
    validateresult = await execute_all_validations_for_data_asset(dataAssetId)
    return validateresult

#获取最新的简略的验证结果
@gx_router.get("/dataasset/{dataAssetId}/validate", response_model=List[ValidationResultBase])
async def validate_data(dataAssetId: int):
    expectationsuites = await get_expectation_by_dataassetId(dataAssetId)
    validateresult = await get_latest_validation_result(expectationsuites)
    return validateresult

@gx_router.get("/dataasset/{dataAssetId}/detail_validate", response_model=List[ValidationResultDetail])
async def validate_data(dataAssetId: int):
    validateresult = await get_all_validation_results(dataAssetId)
    return validateresult

