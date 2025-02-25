from django.shortcuts import render
from yt_dlp import YoutubeDL
from .form import VideoLinkForm
from .models import Video
import os
import shutil
from django.conf import settings
import platform
from django.http import JsonResponse


# Fonction pour récupérer le dossier de téléchargement
def get_downloads_folder():
    """Retourne le chemin du dossier de téléchargements selon le système d'exploitation."""
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:  # Linux et autres
        return os.path.join(os.path.expanduser("~"), "Downloads")

# Fonction pour suivre la progression du téléchargement
def progress_hook(request, d):
    """Fonction de rappel pour suivre la progression du téléchargement."""
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) * 100 / d.get('total_bytes', 1)
        # Sauvegarder la progression dans la session
        request.session['download_progress'] = percent

# Vue principale pour le téléchargement
def download_video(request):
    message = None
    video_url = None
    if request.method == "POST":
        form = VideoLinkForm(request.POST)
        if form.is_valid():
            video_link = form.cleaned_data['video_link']
            output_dir = get_downloads_folder()  # Utiliser le dossier de téléchargements

            # Vérifier les permissions du dossier de téléchargement
            if not os.access(output_dir, os.W_OK):
                message = "Erreur : Impossible d'écrire dans le dossier de téléchargements."
                return render(request, 'index.html', {'form': form, 'message': message})

            # Options de téléchargement pour youtube-dl
            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Utiliser un modèle de sortie
                'format': 'best',  # Télécharger la meilleure qualité disponible
                'progress_hooks': [lambda d: progress_hook(request, d)],  # Passer 'request' à la fonction de rappel
            }

            try:
                # Télécharger la vidéo
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
                    message = "Téléchargement réussi ! Vidéo enregistrée dans le dossier de téléchargements."

                    # Récupérer le chemin du fichier vidéo téléchargé
                    video_files = os.listdir(output_dir)
                    video_files = [f for f in video_files if f.endswith(('mp4', 'webm', 'mkv'))]
                    if video_files:
                        # Copier la vidéo dans le dossier MEDIA_ROOT pour qu'elle soit accessible via /media/
                        video_path = os.path.join(output_dir, video_files[0])
                        media_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
                        os.makedirs(media_dir, exist_ok=True)
                        new_video_path = os.path.join(media_dir, video_files[0])

                        # Copier le fichier vidéo dans le répertoire media
                        shutil.copy(video_path, new_video_path)

                        # Enregistrer la vidéo dans la base de données
                        video = Video.objects.create(
                            title=video_files[0],  # Nom du fichier vidéo comme titre
                            file=os.path.join('videos', video_files[0])  # Chemin relatif vers le fichier
                        )

                        video_url = os.path.join(settings.MEDIA_URL, 'videos', video_files[0])

            except Exception as e:
                message = f"Erreur lors du téléchargement : {e}"

    else:
        form = VideoLinkForm()

    return render(request, 'index.html', {'form': form, 'message': message, 'video_url': video_url})

# Vue pour obtenir la progression du téléchargement
def get_progress(request):
    """Retourne la progression du téléchargement en pourcentage"""
    progress = request.session.get('download_progress', 0)  # Récupérer la progression depuis la session
    return JsonResponse({'percent': progress})



def politique(request):
    return render(request, 'politique.html')
