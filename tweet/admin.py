from django.contrib import admin
from .models import TweetModel, TweetComment

# UserModel -> Admin 추가
admin.site.register(TweetModel)
admin.site.register(TweetComment)
