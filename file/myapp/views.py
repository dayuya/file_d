from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from myapp.models import File
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from django.http import FileResponse
from django_redis import get_redis_connection
import pickle
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from myapp.Result import Result
from myapp.ErrorCode import ErrorCode
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO 
import string
import uuid
redis_conn = get_redis_connection("default")

# Create your views here.
def view_files(request):
    # 创建（新增）一个新的 File 实例
    new_file = File.objects.create(
        file_id=str(uuid.uuid4()).replace('-', ''),
        user_id=123,            # 随机用户ID，例如，123
        file_type=1,            # 文件类型
        file_name='example.txt',# 文件名
        status=1,               # 状态
        file_url='example.com', # 文件URL
    )

    # 打印新创建的 File 对象的 ID
    print(new_file.file_id)
    return HttpResponse("1")

def test(request):
    if not request.user.is_authenticated:
        return Result.fail(ErrorCode.NO_LOGIN.code,ErrorCode.NO_LOGIN.msg)
    return Result.success("666")

def login(request):

    username = request.POST.get("username")
    password = request.POST.get("password")
    auth_obj = auth.authenticate(username=username, password=password)
    user_data = {
    'username': auth_obj.username,
    'user_id': auth_obj.id,
    'first_name': auth_obj.first_name,#用户的名字
    'last_name': auth_obj.last_name,#用户的姓氏
    # 添加其他必要的关键信息
    }
    if not auth_obj:
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,ErrorCode.ACCOUNT_EXIST.msg)
    # 设置有效期，例如设定为 1 小时
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    # 构建 payload 数据
    payload = {
        'user_id':auth_obj.id,
        'exp': expiration_time
    }
    # 使用 secret key 生成 JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    redis_conn.setex("TOKEN_"+token, 60*60*24,pickle.dumps(user_data))  # 键 "my_key" 将在 60*60*24 秒后过期
    return Result.success(token)
def currentUser(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not checkToken(token):
        return Result.fail(ErrorCode.NO_LOGIN.code,ErrorCode.NO_LOGIN.msg)
    userJson = redis_conn.get("TOKEN_" + token)  # 根据 token 获取用户信息
    if not userJson:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    aa=pickle.loads(userJson)
    return Result.success(aa)

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 使用 username 属性进行用户查询
    try:
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            return Result.fail(ErrorCode.REGISTRATION_FAILED.code,"用户存在")
        User.objects.create_user(username=username, password=password)
        return Result.success(True)
    except Exception as e:
        return Result.fail(ErrorCode.REGISTRATION_FAILED.code, ErrorCode.REGISTRATION_FAILED.msg)
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # 确保 upload 文件夹存在
        upload_folder = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(upload_folder, exist_ok=True)
        # 构造文件的保存路径
        file_path = os.path.join(upload_folder, uploaded_file.name)
        # 保存文件到指定路径
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': '文件上传成功'})
    return JsonResponse({'error': '请求方法错误或没有选择文件'}, status=400)
def download_file(request, filename):
    # 确定文件的保存路径
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        # 打开文件并返回给客户端进行下载
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return Result.fail(404,'文件不存在')
    
def checkToken(token):
    try:
        # 解码 JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # 验证有效期
        expiration_time = datetime.fromtimestamp(payload['exp'])
        current_time = datetime.utcnow()
        if current_time > expiration_time:
            return None  # Token 已过期
        
        # 返回解码后的 payload 数据
        return payload
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None  # Token 不合法或已过期
    

def generate_captcha_image(codeuuid):
    # 1.生成随机rgb数组
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    # 2. 生成随机字符串
    random_str = random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 5)

    # 3. 创建Image对象并为其配置ImageDraw对象
    img = Image.new('RGB', (270, 120), color=get_random_color())
    draw = ImageDraw.Draw(img)

    # 4. 创建ImageFont对象
    kumo_font = ImageFont.truetype('D:/project/pyProject/fileshare/file/myapp/font/KumoFont.ttf', size=40)  # 路径结合自己存放的路径

    # 5. 在img中绘制随机字符串和线条
    i, j = 25, 20
    for c in random_str:
        draw.text((i, j), c, get_random_color(), font=kumo_font)
        draw.line((random.randint(0, 270), random.randint(0, 120), random.randint(0, 270),
                random.randint(0, 120)),get_random_color(), width=3)
        i += 40
    redis_client = get_redis_connection('img_code')  # 获取redis客户端
    redis_client.setex(str(codeuuid), 60, ''.join(random_str))
    # 6. 创建字节流，用于保存Image对象
    image_bytes = BytesIO()
    img.save(image_bytes, format='png')
    data=image_bytes.getvalue()
    return data

def get_code(request,codeuuid):
    # 生成并获取验证码信息
    image_data = generate_captcha_image(codeuuid)
    # 返回带有验证码图片的响应
    return HttpResponse(image_data, content_type='image/png')

from django.core.paginator import Paginator
def get_files(request):
    currentPage = int(request.POST.get("currentPage"))
    pageSize = int(request.POST.get("pageSize"))
    files = File.objects.all().order_by('-modifie_time')
    paginator = Paginator(files, pageSize)
    page = paginator.get_page(currentPage)
    result = page.object_list  # 当前页的查询结果
    totalCount = paginator.count  # 总记录数
    list = [] 
    for item in result:
        list.append({
        'fileId': item.file_id,
        'fileName': item.file_name,
        'status': item.status,
        'fileType': item.file_type,
        })
    data={"total":totalCount,"list":list}
    return Result.success(data)