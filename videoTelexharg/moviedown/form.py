from django import forms

class VideoLinkForm(forms.Form):
    video_link = forms.URLField(label="Lien de la vidéo", widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Entrez le lien YouTube ou Facebook ici...'
    }))
