
from django import forms
from .models import Video

# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ['title', 'video']





class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video', 'html_code', 'cam_url','num_people_limit']



class VideoActivationForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['active']
