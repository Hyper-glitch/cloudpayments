"""Module for marshmallow schemas."""
from marshmallow import Schema, fields, validate


class ParamsSchema(Schema):
    Amount = fields.Integer(required=True)
    IpAddress = fields.String(required=True)
    CardCryptogramPacket = fields.String(required=True)


class SuccessfulResponseSchema(Schema):
    Model = fields.Dict()
    Success = fields.Boolean(validate=validate.Equal(True))
    Message = fields.String(missing=None)
