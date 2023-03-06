from django.urls import path

from .views import index, other_page, BBLoginView, BBLogoutView, BBPasswordChangeView, BBPasswordResetView, BBPasswordResetDoneView, profile, ChangeUserInfoView, \
    RegisterUserView, RegisterDoneView, user_activate

app_name = 'main'
urlpatterns = [
    path('accounts/password_reset/', BBPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', BBPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout', BBLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
