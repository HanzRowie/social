from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,PostSerializer,CommentSerializer,FollowSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile,Post,Comment,Follow
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
    
    def put(self,request,format = None,pk = None):

        stu = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(stu,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Updated'})
        return Response(serializer.errors)
    
    def patch(self,request,format = None,pk=None):
        
        stu = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(stu,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Updated'})
        return Response(serializer.errors)
    
    def delete(self,request,pk = None):
        pk = pk
        stu = Profile.objects.get(pk=pk)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
class PostView(APIView):
    def get(self,request,pk = None):
        id = pk
        if id is not None:
            stu = Post.objects.get(pk = pk)
            serializer = PostSerializer(stu)
            return Response(serializer.data)
        stu = Post.objects.all()
        serializer = PostSerializer(stu)
        return Response(serializer.data)
    
    def post(self , request):
        data = request.data
        serializer = PostSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data  successfully Posted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request ,format = None,pk =None):
        id = pk
        stu = Post.objects.get(pk = pk)
        serializer = PostSerializer(stu,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Successfully Updated'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,format = None ,pk =None):
        id = pk
        stu = Post.objects.get(pk = pk)
        serializer = PostSerializer(stu,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Post Successfully Updated"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk = None):
        id = pk
        stu = Post.objects.get(pk = pk)
        stu.delete()


class CommentView(APIView):
    def get(self,request,pk = None):
        id = pk
        if id is not None:
            stu = Comment.objects.get(id =pk)
            serializer = CommentSerializer(stu,data = request.data)
            return Response(serializer.data)
        stu = Comment.objects.all()
        serializer =CommentSerializer(stu,data = request.data)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Comment  successfully Posted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk = None):
        id = pk
        stu = Comment.objects.get(pk=pk)
        serializer =  CommentSerializer(stu,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Comment Successfully Updated'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk = None):
        id = pk
        stu = Comment.objects.get(id=pk)
        serializer = CommentSerializer(stu,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Comment Updated Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk =None):
        id = pk
        stu = Comment.objects.get(pk = pk)
        stu.delete()

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

      

 


        




    
         


   




        


         




        
        
