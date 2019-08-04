from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth.models import User
from chat.models import register_form, users
from utiles.check_code import create_validate_code
from io import BytesIO


# Create your views here.

def acc_login(request):
    error_msg = ' '
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        qs = users.objects.filter(username=username, password=password)
        print("lalalal")
        if qs.exists():
            request.session['is_login'] = True
            request.session["username"] = username
            request.session.set_expiry(6 * 60 * 60)
            # 验证通过
            return redirect('/index/', {"username": username})
        else:
            error_msg = "用户名或密码错误"
        return render(request, "login.html", {"error_msg": error_msg})


def acc_register(request):
    '''注册'''
    if request.method == "GET":
        obj = register_form()
        return render(request, "register.html", {"obj": obj})
    elif request.method == "POST":
        obj = register_form(request.POST)
        check = request.POST.get("check", None)
        check_code = request.session["check_code"]
        if obj.is_valid() and check == check_code:
            data = obj.clean()
            try:
                users.objects.create(**data)
                return redirect("/login/")
            except Exception as e:
                number_error = "该昵称已存在"
                return render(request, "register.html", {"obj": obj})
        else:
            code_error = "验证码输入错误"
            return render(request, "register.html", {"obj": obj, "code_error": code_error})


def yanzhengma(request):
    '''生成验证码'''
    f = BytesIO()  # 创建生成一个内存地址
    img, code = create_validate_code()  # 生成验证码， code是验证码文字内容，img是验证码对象
    print(code)
    img.save(f, "PNG")  # 把验证码写入内存地址
    request.session["check_code"] = code  # 对应验证用的
    return HttpResponse(f.getvalue())  # 把验证码从内存中读出来并返回给客户端


def index(request):
    print('kakakakakak')
    try:
        res = request.session['is_login']
        username = request.session["username"]
        if res:
            print("us")
            return render(request, 'index.html', {"username": username})
        else:
            return redirect('/login/')
    except:
        print("login")
        return redirect('/login/')
