from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from .forms import RegistrationForm
from .models import Post, Profile, RELATIONSHIP_FOLLOWING, Hashtag, Comment

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('cats:login'))

def fireFollow(request):
    user = get_object_or_404(User, username=request.GET['username'])
    to_profile = get_object_or_404(Profile, user=user)
    from_profile = request.user.profile
    if to_profile in from_profile.get_following():
        from_profile.remove_relationship(to_profile, RELATIONSHIP_FOLLOWING)
        following = 'false'
    else:
        from_profile.add_relationship(to_profile, RELATIONSHIP_FOLLOWING)
        following = 'true'
    print(from_profile.get_following())
    return JsonResponse({'following': following})

def addComment(request):
    user = request.user
    post = get_object_or_404(Post, pk=request.GET['post_id'])
    print('COMMENT: ' + str(request.GET['comment_text']))
    print('FOR POST: ' + str(request.GET['post_id']))
    comment = Comment(author=user,
                    content=request.GET['comment_text'],
                    post=post)
    comment.save()
    return JsonResponse({
        'comment': comment.content,
        'author': user.username
    })

class HashtagView(TemplateView):
    template_name = 'cats/pages/hashtag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            hashtag = Hashtag.objects.get(name=kwargs['hashtag'])
            posts = hashtag.post.all()
        except Hashtag.DoesNotExist as e:
            posts = []
        else:
            context['posts'] = posts
            context['hashtag'] = kwargs['hashtag']
        return context

class LoginView(TemplateView):
    template_name = 'cats/pages/index.html'

    def post(self, *args, **kwargs):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('cats:home'))
        else:
            return render(self.request, 'cats/pages/index.html', {
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
        context = super().get_context_data(**kwargs)
        if kwargs:
            # viewing other profile
            username = kwargs['username']
            user = get_object_or_404(User, username=username)
            from_profile = get_object_or_404(Profile, user=self.request.user)
            to_profile = get_object_or_404(Profile, user=user)
            if to_profile in from_profile.get_following():
                follow_text = 'Unfollow'
            else:
                follow_text = 'Follow'
            context['follow_text']  = follow_text
        else:
            username = self.request.user.username
        context['profile'] = get_object_or_404(User, username=username)
        return context

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

        # identify hashtags
        tags = [i for i in caption.split() if i[0] == '#']
        for tag in tags:
            # if tag is non exisiting
            if Hashtag.objects.filter(name=tag[1:]).count() == 0:
                hashtag = Hashtag(name=tag[1:])
                hashtag.save()
            else:
                hashtag = Hashtag.objects.get(name=tag[1:])
            hashtag.post.add(post)

        return HttpResponseRedirect(reverse('cats:home'))

class EditProfileView(TemplateView):
    template_name = 'cats/pages/edit-profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        info = {
            'username': user.username,
            'f_name': user.first_name,
            'email': user.email,
            'bio': profile.bio
        }
        form = RegistrationForm(info)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, *args, **kwargs):
        form = RegistrationForm(self.request.POST)

        def return_error():
            return render(self.request, 'cats/pages/edit-profile.html', {
                                'form': form,
                                'password_error': 'Password Mismatch' })

        if form.is_valid():
            user = self.request.user
            profile = get_object_or_404(Profile, user=user)
            user.username = self.request.POST['username']
            user.first_name = self.request.POST['f_name']
            user.email = self.request.POST['email']
            profile.bio = self.request.POST['bio']
            if self.request.POST['password']:
                if self.request.POST['password'] == self.request.POST['password_confirm']:
                    user.password = self.request.POST['password']
                else:
                    return return_error()
            if self.request.FILES['image']:
                profile.profile_picture = self.request.FILES['image']
            user.save()
            profile.save()
            return HttpResponseRedirect(reverse('cats:home'))
        else:
            return return_error()

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
            user.first_name = self.request.POST['f_name']
            user.email = self.request.POST['email']
            user.password = self.request.POST['password']
            user.save()
            profile.bio = self.request.POST['bio']
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
