from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F, Count
from django.contrib import messages
from blog.forms import ReviewForm
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.contrib.auth.models import User
from blog.models import News, Rate
from users.models import Profile


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

    def get_queryset(self):
        query = self.request.GET.get('search','')
        if query:
            object_list = News.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        else:
            object_list = News.objects.all()
        return object_list.order_by('-date')

class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['test'] = user.friend.all()
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')

def change_friend(request, operation, username):
    new_friend = User.objects.get(username=username)
    if operation == 'add':
        Profile.add_friend(request.user, new_friend)
    elif operation == 'del':
        Profile.del_friend(request.user, new_friend)
    return redirect('/')

def post_detail(request, pk):
    post = get_object_or_404(News, pk=pk)
    is_favourite = False
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True
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
        return redirect(post.get_absolute_url())

class Contacts(TemplateView):
    template_name = 'blog/contacts.html'

class GroupListView(ListView):
    model = News
    template_name = 'blog/my_group.html'
    context_object_name = 'news'
    paginate_by = 10
