from django.db import models


CHOICES = [
    ('translate', 'Translation'),
    ('emocolor', 'Emotional color'),
    ('count-words', 'Determining word frequencies'),
    ('synonyms', 'Synonyms'),
    ('antonyms', 'Antonyms'),
    ('definitions', 'Definitions')
    ]


class Analyzer(models.Model):
    method = models.CharField(max_length=60, choices=CHOICES)
    text = models.TextField()

# Create your models here.
