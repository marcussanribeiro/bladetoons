from rest_framework import serializers
from backend.model.model_anime import Anime

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'




class AnimeRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ["id", "titulo", "slug", "imagem"]