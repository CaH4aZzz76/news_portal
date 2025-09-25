from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    news = Post.objects.filter(post_type__in=['NEW', 'ART'])
    return render(request, 'flatpages/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(Post, pk=pk)
    comments = news_item.comments.all()
    return render(request, 'flatpages/news_detail.html', {'news': news_item, 'comments': comments})
