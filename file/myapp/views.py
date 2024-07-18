from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from myapp.models import File,Categories,Storage,FileRecord
from django.db.models import F
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
import time

from django.db.models import Q

redis_conn = get_redis_connection("default")
redis_img_code = get_redis_connection('img_code')  # 获取redis客户端

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
    FileRecord.objects.create(
        # file_id=str(uuid.uuid4()).replace('-', ''),
        file_id=123,             
        user_id=1,             
        download_status='1',#  
        download_ip=1,               #  
        # download_time='example.com', #  
    )
    if not request.user.is_authenticated:
        return Result.fail(ErrorCode.NO_LOGIN.code,ErrorCode.NO_LOGIN.msg)
    return Result.success("666")
def updatepwd(request):
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    username = request.POST.get("username")
    password = request.POST.get("password")
    code = request.POST.get("code")
    randomStr = request.POST.get("randomStr")
    value = redis_img_code.get(str(randomStr))
    if aa['username'] !=username:
        return Result.fail(ErrorCode.NO_PERMISSION.code, ErrorCode.NO_PERMISSION.msg)
    if value:
        value=value.decode()
        print(value+"="+code)
    print(value)
    if not value:
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码异常")
    if code.lower() != value.lower():
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码错啦")
    # 使用 username 属性进行用户查询
    try:
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            user = User.objects.get(username=username)  # 根据用户名获取用户对象
            user.set_password(password)  # 设置新密码
            user.save()  # 保存修改后的用户对象
            return Result.success("修改成功")
        return Result.fail(ErrorCode.REGISTRATION_FAILED.code, "修改失败")
    except Exception as e:
        return Result.fail(ErrorCode.REGISTRATION_FAILED.code, "修改失败")
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    code = request.POST.get("code")
    randomStr = request.POST.get("randomStr")
    value = redis_img_code.get(str(randomStr))
    if value:
        value=value.decode()
        print(value+"="+code)
    print(value)
    if not value:
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码异常")
    if code.lower() != value.lower():
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码错啦")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,ErrorCode.ACCOUNT_PWD_NOT_EXIST.msg)
    if not user.check_password(password):
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,ErrorCode.ACCOUNT_PWD_NOT_EXIST.msg)
    user_data = {
    'username': user.username,
    'user_id': user.id,
    'first_name': user.first_name,#用户的名字
    'last_name': user.last_name,#用户的姓氏
    'is_admin': user.is_staff,#用户的姓氏
    # 添加其他必要的关键信息
    }
    # 设置有效期，例如设定为 24 小时
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    # 构建 payload 数据
    payload = {
        'user_id':user.id,
        'exp': expiration_time
    }
    # 使用 secret key 生成 JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    redis_conn.setex("TOKEN_"+token, 60*60*24,pickle.dumps(user_data))  # 键 "my_key" 将在 60*60*24 秒后过期
    return Result.success(token)
def currentUser(request):
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(403,aa)
    return Result.success(aa)

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    code = request.POST.get("code")
    randomStr = request.POST.get("randomStr")
    value = redis_img_code.get(str(randomStr))
    if value:
        value=value.decode()
        print(value+"="+code)
    print(value)
    if not value:
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码异常")
    if code.lower() != value.lower():
        return Result.fail(ErrorCode.ACCOUNT_PWD_NOT_EXIST.code,"验证码错啦")
    # 使用 username 属性进行用户查询
    try:
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            return Result.fail(ErrorCode.REGISTRATION_FAILED.code,"用户存在")
        user=User.objects.create_user(username=username, password=password)
        Storage.objects.create(
            user_id=user.id,
            allocated_size=1024*1024*1024,           
            used_size=0,          
        )        
        return Result.success(True)
    except Exception as e:
        return Result.fail(ErrorCode.REGISTRATION_FAILED.code, ErrorCode.REGISTRATION_FAILED.msg)
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('files'):
        uploaded_file = request.FILES['files']
        print(uploaded_file.size)
        aa=get_userinfo(request)
        if not aa:
            return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        file_uuid=str(uuid.uuid4()).replace('-', '')
        new_file = File.objects.create(
            file_id=file_uuid,
            user_id=aa['user_id'],          
            file_type=file_extension[1:],           
            file_size=uploaded_file.size,           
            file_name=file_name,
            status=0,              
            file_url=file_uuid, 
        )
        # 确保 upload 文件夹存在
        upload_folder = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(upload_folder, exist_ok=True)
        # 构造文件的保存路径
        file_path = os.path.join(upload_folder, file_uuid+"."+file_extension[1:])
        # 保存文件到指定路径
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        storage =Storage.objects.filter(user_id=aa['user_id']).update(used_size=F('used_size')+uploaded_file.size)
        if storage>0:
            pass
        return Result.success("文件上传成功")
    return Result.fail(400,'请求方法错误或没有选择文件')
def download_file(request, fileID):
    aa=get_userinfo(request)
    user_id=aa['user_id'] 
    try:
         user=User.objects.get(id=user_id)
    except User.DoesNotExist:
        FileRecord.objects.create(
            file_id=fileID,             
            user_id=user_id,             
            download_status='1', 
            download_ip=1,                
        )
        return Result.fail(403,'无权限')
    file=File.objects.get(file_id=fileID)
    if user_id!=user_id and not user.is_staff and file.status==2:
        FileRecord.objects.create(
            file_id=fileID,             
            user_id=user_id,             
            download_status='1',  
            download_ip=1,                 
        )
        return Result.fail(403,'无权限')
    file_type=file.file_type
    filename=str(file.file_name+"."+file_type)
    file_url=file.file_url
    # 确定文件的保存路径
    file_path = os.path.join(settings.MEDIA_ROOT, file_url+'.'+file_type)
    if os.path.exists(file_path):
        import mimetypes
        # 获取文件的MIME类型
        content_type, _ = mimetypes.guess_type(file_path)
        # 打开文件并返回给客户端进行下载
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Access-Control-Expose-Headers'] = "Content-Disposition"
            response['Content-Disposition'] = f'attachment; filename="{filename.encode("utf-8").decode("latin-1")}"'
            FileRecord.objects.create(
                file_id=fileID,             
                user_id=user_id,             
                download_status='1', 
                download_ip=1,                 
            )
            return response
    else:
        FileRecord.objects.create(
            file_id=fileID,             
            user_id=user_id,             
            download_status='0',
            download_ip=1,               
        )
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
    img = Image.new('RGB', (390, 120), color=get_random_color())
    draw = ImageDraw.Draw(img)

    # 4. 创建ImageFont对象
    kumo_font = ImageFont.truetype('D:/project/pyProject/fileshare/file/myapp/font/KumoFont.ttf', size=80)  # 路径结合自己存放的路径

    # 5. 在img中绘制随机字符串和线条
    i, j = 75, 20
    for c in random_str:
        draw.text((i, j), c, get_random_color(), font=kumo_font)
        draw.line((random.randint(0, 390), random.randint(0, 180), random.randint(0, 390),
                random.randint(0, 180)),get_random_color(), width=3)
        i += 50
    print(str(codeuuid))
    redis_img_code.setex(str(codeuuid), 600, ''.join(random_str))
    value = redis_img_code.get(str(codeuuid)).decode()
    print(value)
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
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    currentPage = request.POST.get("currentPage")
    pageSize = request.POST.get("pageSize")
    queryInput = request.POST.get("queryInput")
    queryStatus = request.POST.get("queryStatus")
    categorieId = request.POST.get("queryCategorie")
    files = File.objects.filter(user_id=aa['user_id']).order_by('-modifie_time')
    
    # 使用 Q 对象创建复杂的查询条件
    query = Q()

    if queryStatus != "all":
        query &= Q(status=queryStatus)
    if queryInput is not None and queryInput!="null":
        query &= Q(file_name__icontains=queryInput)
    if categorieId != "all":
        category = Categories.objects.get(id=categorieId)
        categoryTypes = tuple(category.type.split(","))
        query &= Q(file_type__in=categoryTypes)

    # 应用查询条件
    files = files.filter(query)

    paginator = Paginator(files, pageSize)
    page = paginator.get_page(currentPage)
    result = page.object_list  # 当前页的查询结果
    totalCount = paginator.count  # 总记录数
    list = [] 
    status={0:"未发布",1:"审核中",2:"通过",3:"驳回"}
    for item in result:
        list.append({
        'fileId': item.file_id,
        'fileName': item.file_name,
        'status': status[item.status],
        'fileType': item.file_type,
        'modifieTime':item.modifie_time,
        'username':aa['username'],
        'user_id':aa['user_id'],
        })
    data={"total":totalCount,"list":list}
    return Result.success(data)

def get_categories(request):
    Categorie=Categories.objects.all().values('id','name')
    return Result.success(list(Categorie))
def getFilesByCategorieId(request):
    categorieId = request.POST.get("id")
    category = Categories.objects.get(id=categorieId)
    categoryTypes=tuple(category.type.split(","))
    files = File.objects.filter(file_type__in=categoryTypes).order_by('-modifie_time')
    print(files.query)
    data = [] 
    for item in files:
        data.append({
        'fileId': item.file_id,
        'fileName': item.file_name,
        'status': item.status,
        'fileType': item.file_type,
        })
    return Result.success(data)


def editFileNameByid(request):
    fileId = request.POST.get("id")
    status={"未发布":0,"审核中":1,"通过":2,"驳回":3}
    file = File.objects.filter(file_id=fileId).update(status=status['审核中'],modifie_time=int(time.time()*1000))
    if file>0:
        return Result.success("更新成功")
    return Result.fail(500,"更新失败")
def delete(request,fileId):
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    file=File.objects.get(file_id=fileId)
    filesize=file.file_size
    file_count, file_objects = file.delete()
    if file_count>0:
        storage =Storage.objects.filter(user_id=file.user_id).update(used_size=F('used_size')-filesize)
        if storage>0:
            pass
        return Result.success("删除成功")
    return Result.fail(500,"找不到文件")


def get_userinfo(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if checkToken(token) is None:
        return False
    userJson = redis_conn.get("TOKEN_" + token)  # 根据 token 获取用户信息
    if not userJson:
        return False
    aa=pickle.loads(userJson) 
    return aa


def getStoarge(request):
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    try:
        storage = Storage.objects.get(user_id=aa['user_id'])
    except Storage.DoesNotExist:
        return Result.fail(0,"存储异常")
    data={}
    data['allocated_size']=storage.allocated_size
    data['used_size']=storage.used_size
    return Result.success(data)


def getFilesShare(request):
    aa=get_userinfo(request)
    if not aa:
        return Result.fail(ErrorCode.NO_LOGIN.code, ErrorCode.NO_LOGIN.msg)
    currentPage = request.POST.get("currentPage")
    pageSize = request.POST.get("pageSize")
    queryInput = request.POST.get("queryInput")
    categorieId = request.POST.get("queryCategorie")
    files = File.objects.order_by('-modifie_time')
    
    # 使用 Q 对象创建复杂的查询条件
    query = Q()
    status={"未发布":0,"审核中":1,"通过":2,"驳回":3}
    query &= Q(status=status["通过"])
    if queryInput is not None and queryInput!="null":
        query &= Q(file_name__icontains=queryInput)
    if categorieId != "all":
        category = Categories.objects.get(id=categorieId)
        categoryTypes = tuple(category.type.split(","))
        query &= Q(file_type__in=categoryTypes)

    # 应用查询条件
    files = files.filter(query)
    print(files.query)
    paginator = Paginator(files, pageSize)
    page = paginator.get_page(currentPage)
    result = page.object_list  # 当前页的查询结果
    totalCount = paginator.count  # 总记录数
    list = [] 
    status={0:"未发布",1:"审核中",2:"通过",3:"驳回"}
    for item in result:
        try:
             user=User.objects.get(id=item.user_id)
        except User.DoesNotExist:
            list.append({
            'fileId': item.file_id,
            'fileName': item.file_name,
            'status': status[item.status],
            'fileType': item.file_type,
            'modifieTime':item.modifie_time,
            'username':None,
            'user_id':None,
            })
            continue
        list.append({
        'fileId': item.file_id,
        'fileName': item.file_name,
        'status': status[item.status],
        'fileType': item.file_type,
        'modifieTime':item.modifie_time,
        'username':user.username,
        'user_id':user.id,
        })
    data={"total":totalCount,"list":list}
    return Result.success(data)

