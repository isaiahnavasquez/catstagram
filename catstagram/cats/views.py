from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from .forms import RegistrationForm
from .models import Post, Profile

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('cats:login'))

class LoginView(TemplateView):
    template_name = 'cats/pages/index.html'

    def post(self, *args, **kwargs):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('cats:home'))
        else:
            return render(self.request, 'blogs/login.html', {
                'error_message': 'Invalid Credentials. Please Try Again.'
            })

class HomeView(TemplateView):
    template_name = 'cats/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class ProfileView(TemplateView):
    template_name = 'cats/pages/profile.html'

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        if kwargs:
            username = kwargs['username']
        else:
            username = self.request.user.username
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=username)
        return context

class EditProfileView(TemplateView):
    template_name = 'cats/pages/edit-profile.html'

class CreatePost(TemplateView):
    template_name = 'cats/pages/create-post.html'

    def post(self, *args, **kwargs):
        caption = self.request.POST['caption']
        author = self.request.user
        pub_date = timezone.now()
        image = self.request.FILES['image']
        post = Post(caption=caption,
                    author=author,
                    pub_date=pub_date,
                    picture=image)
        post.save()
        return HttpResponseRedirect(reverse('cats:home'))

class RegisterView(TemplateView):
    template_name = 'cats/pages/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RegistrationForm
        context['form'] = form
        return context

    def post(self, *args, **kwargs):
        if self.request.POST['password'] == self.request.POST['password_confirm'] and RegistrationForm(self.request.POST).is_valid():
            user = User()
            profile = Profile()
            user.username = self.request.POST['username']
            user.f_name = self.request.POST['f_name']
            user.email = self.request.POST['email']
            profile.bio = self.request.POST['bio']
            user.password = self.request.POST['password']
            user.save()
            profile.user = user
            profile.save()
            login(self.request, user)
            return HttpResponseRedirect(reverse('cats:home'))
        else:
            form = RegistrationForm(self.request.POST)
            return render(self.request, 'cats/pages/register.html', {
                        'form': form,
                        'password_error': 'Password Mismatch'
                    })
