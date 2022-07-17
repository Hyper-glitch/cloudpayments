"""The main module for running CloudPayments client"""
import aiohttp
from environs import Env
import uuid
from cloudpayments_client import CloudPaymentsClient


def run_cloudpayments_client():
    env = Env()
    env.read_env()

    public_id = env.str('PUBLIC_ID')
    api_secret = env.str('API_SECRET')

    example_yandex_pay_token = "\"{\\\"type\\\":\\\"Yandex\\\",\\\"signedMessage\\\":\\\"{\\\\\\\"encryptedMessage\\\\\\\":\\\\\\\"xqpAiS2L71BZNgH514AQDwOVawJF4gHXF8P+ECIFRqFHlDMRtxHsO9hNQSeegSssRdDMlBIyOObY5dqI3iwX99UKYP6qFD+tKEYJQkUdiKyhZCwgUsVdHBlFQA+iiXVLf7DZ5WCIaHjpl4mckrGeDg4XGDIX4FB0BorLqocbDLcl0JZi2zzkNtn9FDLPSAs1qbTEMdb3TAS0iDAIkuAy5DGJ3+4Av9PWvIllW4LRdQ34rR8MPszJxq9Xagw/jeKUglyUERQgi5cnVWIB992yPh9UFgNuCQBc+JWLMzuOIKKxFiVK6VBSsuHpDWrSZqMolN6PIeNvETxQ34g+O/u4KiwWd3IG/pb5e0FYbzn/gWzlDSPsqNSuB713qZDHCI7eFB7h7iPTdk/Wd78Vv7Vlg4oVQdMWCbgSjtWDamKeq/OMiVDW5j36CebRQWxB8/XFj4nAInHIjoUUKsEQ5gf00n9/48RUNVCbRr6qykvsfnD0XP5V4OJOeIhAZN2CAgGxgrGC5MibfjAf+D/EnunHwOvtmI6KQAsGv9QgrRC8sxTeyk7OT9vUCzK2DIRDYyCtvloGalRq1PRdJWQX\\\\\\\",\\\\\\\"tag\\\\\\\":\\\\\\\"LTx6/HA9iWaZwbYaFN1j9aDOPp2PBlR2iBMUBQ7zyUg=\\\\\\\",\\\\\\\"ephemeralPublicKey\\\\\\\":\\\\\\\"BHHBcT4SvFgxMK14Oz3/dk/uiCL2m4jeTFDEcoYHXt5gAz2wFVEnvRD4fHArkbIOcry9nlUYHWgT4GicEl9qkXY=\\\\\\\"}\\\",\\\"protocolVersion\\\":\\\"ECv2\\\",\\\"signature\\\":\\\"MEUCICyyzWnCEf2iHlUszDzvbAx/qk/sLmbTaOWPVEq1hr29AiEA0lfZ85pCofYhxVX971Xtshysawi7+KEe8ZpPVlV/Md4=\\\",\\\"intermediateSigningKey\\\":{\\\"signedKey\\\":\\\"{\\\\\\\"keyValue\\\\\\\":\\\\\\\"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEqYNePt6BPgCv5JxfO9dF2vrSqmnp4Mhe/vF+XO+Devbs6/KVpVVoTD8LLcAo4TZh6IuODVnVpHrTObhg3HJVJA==\\\\\\\",\\\\\\\"keyExpiration\\\\\\\":\\\\\\\"1764950892000\\\\\\\"}\\\",\\\"signatures\\\":[\\\"MEQCIDRslMW7wNZbpqVw/dD7hDQh30hGhqfjfWTBvc7zAYJSAiAGAvjAslA2AxwdAEuOfacFr6DaE5yiiUuUtM6DUreZYg==\\\"]}}\""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Request-ID': str(uuid.uuid4()),
    }
    auth = aiohttp.BasicAuth(login=public_id, password=api_secret, encoding='utf-8')
    params = {
        'Amount': 100,
        'IpAddress': '123.123.123.123',
        'CardCryptogramPacket': example_yandex_pay_token,
    }

    cloudpayments_client = CloudPaymentsClient()
    cloudpayments_client.charge(auth=auth, headers=headers, params=params, one_stage_payment=True)


if __name__ == '__main__':
    run_cloudpayments_client()
