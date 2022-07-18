# Cloudpayments client

## Basic information

***Cloudpayments client*** allows you to make payment by data cryptogram result of the encryption algorithm for single stage and two-stage payment.
***This project solves:***
1. Request authentication
2. The architecture allows you to add other API methods


## Starting

| Environmental         | Description                  |
|-----------------------|------------------------------|
| `API_SECRET`          | login in personal account    |
| `PUBLIC_ID`           | password in personal account |

1. clone the repository:
```bash
https://github.com/Hyper-glitch/cloudpayments.git
```
2. Create **.env** file and set the <ins>environmental variables</ins> as described above.
3. Create venv
```bash
python3 -m venv venv
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Run python script
```bash
python3 main.py
```