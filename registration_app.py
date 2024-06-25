import requests

def generate_partner_token(client_id, client_secret):
    url = "https://auth.tesla.com/oauth2/v3/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://fleet-api.prd.eu.vn.cloud.tesla.com",
        "scope": "vehicle_device_data"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

# Введите ваши данные
client_id = "01ac7c94-d83e-4d60-a540-351a5b49f040"
client_secret = "ta-secret.jMp-c@F0yis$4kEw"

# Получение токена
access_token = generate_partner_token(client_id, client_secret)
print("Generated access token:", type(access_token), access_token)



url = "https://fleet-api.prd.eu.vn.cloud.tesla.com/api/1/partner_accounts"

payload = "{\n    \"domain\":\"localhost:8000\"}"
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {access_token}'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)