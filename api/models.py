from django.db import models
from djongo import models

# Create your models here.

class PDFData(models.Model):
    email = models.EmailField(unique=True)
    content = models.TextField()
    nouns = models.TextField()
    verbs = models.TextField()

    def __str__(self):
        return self.email

