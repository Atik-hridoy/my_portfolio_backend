from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'year', 'technologies', 
                  'live_url', 'github_url', 'image_url', 'featured', 
                  'category', 'created_at', 'updated_at']
