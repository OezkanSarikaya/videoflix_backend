from django.contrib import admin
from .models import Video, Genre, VideoProgress
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.


class VideoResource(resources.ModelResource):

    class Meta:
        model = Video


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Genre)
admin.site.register(VideoProgress)
