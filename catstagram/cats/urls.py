from django.urls import path
from .views import LoginView, HomeView,\
                    ProfileView, CreatePost,\
                    RegisterView, EditProfileView
from . import views

app_name = 'cats'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home', HomeView.as_view(), name='home'),
    path('logout', views.logoutUser, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>', ProfileView.as_view(), name='view_profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('follow/', views.fireFollow, name='follow'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-post', CreatePost.as_view(), name='create-post'),
]
