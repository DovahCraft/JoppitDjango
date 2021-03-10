from rest_framework import serializers
from .models import Post, Vote

class PostSerializer(serializers.ModelSerializer):
    #Create read only fields
    poster = serializers.ReadOnlyField(source='poster.username')
    #poster.id is inheritied from model, so we dont define it explicitly.
    poster_id = serializers.ReadOnlyField(source='poster.id')
    #Add a field for all the votes for a post
    votes = serializers.SerializerMethodField()

    #When someone queries the database for a model, send these fields back
    class Meta:
        #We are serializing a post
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'votes']
    #NOTE: Get method must have the same name as the class member variable.
    #get_<VARNAME>
    #Ex: get_votesss would not work, but get_votes does.
    def get_votes(self, post):
        #Filter (i.e. query) the vote objects based on the post field that contains the passed in post obj.
        return Vote.objects.filter(post=post).count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        #We are serializing a vote
        model = Vote
        fields = ['id']
