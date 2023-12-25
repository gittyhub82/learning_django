from django import forms
from .models import Shiekh, Book, AudioEpisode

class ShiekhForm(forms.ModelForm):
    class Meta:
        model = Shiekh
        fields = ['name', 'description', 'image']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['description'].required = False
            self.fields['image'].required = False

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shiekh', 'title']


class AudioEpisodeForm(forms.ModelForm):
    class Meta:
        model = AudioEpisode
        fields = ['audio_file']

