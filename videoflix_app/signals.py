"""
Signal handlers for video upload, update, and deletion events.
"""

import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_rq import get_queue
from .models import Video
from videoflix_app.tasks import convert720p, convert120p, convert360p, convert1080p

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for video save event.
    Triggers video processing tasks (conversion) when a new video is uploaded or updated.
    """
    print("Video uploaded")

    # Check if the video is newly created or updated
    if created:
        print("New Video created")

        # Ensure the video file exists before starting the conversion tasks
        if instance.video_file:
            video_path = os.path.normpath(instance.video_file.path)
            queue = get_queue("default", autocommit=True)
            queue.enqueue(convert120p, video_path)
            queue.enqueue(convert360p, video_path)
            queue.enqueue(convert720p, video_path)
            queue.enqueue(convert1080p, video_path)
        else:
            print(f"Error: Video file for {instance.title} not found!")
    else:  # If the video is being updated
        print(f"Video {instance.title} updated")

        # Process new video file during update
        if instance.video_file:
            video_path = os.path.normpath(instance.video_file.path)
            queue = get_queue("default", autocommit=True)
            queue.enqueue(convert120p, video_path)
            queue.enqueue(convert360p, video_path)
            queue.enqueue(convert720p, video_path)
            queue.enqueue(convert1080p, video_path)
        else:
            print(f"Error: No video file found for update of {instance.title}")


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Signal handler for video delete event.
    Cleans up video and thumbnail files when a video is deleted.
    """
    print("Video deleted")

    # Delete original video file
    if instance.video_file:
        original_file_path = instance.video_file.path
        if os.path.isfile(original_file_path):
            os.remove(original_file_path)
            print(f"Original file deleted: {original_file_path}")

        # Delete video files for all resolutions
        resolutions = ["120p", "360p", "720p", "1080p"]
        for resolution in resolutions:
            base, extension = os.path.splitext(original_file_path)
            file_path = f"{base}_{resolution}{extension}"
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"{resolution} file deleted: {file_path}")

    # Delete the thumbnail file
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
        print(f"Thumbnail file deleted: {instance.thumbnail.path}")
