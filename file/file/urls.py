"""
URL configuration for file project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('viewFiles', views.view_files),
    path('test', views.test),
    path('api/login', views.login),
    path('register', views.register),
    path('api/upload', views.upload_file, name='upload_file'),
    path('api/download/<str:fileID>', views.download_file, name='download-file'),
    path('currentUser', views.currentUser, name='currentUser'),
    path('getCode/<str:codeuuid>', views.get_code, name='get_code'),
    path('getFiles', views.get_files, name='get_files'),
    path('getCategories', views.get_categories, name='get_categories'),
    path('getFilesByCategorieId', views.getFilesByCategorieId, name='getFilesByCategorieId'),
    path('editFileNameByid', views.editFileNameByid, name='editFileNameByid'),
    path('delete/<str:fileId>', views.delete, name='delete'),
]
