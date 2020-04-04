from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import News, Rate
from django.contrib import messages
from blog.forms import ReviewForm


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["popular"] = News.objects.order_by("-count")[:7]
        context["rate"] = Rate.objects.all()
        return context

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

def post_detail(request, pk):
    post = get_object_or_404(News, pk=pk)
    is_favourite = False
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True
        messages.success(request, 'Статья успешно добавлена/удалена из избранного')
    News.objects.filter(pk=pk).update(count=F('count')+1)
    return render(request, 'blog/detail.html', {'object': post, 'is_favourite': is_favourite})

def favourite_post(request, pk):
    post = get_object_or_404(News, id=pk)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'img']

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
    fields = ['title', 'text', 'img']

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

class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        post = News.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.user = request.user
            form.save()
        return redirect('/')

class Contacts(TemplateView):
    template_name = 'blog/contacts.html'
