from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,PostSerializer,CommentSerializer,FollowSerializer,LikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile,Post,Comment,Follow,Like
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import generics


# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        try:
            data =request.data
            serializer = RegisterSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': {},
                'message': "Your account has been created"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'data': str(e), 
                'message': "An error occurred"
            }, status=status.HTTP_400_BAD_REQUEST) 
        
class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)
            resopnse = serializer.get_jwt_token(serializer.data)
            return Response(resopnse,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'data': {}, 
                'message': "An error occurred"
            }, status=status.HTTP_400_BAD_REQUEST) 

class ProfileSearch(APIView):
    def get(self,request):
        search = request.GET.get('serach','')
        profile = Profile.objects.filter(
            Q(user__username__icontains=search)
        )       
        page_number = request.GET.get('page', 1)
        paginator = Paginator(profile, 2)
        page_obj = paginator.get_page(page_number)

        serializer = ProfileSerializer(page_obj, many=True)
        return Response({
            'data': serializer.data,
            'message': "Profile fetched successfully"
        }, status=status.HTTP_200_OK)

    

class ProfileView(APIView):
    def get(self,request,pk = None):
        id = pk
        if id is not None:
            stu = Profile.objects.get(pk = pk)
            serializer = ProfileSerializer(stu)
            return Response(serializer.data)
        stu = Profile.objects.all()
        serializer = ProfileSerializer(stu)
        return Response(serializer.data)
         
    def post(self,request):
        data = request.data
        
        serializer = ProfileSerializer(data = data,)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None

    def get(self, request):
        profile = self.get_object()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'msg': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_object()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'msg': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        profile.delete()
        return Response({'msg': 'Profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
class PostView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                post = Post.objects.get(pk=pk)
                if post.user == request.user or Follow.objects.filter(follower=request.user, following=post.user).exists():
                    serializer = PostSerializer(post, context={'request': request})
                    return Response(serializer.data)
                else:
                    return Response({'error': 'You are not allowed to view this post.'}, status=status.HTTP_403_FORBIDDEN)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get current user's and followed users' posts
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        allowed_users = list(followed_users) + [request.user.id]
        posts = Post.objects.filter(user__id__in=allowed_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
        
    def post(self , request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.data)
            
            return Response({'msg': 'Data successfully posted'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self,request ,format = None,pk =None):
        post = Post.objects.get(pk = pk)
        if post.user != request.user:
            return Response({'error': 'You are not allowed to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post successfully updated'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,format = None ,pk =None):
        post = Post.objects.get(pk =pk)
        if post.user != request.user:
            return Response({'error': 'You are not allowed to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    def delete(self,request,pk = None):
      post = Post.objects.get(pk = pk)
      if  post.user != request.user:
        return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
      post.delete()

      return Response({'msg': 'Post deleted successfully'})


class CommentView(APIView):


    def get(self,request,pk = None):
        if pk:
            try:
                comment = Comment.objects.get(pk=pk)
                # Check if the user is allowed to view the comment
                if (
                    comment.user == request.user or
                    comment.post.user == request.user or
                    Follow.objects.filter(follower=request.user, following=comment.post.user).exists()
                ):
                    serializer = CommentSerializer(comment, context={'request': request})
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        # If no pk is provided, show all comments the user is allowed to see
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        allowed_posts = Post.objects.filter(user__in=list(followed_users) + [request.user.id])
        comments = Comment.objects.filter(post__in=allowed_posts)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
      

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            post_id = request.data.get('post')
            try:
                post = Post.objects.get(id=post_id)
                if post.user == request.user or \
                   Follow.objects.filter(follower=request.user, following=post.user).exists():
                    serializer.save(user=request.user)
                    return Response({'msg': 'Comment successfully posted'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'You are not allowed to comment on this post'}, status=status.HTTP_403_FORBIDDEN)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.user != request.user:
                return Response({'error': 'You are not allowed to edit this comment'}, status=status.HTTP_403_FORBIDDEN)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Comment successfully updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.user != request.user:
                return Response({'error': 'You are not allowed to edit this comment'}, status=status.HTTP_403_FORBIDDEN)
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Comment successfully updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.user != request.user:
                return Response({'error': 'You are not allowed to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response({'msg': 'Comment successfully deleted'}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class CommentList(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FollowView(APIView):
   
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        user_follow = User.objects.get(id=user_id)
        follow, created = Follow.objects.get_or_create(follower=request.user,following = user_follow)

        if created:
            return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)
        else:
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        
class FollowingListView(generics.ListAPIView):
    def get(self ,request):
        stu = Follow.objects.all()
        serializer = FollowSerializer(stu,many = True)
        return Response(serializer.data)
        
class FeedView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the IDs of users that the current user is following
        following_user_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        
        # Debug lines
        print("Following User IDs:", list(following_user_ids))
        print(self.request.user)
        
        # Filter posts from the following users
        return Post.objects.filter(user__in=following_user_ids).order_by('-created_at')

class LikeToggleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return Response({'liked': False, 'message': 'Post unliked.'}, status=status.HTTP_200_OK)
        return Response({'liked': True, 'message': 'Post liked.'}, status=status.HTTP_200_OK)

class PostLikesListView(ListAPIView):
    serializer_class = LikeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)

      

 


        




    
         


   




        


         




        
        
