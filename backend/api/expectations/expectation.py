from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Dict, Any
from datetime import datetime
class InExpectationSuite(BaseModel):
    id: int = None
    suite_json: Dict[str, Any]=[]
    type_id:int =0
    description: str = None
    model_config = ConfigDict(from_attributes=True)

class ValidationResultBase(BaseModel):
    id: int
    expectation_suite_id: int
    success: bool
    validation_time: datetime
    model_config = ConfigDict(from_attributes=True)

class ValidationResultDetail(ValidationResultBase):
    result_json: Dict[str, Any]
    data_asset_id: int
    @field_serializer('result_json')
    def serialize_result_json(self, result_json: Dict[str, Any], _info):
        cleaned_result = result_json.copy()
        cleaned_result.pop("meta", None)
        return cleaned_result