from django import forms

class AnimeImportForm(forms.ModelForm):
    zip_file = forms.FileField(required=False, label="Upload Pasta (ZIP)")
    xml_file = forms.FileField(required=False, label="Arquivo XML")

    class Meta:
        model = Anime
        fields = '__all__'