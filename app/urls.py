from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:pk>/comment/create/', views.comment_create, name='comment_create'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
