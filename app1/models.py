# encoding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    # sex = models.BooleanField(max_length=1, blank=True, choices=((0, '男'), (1, '女')))
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


class Image(models.Model):
    name = models.CharField(max_length=30, null=False, blank=True, verbose_name='图片名称')
    img_url = models.ImageField(upload_to='photos', null=False, blank=True, verbose_name='图片路径')
    publish_date = models.DateField(auto_now_add=True, verbose_name='发表时间')
    desc = models.CharField(max_length=30, verbose_name='描述')
    likes = models.IntegerField(default=0, verbose_name='喜欢数')
    count = models.IntegerField(default=0, verbose_name='浏览量')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    user = models.ForeignKey(User, verbose_name='用户')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    comment_text = models.TextField(verbose_name='评论正文')
    comment_date = models.DateField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, verbose_name='评论者')
    img = models.ForeignKey(Image, verbose_name='评论图片')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.comment_text
