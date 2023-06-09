# Generated by Django 4.1.7 on 2023-04-06 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание теста'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=512, verbose_name='Название теста'),
        ),
        migrations.AlterField(
            model_name='test',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='test_images/', verbose_name='Картинка вопроса'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
