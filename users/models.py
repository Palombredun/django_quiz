from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_certified = models.BooleanField('certified user', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_admin = models.BooleanField('admin status', default=False)

    def __str__(self):
        return self.email