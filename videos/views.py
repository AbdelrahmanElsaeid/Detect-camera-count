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
from .utils import process_videos  
from django.utils import timezone






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
                # Process frames using your AI model

                process_videos(q)

                # update conut in status 
                thumbnails = q.thumbnails.all()
                results = [int(thumbnail.result)  for thumbnail in thumbnails]
        
                # Calculate the sum of the results
                total_result = sum(results)

                camera_status, created = CameraStatus.objects.get_or_create(
                    video=q,
                    title=q.title,
                    count=total_result,
                    date=timezone.now(),
                )

                if total_result > q.num_people_limit:
                    messages.error(request, f'The number of people ({total_result}) is more than the permissible limit ({q.num_people_limit})')
            return redirect('videos:status')
            
            
                                        
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







@login_required
def camera_detail(request, id):
    video = get_object_or_404(Video, id=id)
    thumbnails = video.thumbnails.all()

    timestamps = [thumbnail.timestamp for thumbnail in thumbnails]
    results = [thumbnail.result for thumbnail in thumbnails]

    context = {
        'timestamps': timestamps,
        'results': results,
    }

    return render(request, 'videos/camera_detail.html', context)



