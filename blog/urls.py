from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShowNewsView.as_view(), name='blog-home'),
    path('user/<str:username>', views.UserAllNewsView.as_view(), name='user-news'),
    path('blog/<int:pk>/update', views.UpdateNewsView.as_view(), name='news-update'),
    path('blog/<int:pk>/delete', views.DeleteNewsView.as_view(), name='news-delete'),
    path('profile/create', views.CreateNewsView.as_view(), name='news-create'),
    path('blog/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('contacts/', views.contacts, name='blog-contacts'),
]
