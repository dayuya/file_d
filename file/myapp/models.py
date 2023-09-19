from django.db import models
import time
import uuid
# Create your models here.
class File(models.Model):
    file_id = models.CharField(max_length=32,primary_key=True, default=str(uuid.uuid4()).replace('-', ''))
    user_id = models.BigIntegerField(null=False)
    file_type = models.CharField(max_length=10,null=True, default=None)
    file_name = models.CharField(max_length=255, null=True, default=None)
    status = models.PositiveSmallIntegerField(null=True, default=None)
    file_url = models.CharField(max_length=255, null=True, default=None)
    modifie_time = models.BigIntegerField(default=int(time.time()*1000))
    class Meta:
        db_table = 'file'  # 指定数据库中的表名
class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'categories'  # 指定数据库中的表名

class Permission(models.Model):
    permission_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'permission'  # 指定数据库中的表名

class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'role'  # 指定数据库中的表名
class RolePermission(models.Model):
    role_id = models.BigIntegerField(primary_key=True)
    permission_id = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'role_permission'  # 指定数据库中的表名
class Storage(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    allocated_size = models.BigIntegerField(null=True, blank=True, default=None)
    used_size = models.BigIntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'storage'
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=64, null=True, blank=True, default=None)
    password = models.CharField(max_length=255)
    role_id = models.BigIntegerField()
    account = models.CharField(max_length=64)

    class Meta:
        db_table = 'user'