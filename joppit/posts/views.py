from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from rest_framework.exceptions import ValidationError

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


#Deleting a post using the RetrieveDestroyAPIView
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    #Make queryset, what do we want from the database?
    queryset = Post.objects.all()
    #Create a serializer class object to convert Post object to JSON
    serializer_class = PostSerializer
    #Set permissions for who can post, must be authenticated to POST request, but can GET request as it is readonly for non authed users. 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        #Query to see if the current user has access to this post to only delete their own.
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        #If we have our own post to delete, do so.
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        #Otherwise no post exists that belongs to the user for deletion.
        else:
            raise ValidationError("You can't delete another brotha's post mang!")

    

#Use a mixin extension to destroy votes as well.
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    #ONly authed users can vote on posts
    permissions_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        #Current upvoting user
        user = self.request.user
        #Get the specific posts based on passed primary key to kwargs (the endpoint link)
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    #Define what the post is to be upvoted and then add a vote.
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post!')
        #This is the default, bad in this case bc poster_id is required.
        #serializer.save()
        #Voter is currently authed user, post is post with id passed to kwargs
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    #Allows user to delete their upvotes
    def delete(self, request, *args, **kwargs):
        #Check if exists in db
        if self.get_queryset().exists():
            #Delete the vote via the queryset.
            self.get_queryset().delete()
            #Return the no content, we removed it OK.
            return Response(status=status.HTTP_204_NO_CONTENT)
        #No matching votes found, return an error message to the user.
        else:
            raise ValidationError("You never voted for this post...GAH!")