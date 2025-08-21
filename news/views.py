from django.shortcuts import render
from .models import News

def news(request):
    news_s = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news_s':news_s})
