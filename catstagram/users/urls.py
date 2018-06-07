from django.urls import path
from .views import(
    ResetPasswordView,
    ConfirmResetPasswordview
)


app_name = 'users'
urlpatterns = [
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-confirm', ConfirmResetPasswordview.as_view(), name='confirm-reset-password'),
]
