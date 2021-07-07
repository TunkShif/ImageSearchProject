from rest_framework import serializers
from .models import Folder, Image


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['path']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['path']
