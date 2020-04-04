from django.urls import path
from users import views as userViews
from django.contrib.auth import views as authViews


urlpatterns = [
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
    path('profile/options/', userViews.change, name='change'),
    path('profile/favourite/', userViews.favourite_list, name='favourite'),
    path('profile/', userViews.profile, name='profile'),
]
