from django.contrib import admin
from .models import Video,Thumbnail, CameraStatus
# Register your models here.


admin.site.register(Video)
admin.site.register(Thumbnail)
admin.site.register(CameraStatus)


