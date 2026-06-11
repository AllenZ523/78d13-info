from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members_app.urls')),   # 将根路径指向 members_app
]