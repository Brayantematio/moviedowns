from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)  # Le titre de la vidéo
    file = models.FileField(upload_to='videos/')  # Le fichier vidéo
    uploaded_at = models.DateTimeField(auto_now_add=True)  # La date d'upload

    def __str__(self):
        return self
