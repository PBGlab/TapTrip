from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    """ 發送 Email 驗證信 """
    user.generate_verification_token()  # 產生 Token
    verification_url = f"http://127.0.0.1:8000/verify/{user.email_verification_token}" 
    
    subject = "TapTrip 旅遊一指通 - 帳號驗證"
    message = f"請點擊以下連結完成 Email 驗證：\n{verification_url}"
    html_message = f"""
    <p>請點擊以下連結完成 Email 驗證：</p>
    <p><a href="{verification_url}" style="color: #1a73e8; text-decoration: none;">點此驗證 Email</a></p>
    <p>如果無法點擊連結，請複製以下網址至瀏覽器：</p>
    <p>{verification_url}</p>
    """
    #正式上架才超連結才能有效使用
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
