from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile,Post,Comment,Follow,Like


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        if User.objects.filter(username = data['username'].lower()).exists():
            raise serializers.ValidationError("Username is taken")
        return data
    
    def create(self,validate_data):
        username = validate_data['username'].lower()
        user = User.objects.create(
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name'],
            username = username
        )
        user.set_password(validate_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField()

    def validate(self ,data):
       
       if not User.objects.filter(username = data['user_name']).exists():
           raise serializers.ValidationError("User not found")
       return data
    
    def get_jwt_token(self,data):
        user = authenticate(username=data['user_name'],password = data['password'])
        if not user:
            return {'message': 'Invalid credentials', 'data': {}}
        refresh = RefreshToken.for_user(user)
        return {
         'message': 'Login successfully',
        'data': {
           'refresh': str(refresh),
           'access': str(refresh.access_token),
            }
        }
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'id_user', 'bio', 'img', 'address']

    def create(self, validated_data):
        # Create a new instance of the Profile model using the validated data
        return Profile.objects.create(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user','captions','created_at','post_img','likes_count','is_liked_by_user']
        read_only_fields = ['user']
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'captions', 'created_at']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        # Create and return a new Comment instance, given the validated data
        return Comment.objects.create(**validated_data)
    
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower','following','created_at']

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Like
        fields = ['user', 'username', 'created_at']

    