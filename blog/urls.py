from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShowNewsView.as_view(), name='blog-home'),
    path('user/<str:username>/', views.UserAllNewsView.as_view(), name='user-news'),
    path('user/<str:username>/<str:operation>/', views.change_friend, name='change-friend'),
    path('blog/<int:pk>/update/', views.UpdateNewsView.as_view(), name='news-update'),
    path('blog/<int:pk>/delete/', views.DeleteNewsView.as_view(), name='news-delete'),
    path('blog/<int:pk>/favourite/', views.favourite_post, name='favourite-post'),
    path('profile/create/', views.CreateNewsView.as_view(), name='news-create'),
    path('blog/<int:pk>/', views.post_detail, name='news-detail'),
    path('blog/review/<int:pk>/', views.AddReview.as_view(), name='review'),
    path('my-groups/', views.GroupListView.as_view(), name='my-groups'),
    path('contacts/', views.Contacts.as_view(), name='blog-contacts'),
]
