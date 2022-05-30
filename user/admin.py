from django.contrib import admin
from .models import UserModel

# UserModel -> Admin 추가
admin.site.register(UserModel)
