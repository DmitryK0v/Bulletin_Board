from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.views.static import serve

from .views import index, other_page, BBLoginView, BBLogoutView, BBPasswordChangeView, BBPasswordResetView, \
    BBPasswordResetDoneView, profile, ChangeUserInfoView, \
    RegisterUserView, RegisterDoneView, user_activate, by_rubric, detail, profile_ads_add

app_name = 'main'
urlpatterns = [
    path('accounts/password_reset/', BBPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', BBPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('account/profile/add', profile_ads_add, name='profile_ads_add'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout', BBLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
