from django.shortcuts import render
from .models import Topic,Entry
from django.http import HttpResponseRedirect,Http404  #重定向模块
from django.urls import reverse  #reverse模块根据指定的url确定url
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')  #filter筛选器实现用户只能访问自己的主题
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    """显示单个主题及其内容"""
    topic=Topic.objects.get(id=topic_id)
    if topic.owner!=request.user:                              #if判断实现用户只能访问自己的主题
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,"learning_logs/topic.html",context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method!='POST':
        form=TopicForm()
    else:
        form=TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)       #先不提交，把表单form的值传递给新表单new_topic,后续修改
            new_topic.owner=request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """添加新条目"""
    topic=Topic.objects.get(id=topic_id)
    if topic.owner!=request.user:
        raise Http404
    if request.method!="POST":
        form=EntryForm()

    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    context = {'form': form, 'topic': topic}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request,entry_id):
    """编辑已有条目"""
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic

    if topic.owner!=request.user:           #if判断实现用户只能访问自己的主题
        raise Http404
    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            edit_entry=form.save(commit=False)
            edit_entry.date_added=timezone.now()
            edit_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)