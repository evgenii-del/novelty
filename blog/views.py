from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import News

class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self): # новый
        query = self.request.GET.get('search','')
        if query:
            object_list = News.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)).order_by('-date')
        else:
            object_list = News.objects.all().order_by('-date')
        return object_list


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')


class NewsDetailView(DetailView):
    model = News
    template_name = 'blog/detail.html'

class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create.html'
    fields = ['title','text']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create.html'
    fields = ['title','text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'blog/delete.html'
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

def contacts(request):
    return render(request, 'blog/contacts.html')
