from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


class Logo(models.Model):
    image = CloudinaryField(folder='home/logo/')
    
    

class bukMosque(models.Model):
    image = CloudinaryField(folder='home/logo/')


class Shiekh(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField(folder='home/image/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    

class Book(models.Model):
    shiekh = models.ForeignKey(Shiekh, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.title
    
class AudioEpisode(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    audio_file = CloudinaryField(resource_type='auto',folder='home/audio_files')


    def __str__(self) -> str:
        return self.title
    