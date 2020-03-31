from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        """魔术方法，在需要打印时调用"""
        return self.text

class Entry(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    class Meta:  #内部类，定义模型类的一些行为特性
        verbose_name_plural='entries'  #指定模型类的复数形式，否则会自动加“s”。  verbose_name则是指定模型的名称

    def __str__(self):
        return self.text[:50]+'...'