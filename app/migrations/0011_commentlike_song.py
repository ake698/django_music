# Generated by Django 2.1 on 2020-02-27 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_commentlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentlike',
            name='song',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.Song', verbose_name='歌曲'),
        ),
    ]
