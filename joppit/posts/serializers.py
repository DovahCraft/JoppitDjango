from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    #Create read only fields
    poster = serializers.ReadOnlyField(source='poster.username')
    #poster.id is inheritied from model, so we dont define it explicitly.
    poster_id = serializers.ReadOnlyField(source='poster.id')

    #When someone queries the database for a model, send these fields back
    class Meta:
        #We are serializing a post
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created']