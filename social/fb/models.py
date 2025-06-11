from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,max_length=90)
    id_user = models.IntegerField(primary_key=True,default=0)
    bio = models.TextField(blank = True,default='')
    img = models.ImageField(upload_to='profile_image/',default='blank-profile-picture.png')
    address = models.CharField(max_length=90,blank=True,default='')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    captions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_img = models.ImageField(upload_to='post_image',default='blank-profile-picture.png' )
    # def __str__(self):
    #     return f'Post by {self.user.username}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    captions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.id}'
    
class Follow(models.Model):
    follower =  models.ForeignKey(User,related_name="following",on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name="followers",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.id}"

    