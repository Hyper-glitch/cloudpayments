"""Module for marshmallow schemas."""
from marshmallow import Schema, fields, validate


class ParamsSchema(Schema):
    """Schema for serializing params."""
    Amount = fields.Integer(required=True)
    IpAddress = fields.String(required=True)
    CardCryptogramPacket = fields.String(required=True)


class SuccessfulResponseSchema(Schema):
    """Schema for deserializing and validation response if its successful."""
    Model = fields.Dict()
    Success = fields.Boolean(validate=validate.Equal(True))
    Message = fields.String(missing=None)
