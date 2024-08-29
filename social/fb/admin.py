from django.contrib import admin
from .models import Profile,Post,Comment,Follow

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','id_user','bio','img','address')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','captions','created_at','post_img','likes']
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','user','captions','created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower','following','created_at']