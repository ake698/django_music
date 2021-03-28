from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db.models import Q
import json


# Create your views here.

# 拦截器 用于检测用户是否登录
def check(func):
    def wra(req, *arg, **kwargs):
        if not req.session.get('active'):
            return redirect("/login/")
        return func(req, *arg, **kwargs)

    return wra


# 获取当前登录的用户
def getUser(request):
    username = request.session['active']
    user = UserManager.objects.get(username=username)
    return user


# 首页
def index(request):
    songs = Song.objects.all()
    cates = Category.objects.all()
    comment_songs = songs.order_by("count")
    new_songs = songs.order_by("-createTime")
    return render(request, 'index.html',
                  {"cates": cates, "songs": songs, "comment_songs": comment_songs, "new_songs": new_songs})


def echart(request):
    cates = Category.objects.all()
    return render(request, 'echart.html', {"cates": cates})


def echart_data(request):
    songs = Song.objects.all().order_by("-broadcast")
    categoriy_data = []
    categories = Category.objects.all()
    for i in categories:
        count = i.song_set.count()
        categoriy_data.append({"name":i.category,"value":count})
    result = {"category":categoriy_data,"clound": [], "y_datas": list(songs.values_list("broadcast", flat=True))}
    type = request.GET.get("type")
    if type:
        if type == "like":
            songs = songs.order_by("-comments")
            result["y_datas"] = list(songs.values_list("comments", flat=True))
        if type == "comment":
            songs = songs.order_by("-count")
            result["y_datas"] = list(songs.values_list("count", flat=True))
    if songs.count() >= 10:
        songs = songs[:10]
    result["x_datas"] = list(songs.values_list("title", flat=True))
    print(result["x_datas"])
    print(result["y_datas"])
    for i in range(songs.count()):
        name = result["x_datas"][i]
        value = result["y_datas"][i]
        result["clound"].append({"name":name,"value": value})
    return HttpResponse(json.dumps(result), content_type="application/json")


@check
# 播放页面
def player(request, id):
    try:
        song = Song.objects.get(id=int(id))
    except:
        return HttpResponse("歌曲错误！！")
    cates = Category.objects.all()
    # 查询此作者的其他歌曲
    songs = Song.objects.filter(author=song.author).exclude(id=int(id))
    if len(songs) < 1:
        songs = Song.objects.filter(category=song.category).exclude(id=int(id))
        if len(songs) < 1:
            songs = Song.objects.all()[:5]
    # 获取评论
    comments = Comment.objects.filter(song__id=int(id))
    user = getUser(request)
    return render(request, 'player.html',
                  {"cates": cates, "song": song, "songs": songs, "comments": comments, "user": user})


@check
# 评论收藏
def commentsLike(request):
    result = {
        "code": "400",
        "msg": "错误！",
    }
    user = getUser(request)
    if request.method == "POST":
        songId = request.POST['songId']
        commentId = request.POST['commentId']
        flag = request.POST['flag']

        song = Song.objects.get(id=int(songId))
        comment = Comment.objects.get(id=int(commentId))
        if flag == "like":
            # 收藏评论
            CommentLike.objects.create(song=song, comment=comment, user=user)
        else:
            # 取消收藏
            CommentLike.objects.filter(comment=comment).delete()
        result['code'] = "200"
        result['msg'] = "操作成功！"
        return HttpResponse(json.dumps(result), content_type="application/json")
    try:
        id = request.GET['id']
    except:
        return HttpResponse(json.dumps(result), content_type="application/json")

    likes = CommentLike.objects.filter(user=user, song__id=int(id))
    likelist = []
    for i in likes:
        likelist.append(i.comment.id)
    result['data'] = likelist
    result['code'] = "200"
    result['msg'] = "成功！"
    return HttpResponse(json.dumps(result), content_type="application/json")


@check
# 歌曲收藏
def like(request):
    result = {
        "code": "400",
        "msg": "错误！",
    }
    if request.method == "POST":
        id = request.POST.get("id")
        flag = request.POST.get("flag")
        song = Song.objects.get(id=id)
        if flag == "like":
            # 收藏歌曲
            like = Like(song=song, user=getUser(request))
            like.save()
            song.count = song.count + 1
        else:
            # 取消收藏歌曲
            Like.objects.filter(song=song, user=getUser(request)).delete()
            song.count = song.count - 1
        result['code'] = "200"
        result['msg'] = "操作成功！"
        song.save()
        return HttpResponse(json.dumps(result), content_type="application/json")
    try:
        id = request.GET['id']
    except:
        return HttpResponse(json.dumps(result), content_type="application/json")
    song = Song.objects.get(id=id)
    like = Like.objects.filter(song=song, user=getUser(request)).count()
    result['code'] = "200"
    result['msg'] = "操作成功！"
    result['data'] = like
    return HttpResponse(json.dumps(result), content_type="application/json")


@check
# 发表评论
def comment(request):
    result = {
        "code": "400",
        "msg": "错误！",
    }
    if request.method == "POST":
        id = request.POST.get("id")
        content = request.POST['content']
        user = getUser(request)
        song = Song.objects.get(id=int(id))
        # 创建评论
        Comment.objects.create(song=song, user=user, content=content)
        result['code'] = "200"
        result['msg'] = "操作成功！"
        song.comments += 1
        song.save()
    return HttpResponse(json.dumps(result), content_type="application/json")


@check
# 回复评论
def replyComment(request):
    result = {
        "code": "400",
        "msg": "错误！",
    }
    if request.method == "POST":
        content = request.POST['content']  # 评论内容
        commentId = request.POST['commentId']  # 原评论id

        user = getUser(request)
        comment = Comment.objects.get(id=int(commentId))
        song = comment.song  # 评论的歌曲
        to_user = comment.user
        to_conent = comment.content
        if comment.user_id == user.id:
            result['msg'] = "不能自己回复自己的评论！"
            return HttpResponse(json.dumps(result), content_type="application/json")

        # 创建评论
        c = Comment.objects.create(song=song, user=user, content=content, to_user=to_user, to_content=to_conent)
        result['code'] = "200"
        result['msg'] = "操作成功！"
        song.comments += 1
        song.save()
    return HttpResponse(json.dumps(result), content_type="application/json")


@check
# 个人中心
def person(request):
    cates = Category.objects.all()
    user = getUser(request)
    likes = Like.objects.filter(user=user)
    comments = CommentLike.objects.filter(user=user)
    return render(request, 'person.html', {"cates": cates, "user": user, "likes": likes, "comments": comments})


@check
# 修改个人信息
def modify(request):
    user = getUser(request)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        userimg = request.POST.get("userimg")
        user.nickname = title
        user.desc = description
        user.img = userimg
        user.save()
        result = {
            "code": "200",
            "msg": "操作成功！",
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    cates = Category.objects.all()
    return render(request, 'modify.html', {"cates": cates, "user": user})


@check
# 上传图片并返回图片链接
def imgUpload(request):
    result = {
        "code": "400",
        "msg": "msg",
    }
    if request.method == "POST":
        img = request.FILES.get('files')
        if img != None and img != "":
            from Music.settings import MEDIA_ROOT
            import os, time
            filesp = img.name.split(".")
            fileType = filesp[-1]
            if (fileType not in ["jpg", "png", "jpeg"]):
                result["msg"] = "格式错误!"
                return HttpResponse(json.dumps(result), content_type="application/json")
            filesp.pop(-1)
            fileName = "%s_%s.%s" % ("".join(filesp), int(round(time.time() * 1000)), fileType)
            f = open(os.path.join(MEDIA_ROOT, "users", fileName), 'wb')
            for chunk in img.chunks():
                f.write(chunk)
            f.close()
            result['code'] = "200"
            result['msg'] = "users/%s" % (fileName)
            return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")


# 分类页面
def category(request, id):
    cates = Category.objects.all()
    cate = cates.get(id=int(id))
    return render(request, 'category.html', {"cates": cates, "cate": cate, "id": int(id)})


# 搜索页面
def search(request):
    try:
        key = request.GET['key']
    except:
        return redirect("/index/")
    cates = Category.objects.all()
    songs = Song.objects.filter(Q(author__contains=key)
                                | Q(title__contains=key)
                                )
    return render(request, 'search.html', {"cates": cates, "songs": songs})


# 返回验证码
def get_code(request):
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random, os
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    ttrFile = os.path.join(os.path.dirname(__file__), 'kt.ttf')
    font = ImageFont.truetype(ttrFile, 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 用户登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        j_captcha = request.POST['j_captcha'].upper()
        code = request.session.get('verifycode').upper()
        if code != j_captcha:
            return HttpResponse("2")
        user = UserManager.objects.filter(username=username, password=passwd)
        if user:
            request.session["active"] = username
            return HttpResponse("0")
        else:
            return HttpResponse("1")
    else:
        return render(request, 'login.html')


@check
# 用户注销
def logout(request):
    request.session.flush()
    response = HttpResponse("注销成功")
    response['Refresh'] = "2;/index/"
    return response


# 用户注册
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        j_captcha = request.POST['j_captcha'].upper()
        code = request.session.get('verifycode').upper()
        if code != j_captcha:
            return HttpResponse("2")
        user = UserManager.objects.filter(username=username)
        if user:
            return HttpResponse("1")
        else:
            UserManager.objects.create(username=username, password=passwd).save()
            return HttpResponse("0")
    else:
        return render(request, 'register.html')
