from django.shortcuts import render

# Create your views here.

import os
from django.conf import settings
from yt_dlp import YoutubeDL
from django.shortcuts import render
from .form import VideoLinkForm
import platform

def politique(request):
    return render(request, 'politique.html')
def get_downloads_folder(): 
    
    """Retourne le chemin du dossier de téléchargements selon le système d'exploitation."""
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:  # Linux et autres
        return os.path.join(os.path.expanduser("~"), "Downloads")

def download_video(request):
    message = None
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
            }

            try:
                # Télécharger la vidéo
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
                    message = "Téléchargement réussi ! Vidéo enregistrée dans le dossier de téléchargements."
            except Exception as e:
                # En cas d'erreur, afficher le message
                message = f"Erreur lors du téléchargement : {e}"

    else:
        form = VideoLinkForm()

    # Retourner la réponse à l'utilisateur
    return render(request, 'index.html', {'form': form, 'message': message})

