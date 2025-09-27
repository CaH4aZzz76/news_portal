from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .models import Post



class NewsListView(ListView):
    model = Post
    template_name = 'flatpages/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NEW').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        if is_paginated:
            index = page_obj.number - 1
            max_index = len(paginator.page_range)
            start_index = max(index - 2, 0)
            end_index = min(index + 3, max_index)
            context['page_range'] = paginator.page_range[start_index:end_index]

        return context


class NewsSearchView(ListView):
    model = Post
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NEW')
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        date_from = self.request.GET.get('date_from')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        if is_paginated:
            index = page_obj.number - 1
            max_index = len(paginator.page_range)
            start_index = max(index - 2, 0)
            end_index = min(index + 3, max_index)
            context['page_range'] = paginator.page_range[start_index:end_index]

        context['filter_values'] = {
            'title': self.request.GET.get('title', ''),
            'author': self.request.GET.get('author', ''),
            'date_from': self.request.GET.get('date_from', ''),
        }
        return context


def news_detail(request, pk):
    news_item = get_object_or_404(Post, pk=pk)
    comments = news_item.comments.all()
    return render(request, 'flatpages/news_detail.html', {'news': news_item, 'comments': comments})


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'categories']


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    login_url = '/accounts/login/'
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.NEWS
        post.save()
        return super().form_valid(form)


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    login_url = '/accounts/login/'
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    login_url = '/accounts/login/'
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'

    def get_success_url(self):
        if self.object.post_type == Post.NEWS:
            return reverse_lazy('news_list')
        else:
            return reverse_lazy('news_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'flatpages/post_confirm_delete.html'

    def get_success_url(self):
        if self.object.post_type == Post.NEWS:
            return reverse_lazy('news_list')
        else:
            return reverse_lazy('news_list')