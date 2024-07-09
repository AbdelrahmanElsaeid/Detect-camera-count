from django.urls import path
from . import views

app_name = 'videos' 
urlpatterns = [
    path('', views.home, name='home'),
    path('cameras/', views.cameras, name='cameras'),
    path('cameras/<int:id>/', views.camera_detail, name='camera_detail'),
    path('new-camera/', views.new_cameras, name='new-camera'),
    #path('upload/', views.upload_video, name='upload_video'),
    #path('videos-list/', views.video_list, name='video_list'),
    path('status/', views.status, name='status'),
]





