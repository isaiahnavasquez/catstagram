from django.urls import path
from .views import LoginView, HomeView,\
                    ProfileView, CreatePost,\
                    RegisterView, EditProfileView,\
                    HashtagView, PostView, ExploreView
from . import views

app_name = 'cats'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home', HomeView.as_view(), name='home'),
    path('logout', views.logoutUser, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>', ProfileView.as_view(), name='view_profile'),
    path('post/<int:id>', PostView.as_view(), name='view_post'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-post', CreatePost.as_view(), name='create-post'),
    path('hashtag/<str:hashtag>', HashtagView.as_view(), name='hashtag'),
    path('follow/', views.fireFollow, name='follow'),
    path('add-comment/', views.addComment, name='add_comment'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('search/', views.search, name='search'),
]
