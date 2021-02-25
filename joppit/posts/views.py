from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
# Create your views here.

#This class will list out all the posts, extends a generic ListAPIView
# to list information/post objects.
class PostList(generics.ListCreateAPIView):
    #Make queryset, what do we want from the database?
    queryset = Post.objects.all()
    #Create a serializer class object to convert Post object to JSON
    serializer_class = PostSerializer
    #Set permissions for who can post, must be authenticated to POST request, but can GET request as it is readonly for non authed users. 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #Define what the post can be saved as, the process to save it
    def perform_create(self, serializer):
        #This is the default, bad in this case bc poster_id is required.
        #serializer.save()
        serializer.save(poster=self.request.user)