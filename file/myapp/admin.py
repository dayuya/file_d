from django.contrib import admin
from myapp.models import File,Categories,Permission,Role,RolePermission,Storage,FileRecord
from django.contrib.auth.models import User,Permission
# Register your models here.
admin.site.register(File)
admin.site.register(Categories)
admin.site.register(FileRecord)
admin.site.register(Storage)
admin.site.register(Permission)
