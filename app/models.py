from django.db import models
# Create your models here.


class UserManager(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    nickname = models.CharField(max_length=10,verbose_name="昵称",default="静听用户")
    desc = models.TextField(verbose_name="个人描述",null=True,blank=True,default="此用户比较懒，没有写个人简介！！")
    username = models.CharField(max_length=10,unique=True,verbose_name="账号")
    img = models.ImageField(upload_to="users", verbose_name="用户头像", null=True, blank=True, default="users/default.jpg")
    password = models.CharField(max_length=10,verbose_name="密码")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = "用户管理"


class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    category = models.CharField(max_length=10,verbose_name="分类名")
    img = models.ImageField(upload_to="category",verbose_name="分类图片",null=True,blank=True,default="category/default.jpg")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "分类管理"
        verbose_name_plural = "分类管理"


class Song(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="分类")
    title = models.CharField(max_length=40,verbose_name="歌名")
    author = models.CharField(max_length=10,verbose_name="作者",default="佚名")
    img = models.ImageField(upload_to="imgs",verbose_name="歌曲图片",null=True,blank=True,default="imgs/default.jpg")
    file = models.FileField(upload_to="files",verbose_name="歌曲文件",default="files/default.mp3")
    count = models.IntegerField(default=0,verbose_name="评论数量")
    comments = models.IntegerField(default=0,verbose_name="收藏数量")
    createTime = models.DateTimeField(auto_now=True, verbose_name="发布时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "歌曲管理"
        verbose_name_plural = "歌曲管理"


class Like(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    song = models.ForeignKey(Song,on_delete=models.CASCADE,verbose_name="歌曲")
    user = models.ForeignKey(UserManager,on_delete=models.CASCADE,verbose_name="用户")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "歌曲收藏管理"
        verbose_name_plural = "歌曲收藏管理"


class Comment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    user = models.ForeignKey(UserManager, on_delete=models.CASCADE,related_name="user",verbose_name="评论用户")
    content = models.TextField(verbose_name="评论")
    to_user = models.ForeignKey(UserManager, on_delete=models.CASCADE,related_name="to_user",null=True,blank=True,verbose_name="回复用户")
    to_content = models.TextField(null=True,blank=True,verbose_name="原评论")
    createTime = models.DateTimeField(auto_now=True, verbose_name="发布时间")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论管理"
        verbose_name_plural = "评论管理"