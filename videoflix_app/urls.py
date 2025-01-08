# videoflix_app/urls.py
from django.urls import path
from .views import VideoListView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video_list'),  # Liste der Videos
]
