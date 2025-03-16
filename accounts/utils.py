import requests
from django.conf import settings

def send_verification_email(user):
    """ 使用 Brevo API 發送 Email 驗證信 """
    user.generate_verification_token()  # 產生驗證 Token
    verification_url = f"http://127.0.0.1:8000/verify/{user.email_verification_token}"

    api_url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,  # 需要在 settings.py 或 .env 設置 BREVO_API_KEY
        "content-type": "application/json"
    }
    data = {
        "sender": {"name": "TapTrip", "email": settings.DEFAULT_FROM_EMAIL},
        "to": [{"email": user.email, "name": user.username}],
        "subject": "TapTrip 旅遊一指通 - 帳號驗證",
        "htmlContent": f"""
            <p>請點擊以下連結完成 Email 驗證：</p>
            <p><a href="{verification_url}" style="color: #1a73e8; text-decoration: none;">點此驗證 Email</a></p>
            <p>如果無法點擊連結，請複製以下網址至瀏覽器：</p>
            <p>{verification_url}</p>
        """
    }
    response = requests.post(api_url, json=data, headers=headers)

    return response.status_code == 201  # 201 表示成功發送
