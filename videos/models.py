from django.db import models
from userauth.models import User
from django.utils import timezone

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    html_code = models.CharField(max_length=500,null=True, blank=True)
    cam_url = models.CharField(max_length=500,null=True, blank=True)
    active = models.BooleanField(default=False)

    

class Thumbnail(models.Model):
    video = models.ForeignKey(Video, related_name='thumbnails', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='thumbnails/')
    timestamp = models.CharField(max_length=10)
    result = models.CharField(max_length=500,null=True, blank=True)





class CameraStatus(models.Model):
    title = models.CharField(max_length=100)
    video = models.ForeignKey(Video, related_name='camera_video', on_delete=models.CASCADE)
    count = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


