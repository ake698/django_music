# Generated by Django 3.0.3 on 2020-02-24 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=10, verbose_name='分类名')),
                ('img', models.ImageField(blank=True, default='images/category.jpg', null=True, upload_to='static/songs/', verbose_name='分类图片')),
            ],
            options={
                'verbose_name': '分类管理',
                'verbose_name_plural': '分类管理',
            },
        ),
        migrations.AlterField(
            model_name='usermanager',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='歌名')),
                ('img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='歌曲图片')),
                ('file', models.FileField(upload_to='static/songs/', verbose_name='歌曲文件')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name': '歌曲管理',
                'verbose_name_plural': '歌曲管理',
            },
        ),
    ]
