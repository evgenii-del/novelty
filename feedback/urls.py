from django.urls import path
from .views import FeedBackView


urlpatterns = [
    path('', FeedBackView.as_view(), name='feedback-view'),
]
