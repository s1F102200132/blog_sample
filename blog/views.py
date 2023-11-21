from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.http import Http404
from django.utils import timezone
from django.urls import reverse
import random
from blog.models import Article, Comment
from blog.form import ArticleForm



# Create your views here.
def index(request):
    if request.method == 'POST':
        article = Article(title=request.POST['title'], body=request.POST['text'])
        article.save()
        return redirect(detail, article.id)
    if ('sort' in request.GET):
        if request.GET['sort'] == 'like':
            articles = Article.objects.order_by('-like')
        else:
            articles = Article.objects.order_by('-posted_at')
    else:
        articles = Article.objects.order_by('-posted_at')
    context = {
        "articles": articles
    }
    return render(request, 'blog/index.html', context)
    

def hello(request):
     #ランダムに生成したおみくじの結果を保持する変数
    isGreatFortune = False
    fortuneMessage = 'y'
    date = {
        'name': 'Alice',
        'weather': 'CLOUDY',
        'weather_detail': ['Temperature: 23℃', 'Humidity: 40%', 'Wind: 5m/s'],
        'isGreatFortune': isGreatFortune,
        'fortune': random.choices(fortuneMessage)

    }
    return render(request, 'blog/hello.html', date)
def redirect_test(request):
    return redirect(hello)

def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    if request.method == 'POST':
        comment = Comment(article=article, text=request.POST['text'])
        comment.save()
    context = {
        'article' : article,
        'comments': article.comments.order_by('-posted_at')
    }
    return render(request, "blog/detail.html", context)
def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    
    

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article_id)
        

    context = {
        "article_id": article
    }
    return render(request, "blog/edit.html", {'article': article})

def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    article.delete()
    return redirect(index)

def like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    return redirect(detail, article_id)

#新機能
def tbd(request):
    return render(request, "blog/tbd.html")


