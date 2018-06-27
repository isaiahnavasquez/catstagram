from django.urls import path
from api.views import ProfileList, ProfileDetail


urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/<str:username>', ProfileDetail.as_view()),
]