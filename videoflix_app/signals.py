import os
from django.conf import settings
from videoflix_app.tasks import convert720p
from .models import Video
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import django_rq
# from django_rq import enqueue


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde hochgeladen')

    # Überprüfen, ob das Video beim ersten Speichern (created) oder beim Update gespeichert wird
    if created:
        print('New Video created')

        # Prüfen, ob das Video eine Datei enthält, bevor der Pfad gesetzt wird
        if instance.video_file:
            video_path = os.path.normpath(instance.video_file.path)
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert720p, video_path)
        else:
            print(f"Fehler: Die Video-Datei für {instance.title} ist nicht vorhanden!")

    else:  # Wenn das Video ein Update ist
        print(f"Video {instance.title} wurde aktualisiert")

        # Wenn beim Update ein neues Video hochgeladen wurde
        if instance.video_file:
            video_path = os.path.normpath(instance.video_file.path)
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert720p, video_path)
        else:
            print(f"Fehler: Keine Video-Datei gefunden für das Update von {instance.title}")


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    print('Video wird gelöscht')

    # Originaldatei löschen
    if instance.video_file:
        original_file_path = instance.video_file.path
        if os.path.isfile(original_file_path):
            os.remove(original_file_path)
            print(f'Originaldatei gelöscht: {original_file_path}')
        
        # Datei mit Endung "_720p" löschen
        base, extension = os.path.splitext(original_file_path)
        file_720p_path = f"{base}_720p{extension}"
        if os.path.isfile(file_720p_path):
            os.remove(file_720p_path)
            print(f'720p Datei gelöscht: {file_720p_path}')




