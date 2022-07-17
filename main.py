import aiohttp
from environs import Env

from cloudpayments_client import CloudPaymentsClient


def run_cloudpayments_client():
    env = Env()
    env.read_env()

    public_id = env.str('PUBLIC_ID')
    api_secret = env.str('API_SECRET')

    payment_data_cryptogram = '014242424242250102X6424dZ5oVeTMY5j5sA4Z1LrRz9uvjS4W7FJghHVbLSGta4GDB4lvyP0YG7HhcWQDe' \
                              'DAxoSQG9HxBbmCObxGjb0PYGy0r22/+gPRCOnpSYkaCI/tMr3TnCUA1PrcSLIHBUTk5AIOyzW4TT2L+cP1Fx' \
                              'nOaJ2Hpy3LpjjMYVOKt0pPthT1ol/2esAdknuYbh3Pz1Ga5Fo86KQ18WsFvMbM+5XSKU5r5eiDmU7njK8RI5' \
                              'Sxvput8PgRYOdFUl1uORPyKhbqz/obJyhlpy8/wS2qZiyyXp0zNmHzGLb/LYZVZhs1Ay1f3iKrRRc3uK6t4x' \
                              '5s7zYn0mAm0DsEr/iNh7AXuQ=='

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    auth = aiohttp.BasicAuth(login=public_id, password=api_secret, encoding='utf-8')
    params = {
        'Amount': 100,
        'IpAddress': '123.123.123.123',
        'CardCryptogramPacket': payment_data_cryptogram,
    }

    cloudpayments_client = CloudPaymentsClient()
    cloudpayments_client.charge(auth=auth, headers=headers, params=params, one_stage_payment=True)


if __name__ == '__main__':
    run_cloudpayments_client()
