def apply_expectations_to_validator(validator, expectations_list, ignore_unknown=False):
    for exp in expectations_list:
        expectation_type = exp.get("expectation_type")
        kwargs = exp.get("kwargs", {})

        if not hasattr(validator, expectation_type):
            if ignore_unknown:
                continue
            else:
                raise ValueError(f"Unknown expectation type: {expectation_type}")

        expectation_func = getattr(validator, expectation_type)
        expectation_func(**kwargs)