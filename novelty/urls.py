from django.contrib import admin
from django.urls import path, include
from users import views as userViews
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('registration/', userViews.register, name='reg'),
    path('authentication/', authViews.LoginView.as_view(template_name='users/authentication.html'), name='auth'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('pass-reset/', authViews.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
        authViews.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password_reset_done/',
        authViews.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset_complete/',
        authViews.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('profile/options', userViews.change, name='change'),
    path('profile/', userViews.profile, name='profile'),
    path('feedback/', include('feedback.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
