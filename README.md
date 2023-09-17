# file_d
这是django写的资源管理后台

![image](https://github.com/dayuya/file_d/assets/76398179/2df09eaa-46e0-41ef-8c45-75be079d90d5)

建立虚拟环境
``` bash
python -m venv env
```
``` bash
& path/file_d/env/Scripts/activate.ps1
```
``` bash
pip install django
```

依赖....
```
corsheaders
django_redis
pickle
jwt
```
修改数据库
``` bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'file',
        'USER': 'root',  # MySQL 用户名
        'PASSWORD': 'liangzai',  # MySQL 密码
        'HOST': 'localhost',            # 数据库主机（如果在本地使用）
        'PORT': '3306',                 # 数据库端口（默认 MySQL 端口）
    }
}


# 设置redis缓存，假设redis没有设置密码；注意，项目上线时,需要调整路径
CACHES = {
    # 默认缓存, 房子0号库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
 
    # 提供给admin站点的session存储，放在1号库
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    
    # 提供存储短信验证码，放在2号库
    "img_code":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
 
}

```
``` bash
# 数据迁移文件 得cd到file项目目录
python manage.py makemigrations
```
``` bash
# 数据迁移
python manage.py migrate
```
``` bash
# 运行
python .\manage.py runserver
```
