import os
import cv2
from django.shortcuts import get_object_or_404, render, redirect
from .forms import VideoForm, VideoForm
from .models import Video,CameraStatus, Thumbnail
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages





# def capture_thumbnails(video_path, num_frames=10):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_interval = frame_count // num_frames

#     thumbnails = []
#     for i in range(num_frames):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
#         ret, frame = cap.read()
#         if ret:
#             filename = f"{os.path.basename(video_path).split('.')[0]}_frame{i}.jpg"
#             image_path = os.path.join('media/thumbnails', filename)
#             cv2.imwrite(image_path, frame)
#             thumbnails.append(image_path)
#     cap.release()
#     return thumbnails



# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video_instance = form.save()
#             video_path = video_instance.video.path
#             thumbnail_paths = capture_thumbnails(video_path)
#             for thumbnail_path in thumbnail_paths:
#                 with open(thumbnail_path, 'rb') as f:
#                     thumbnail = Thumbnail(video=video_instance)
#                     thumbnail.image.save(os.path.basename(thumbnail_path), ImageFile(f), save=False)
#                     thumbnail.save()
#             return redirect('videos:video_list')
#     else:
#         form = VideoForm()
#     return render(request, 'videos/upload_video.html', {'form': form})


# def video_list(request):
#     videos = Video.objects.all()
#     return render(request, 'videos/video_list.html', {'videos': videos})





def home(request):
    return render(request, 'home.html')





def capture_thumbnails(video_path, num_frames=10):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = frame_count // num_frames

    thumbnails = []
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
        ret, frame = cap.read()
        if ret:
            # Capture the timestamp (in milliseconds) of the current frame
            timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp_seconds = timestamp_ms / 1000.0

            # Convert timestamp to minute:second format
            minutes = int(timestamp_seconds // 60)
            seconds = int(timestamp_seconds % 60)
            formatted_timestamp = f"{minutes}:{seconds:02}"  # Ensure seconds are two digits
            
            # Save the frame as an image
            filename = f"{os.path.basename(video_path).split('.')[0]}_frame{i}.jpg"
            image_path = os.path.join('media/thumbnails', filename)
            cv2.imwrite(image_path, frame)
            
            # Create Thumbnail object and save it with timestamp
           
            
            thumbnails.append((image_path, formatted_timestamp))
    cap.release()
    return thumbnails



@login_required
def cameras(request):
    videos = Video.objects.filter(user=request.user)
    active_videos_count = videos.filter(active=True).count()
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        action = request.POST.get('action')
        q = get_object_or_404(Video, id=video_id)
        if action == 'activate':
            q.active = True
            q.save()

            # add logic capture image  

            if not q.thumbnails.exists():                         
                video_path = q.video.path
                thumbnail_data = capture_thumbnails(video_path)
                
                for image_path, timestamp in thumbnail_data:
                    with open(image_path, 'rb') as f:
                        thumbnail = Thumbnail(video=q, timestamp=timestamp)
                        thumbnail.image.save(os.path.basename(image_path), ImageFile(f), save=False)
                        thumbnail.save()

                # add logic to perform model and save results 

                
                        
                    


        elif action == 'deactivate':
            q.active = False
            q.save()

        return redirect('videos:cameras')
    return render(request, 'videos/cameras.html', {'videos': videos, 'active_videos_count': active_videos_count})



   






def status(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    results = CameraStatus.objects.all()

    if query:
        results = results.filter(title__icontains=query)
    
    if start_date:
        results = results.filter(date__gte=parse_datetime(start_date))
    
    if end_date:
        results = results.filter(date__lte=parse_datetime(end_date))

    return render(request, 'videos/status.html', {'results': results, 'query': query, 'start_date': start_date, 'end_date': end_date})







@login_required
def new_cameras(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user  
            video.save()           
            return redirect('videos:cameras')
        else:
            for field, errors in form.errors.items():  
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = VideoForm()
    return render(request, 'videos/new_camera.html', {'form': form})


