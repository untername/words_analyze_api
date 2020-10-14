from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as lazy
from .managers import UserManager


class User(AbstractUser):

    """
    Переопределенная модель юзера.
    """

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(lazy('email address'), unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self) -> str:

        return self.username


class Analyzer(models.Model):

    CHOICES = [
        ('translate', 'Translation'),
        ('emocolor', 'Emotional color'),
        ('count-words', 'Determining word frequencies'),
        ('synonyms', 'Synonyms'),
        ('antonyms', 'Antonyms'),
        ('definitions', 'Definitions'),
        ('correct', 'Correction')]

    method = models.CharField(max_length=60, choices=CHOICES)
    text = models.TextField()
