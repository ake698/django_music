# Generated by Django 2.1 on 2020-02-26 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_usermanager_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论')),
                ('to_content', models.TextField(blank=True, null=True, verbose_name='原评论')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='发布时间')),
            ],
            options={
                'verbose_name': '评论管理',
                'verbose_name_plural': '评论管理',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
            ],
            options={
                'verbose_name': '歌曲收藏管理',
                'verbose_name_plural': '歌曲收藏管理',
            },
        ),
        migrations.AddField(
            model_name='song',
            name='comments',
            field=models.IntegerField(default=0, verbose_name='收藏数量'),
        ),
        migrations.AlterField(
            model_name='usermanager',
            name='desc',
            field=models.TextField(blank=True, default='此用户比较懒，没有写个人简介！！', null=True, verbose_name='个人描述'),
        ),
        migrations.AddField(
            model_name='like',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Song', verbose_name='歌曲'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserManager', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='app.UserManager', verbose_name='回复用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='app.UserManager', verbose_name='评论用户'),
        ),
    ]
