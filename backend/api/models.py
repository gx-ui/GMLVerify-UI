from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True,auto_increment=True)
    username = fields.CharField(max_length=16)
    password = fields.CharField(max_length=16)
    datasources: fields.ReverseRelation["DataSource"]
class DataSource(Model):
    id = fields.IntField(pk=True,auto_increment=True)
    name = fields.CharField(max_length=16)
    user = fields.ForeignKeyField("models.User",related_name="datasources")
    url = fields.CharField(max_length=255)
    class Meta:
        unique_together = (("name", "user"),)

    dataassets: fields.ReverseRelation["DataAsset"]
class DataAsset(Model):
    id=fields.IntField(pk=True,auto_increment=True)
    name = fields.CharField(max_length=64, null=True)
    datasource = fields.ForeignKeyField("models.DataSource",related_name="dataassets")
    class Meta:
        unique_together = (("name", "datasource"),)

class ExpectationSuite(Model):
    id=fields.IntField(pk=True,auto_increment=True)
    type_id= fields.IntField()
    suite_json = fields.JSONField()
    description = fields.CharField(max_length=255)
    data_asset: fields.ForeignKeyRelation['DataAsset'] = fields.ForeignKeyField('models.DataAsset', related_name='expectation_suites')
    class Meta:
        table = "expectationsuite"

class ValidationResult(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    validation_time = fields.DatetimeField(auto_now_add=True)
    success = fields.BooleanField()
    result_json = fields.JSONField()
    expectation_suite: fields.ForeignKeyRelation['ExpectationSuite'] = fields.ForeignKeyField('models.ExpectationSuite', related_name='validation_results')
    data_asset: fields.ForeignKeyRelation['DataAsset'] = fields.ForeignKeyField('models.DataAsset', related_name='validation_results')

    class Meta:
        table = "validationresult"