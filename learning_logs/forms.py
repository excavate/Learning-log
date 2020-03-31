from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):  #创建表单类
    class Meta:
        model=Topic    #指定提交表单的模型类
        fields=['text']  #指定表单包含的字段
        labels={'text':''}  #让django不要为text字段创建标签

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={"text":''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}