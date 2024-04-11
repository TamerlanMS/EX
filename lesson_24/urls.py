"""
URL configuration for lesson_24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app.views import logout_view, RegisterView, CommentUpdateView, AdUpdateView, AdDeleteView, CommentDeleteView, VerifyEmailView, VerificationSuccessView, VerificationErrorView, SignUpWithVerification, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verification_success/', VerificationSuccessView.as_view(), name='verification_success'),
    path('verification_error/', VerificationErrorView.as_view(), name='verification_error'),
    path('signup/', SignUpWithVerification.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/<int:pk>/', profile_view, name='profile'),
]
