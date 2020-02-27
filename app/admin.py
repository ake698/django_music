from django.contrib import admin
from app.models import *
from django.contrib.auth.models import User,Group

# Register your models here.

admin.site.register(UserManager)
admin.site.register(Category)
admin.site.register(Song)

admin.site.site_header = "超级管理员后台"
admin.site.site_title = "超级管理员后台"
admin.site.unregister(User)
admin.site.unregister(Group)