"""Module for marshmallow schemas."""
from marshmallow import Schema, fields


class ParamsSchema(Schema):
    Amount = fields.Integer(required=True)
    IpAddress = fields.String(required=True)
    CardCryptogramPacket = fields.String(required=True)
