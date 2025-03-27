from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from accounts.models import CustomUser
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        errors = {}

        # 檢查帳號是否存在
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            errors['email'] = '帳號不存在,請先註冊！'
        elif not user.is_email_verified:
            errors['email'] = 'Email 未驗證,請前往信箱完成 Email 驗證！'
        else:
            # 驗證帳號密碼
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                errors['password'] = '密碼錯誤,請重新輸入！'

        if errors:
            return JsonResponse({"success": False, "errors": errors}, status=400)
    
        # ✅ 登入成功
        login(request, user)
        next_url = request.POST.get('next') or request.GET.get('next') or '/home'
        return JsonResponse({"success": True, "redirect_url": next_url, "username": user.username})

    # ✅ GET 請求時回傳 login.html
    return render(request, 'login.html')

#更改密碼功能
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render

@login_required
def updatepassword(request):
    if request.method == 'POST':
        currentpassword = request.POST.get('currentpassword')
        newpassword = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        errors = {}

        # 驗證舊密碼
        if not check_password(currentpassword, user.password):
            errors['currentpassword'] = "舊密碼不正確"

        # 確保新密碼與確認密碼相同
        if newpassword != confirm_password:
            errors['confirm_password'] = "新密碼與確認密碼不一致"

        # 如果有錯誤，回傳 JSON 給前端
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # 更新密碼
        user.set_password(newpassword)
        user.save()

        # **強制登出使用者**
        logout(request)

        return JsonResponse({'success': True, 'redirect_url': '/login/'})  # 成功後導向登入頁面

    return render(request, 'updatepassword.html')

#傳遞username
def user_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"is_authenticated": True, "username": request.user.username})
    return JsonResponse({"is_authenticated": False})



from .utils import send_verification_email
@csrf_exempt  # 開發測試用，正式環境請移除
def register_view(request):
    """註冊 API，發送 Email 驗證"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        # 檢查使用者名稱格式（僅允許英數及底線）
        if not re.match(r"^[\u4e00-\u9fffa-zA-Z0-9]+$", username):
            errors['username'] = '使用者名稱只能使用中文、英文字母或數字，不得使用底線、空白或特殊符號！'

        # 檢查 Email 是否已存在
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = '該 Email 已被註冊！'

        # 檢查密碼是否一致
        if password != confirm_password:
            errors['password'] = '密碼不一致,請重新輸入！'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # 創建帳號（預設未啟用）
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False  # 完成 Email 驗證後才啟用
        )

        # 發送 Email 驗證信
        send_verification_email(user)

        # 成功註冊後，回傳 JSON 並告知前端進行頁面跳轉，同時帶上 email
        redirect_url = "/email_verification_notice/?email=" + email
        return JsonResponse({
            "success": True,
            "message": "請檢查您的 Email, 完成驗證。",
            "redirect_url": redirect_url
        })
        # return render(request, 'email_verification_notice.html', {'email': email})
    return render(request, 'register.html')



from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
@login_required  # ✅ 只有登入的使用者能登出
def logout_view(request):
    """ 顯示登出確認頁面 """
    return render(request, 'logout.html')  # 先顯示登出確認頁面

@require_POST  # ✅ 限制只接受 POST 請求
@login_required  # ✅ 只有登入的使用者能登出
def logout_confirm(request):
    """ 真正執行登出 """
    logout(request)
    return JsonResponse({"success": True, "redirect_url": "/"})  # 讓前端 AJAX 接收 JSON 回應


# Email 驗證提醒
def email_verification_notice_view(request):
    email = request.GET.get('email', '')
    return render(request, 'email_verification_notice.html', {'email': email})

# Email 驗證成功
def verify_email(request, token):
    """ 驗證 Email API，回傳 HTML 頁面 """
    user = CustomUser.objects.get(email_verification_token=token)
    user.is_active = True  # ✅ 啟用帳號
    user.is_email_verified = True
    user.email_verification_token = ""  # 清除 Token
    user.save()
    return render(request, "email_verification_success.html")  # 成功頁面

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 如果是前端 AJAX 可加上這個（開發用）
from django.contrib import messages

@csrf_exempt
def reset_password(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
    except CustomUser.DoesNotExist:
        messages.error(request, '連結無效或已過期，請重新請求找回密碼。')
        return redirect('login')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        errors = {}

        if not password or not confirm:
            errors['password'] = '密碼欄位不得為空'
        elif password != confirm:
            errors['confirm_password'] = '兩次密碼輸入不一致'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        user.set_password(password)
        user.email_verification_token = None
        user.save()

        return JsonResponse({'success': True, 'message': '密碼已成功更新', 'redirect_url': '/login/'})

    return render(request, 'reset_password.html', {'token': token})



from .utils import send_reset_password_email

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return JsonResponse({'success': False, 'message': '此 Email 未註冊'}, status=400)

        send_reset_password_email(user)
        return JsonResponse({'success': True, 'message': '密碼重設連結已寄出，請查看您的信箱！', 'redirect_url': '/login/'})

    return render(request, 'forgot_password.html')

