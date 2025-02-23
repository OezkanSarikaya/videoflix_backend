"""
Admin configuration for the videoflix_app models.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Video, Genre, VideoProgress


class VideoResource(resources.ModelResource):
    """
    Resource class for importing and exporting Video model data.
    """

    class Meta:
        model = Video


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    """
    Admin panel configuration for Video model with import/export functionality.
    """
    resource_class = VideoResource


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Genre model.
    """
    pass


@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for VideoProgress model.
    """
    pass
