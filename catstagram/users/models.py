from django.db import models
from django.contrib.auth.models import User


STATUS_EXPIRED = 0
STATUS_VALID = 1
RESET_STATUSES = (
    (STATUS_EXPIRED, 'expired'),
    (STATUS_VALID, 'valid'),
)

# Create your models here.
class ResetPassword(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='password_resets'
    )
    created = models.DateTimeField('date published')
    status = models.IntegerField(default=STATUS_VALID)
    days_expiration = models.IntegerField(default=1)
