from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ad, Comment
from django.views import View
from .forms import AdForm, CommentForm, SignUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User


def home(request):
    ads = Ad.objects.all()
    return render(request, 'ad_list.html', {'ads': ads})

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ad_update.html'  
    success_url = reverse_lazy('home')

    def get_queryset(self): 
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        ad.save()
        return super().form_valid(form)

    
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['text']  
    template_name = 'comment_update.html'  
    success_url = reverse_lazy('home')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
    
class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy('ad_list')
    template_name = 'ad_confirm_delete.html'

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.ad.pk})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)  # Передайте request.FILES в форму для обработки загруженных файлов
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ad_create.html', {'form': form})

def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ad_list.html', {'ads': ads})

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required
def comment_create(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.author = request.user
            comment.save()
            return redirect('ad_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'comment_create.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

class SignUpWithVerification(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response


class VerificationSuccessView(TemplateView):
    template_name = 'registration/verification_success.html'


class VerificationErrorView(TemplateView):
    template_name = 'registration/verification_error.html'


class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = get_user_model().objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verification_success')
        else:
            return redirect('verification_error')

def profile_view(request, user_id=None):
    if user_id:
        profile_user = User.objects.get(pk=user_id)
    else:
        profile_user = request.user
    ads = Ad.objects.filter(author=profile_user)
    date_joined = profile_user.date_joined
    return render(request, 'profile_view.html', {'profile_user': profile_user, 'ads': ads, 'date_joined': date_joined})