EXPECTATION_DESCRIPTION_TEMPLATES = {
    # 101 Column to exist
    "expect_column_to_exist": "期望列 {column} 存在于表中",
    # 102 Values to be in type list
    "expect_column_values_to_be_in_type_list": "期望 {column} 列的值类型必须属于此集合：{type_list}，且至少 {mostly} 的情况下需满足该要求。",
    # 103 Column values to be of type
    "expect_column_values_to_be_of_type": "期望 {column} 列的值为类型 {type_}，且至少 {mostly} 的情况下需满足该要求。",
    # 104 Table column count to be between
    "expect_table_column_count_to_be_between": "期望表的列数在 {min_value} 和 {max_value} 之间",
    # 105 Table column count to equal
    "expect_table_column_count_to_equal": "期望表的列数等于 {value}",
    # 106 Table columns to match ordered list
    "expect_table_columns_to_match_ordered_list": "期望表的列与有序列表 {column_list} 完全匹配",
    # 107 Table columns to match set
    "expect_table_columns_to_match_set": "期望表的列与集合 {column_set} 匹配",
    # 201 Table row count to be between
    "expect_table_row_count_to_be_between": "期望表的行数在 {min_value} 和 {max_value} 之间",
    # 202 Table row count to equal
    "expect_table_row_count_to_equal": "期望表的行数等于 {value}",
    # 203 Table row count to equal other table
    "expect_table_row_count_to_equal_other_table": "期望表的行数等于其他表 {other_table_name} 的行数",
    # 301 Column values to not be null
    "expect_column_values_to_not_be_null": "期望 {column} 列的值不为空，且至少 {mostly} 的情况下需满足该要求。",
    # 302 Column values to be null
    "expect_column_values_to_be_null": "期望 {column} 列的值为空，且至少 {mostly} 的情况下需满足该要求。",
    # 401 Column values to be unique
    "expect_column_values_to_be_unique": "期望 {column} 列的值是唯一的，且至少 {mostly} 的情况下需满足该要求。",
    # 402 Column distinct values to be in set
    "expect_column_distinct_values_to_be_in_set": "期望 {column} 列的不同值在集合 {value_set} 中",
    # 403 Column distinct values to contain set
    "expect_column_distinct_values_to_contain_set": "期望 {column} 列的不同值包含集合 {value_set}",
    # 405 Column distinct values to equal set
    "expect_column_distinct_values_to_equal_set": "期望 {column} 列的不同值等于集合 {value_set}",
    # 406 Column proportion of unique values to be between
    "expect_column_proportion_of_unique_values_to_be_between": "期望 {column} 列中唯一值的比例在 {min_value} 和 {max_value} 之间(严格大于：{strict_max}，严格小于：{strict_min})",

    # 407 Column unique value count to be between
    "expect_column_unique_value_count_to_be_between": "期望 {column} 列中唯一值的数量在 {min_value} 和 {max_value} 之间",

    # 408 Compound columns to be unique
    "expect_compound_columns_to_be_unique": "期望列组合 {column_list} 的值是唯一的",

    # 409 Select column values to be unique within record
    "expect_select_column_values_to_be_unique_within_record": "期望列 {column_list} 在记录内唯一",

    # 501 Column values to be between
    "expect_column_values_to_be_between": "期望 {column} 列的值在 {min_value} 和 {max_value} 之间(严格大于：{strict_max}，严格小于：{strict_min})，且至少 {mostly} 的情况下需满足该要求。",

    # 502 Column maximum to be between
    "expect_column_max_to_be_between": "期望 {column} 列的最大值在 {min_value} 和 {max_value} 之间",

    # 503 Column mean to be between
    "expect_column_mean_to_be_between": "期望 {column} 列的平均值在 {min_value} 和 {max_value} 之间",

    # 504 Column median to be between
    "expect_column_median_to_be_between": "期望 {column} 列的中位数在 {min_value} 和 {max_value} 之间",

    # 505 Column minimum to be between
    "expect_column_min_to_be_between": "期望 {column} 列的最小值在 {min_value} 和 {max_value} 之间",

    # 506 Column pair values a to be greater than b
    "expect_column_pair_values_a_to_be_greater_than_b": "期望列 {column_A} 的值大于列 {column_B}",

    # 507 Column standard deviation to be between
    "expect_column_stdev_to_be_between": "期望 {column} 列的标准差在 {min_value} 和 {max_value} 之间",

    # 508 Column sum to be between
    "expect_column_sum_to_be_between": "期望 {column} 列的总和在 {min_value} 和 {max_value} 之间",

    # 509 Column value z-scores to be less than
    "expect_column_zscore_to_be_less_than": "期望 {column} 列值的 Z 分数小于 {threshold}",

    # 510 Multicolumn sum to equal
    "expect_multicolumn_sum_to_equal": "期望列 {column_list} 的总和等于 {value}",

    # 601 Column values to be in set
    "expect_column_values_to_be_in_set": "期望 {column} 列的值在集合 {value_set} 中，且至少 {mostly} 的情况下需满足该要求。",

    # 602 Column most common value to be in set
    "expect_column_most_common_value_to_be_in_set": "期望{column}列最常见的值在集合{value_set}中",

    # 603 Column pair values to be equal
    "expect_column_pair_values_to_be_equal": "期望列 {column_A} 和 {column_B} 的值相等，且至少 {mostly} 的情况下需满足该要求。",

    # 604 Column value lengths to be between
    "expect_column_value_lengths_to_be_between": "期望 {column} 列值长度在 {min_value} 和 {max_value} 之间，且至少 {mostly} 的情况下需满足该要求。",

    # 605 Column value lengths to equal
    "expect_column_value_lengths_to_equal": "期望{column}列值长度等于{value}，且至少 {mostly} 的情况下需满足该要求。",

    # 606 Column values to match like pattern
    "expect_column_values_to_match_like_pattern": "期望 {column} 列值匹配类似模式 {like_pattern}，且至少 {mostly} 的情况下需满足该要求。",

    # 607 Column values to match like pattern list
    "expect_column_values_to_match_like_pattern_list": "期望 {column} 列值匹配多个类似模式 {like_pattern_list}，且至少 {mostly} 的情况下需满足该要求。",

    # 608 Column values to match regex
    "expect_column_values_to_match_regex": "期望 {column} 列值匹配正则表达式 {regex}，且至少 {mostly} 的情况下需满足该要求。",

    # 609 Column values to match regex list
    "expect_column_values_to_match_regex_list": "期望 {column} 列值匹配多个正则表达式 {regex_list}，且至少 {mostly} 的情况下需满足该要求。",

    # 610 Column values to not be in set
    "expect_column_values_to_not_be_in_set": "期望 {column} 列的值不在集合 {value_set} 中，且至少 {mostly} 的情况下需满足该要求。",

    # 611 Column values to not match like pattern
    "expect_column_values_to_not_match_like_pattern": "期望 {column} 列值不匹配模式 {like_pattern}，且至少 {mostly} 的情况下需满足该要求。",

    # 612 Column values to not match like pattern list
    "expect_column_values_to_not_match_like_pattern_list": "期望 {column} 列值不匹配任何模式 {like_pattern_list}，且至少 {mostly} 的情况下需满足该要求。",

    # 613 Column values to not match regex
    "expect_column_values_to_not_match_regex": "期望 {column} 列值不匹配正则表达式 {regex}，且至少 {mostly} 的情况下需满足该要求。",

    # 614 Column values to not match regex list
    "expect_column_values_to_not_match_regex_list": "期望 {column} 列值不匹配任何正则表达式 {regex_list}，且至少 {mostly} 的情况下需满足该要求。",




    # 可继续添加更多期望类型...
}


def generate_expectation_description(expectation: dict) -> str:
    """
    根据 expectation 字典生成对应中文描述。
    :param expectation: 示例格式：
        {
            "expectation_type": "expect_column_values_to_be_unique",
            "kwargs": {"column": "vendor_id"}
        }
    :return: 描述字符串
    """
    expectation_type = expectation.get("expectation_type")
    kwargs = expectation.get("kwargs", {})

    if "mostly" in kwargs:
        mostly_percent = f"{int(kwargs['mostly'] * 100)}%"
        kwargs = kwargs.copy()
        kwargs["mostly"] = mostly_percent

    template = EXPECTATION_DESCRIPTION_TEMPLATES.get(expectation_type)
    if not template:
        raise ValueError(f"未知的期望类型: {expectation_type}")

    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"缺少必要参数用于生成描述: {e}")

