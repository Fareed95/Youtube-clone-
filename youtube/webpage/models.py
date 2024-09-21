from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Channel(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='channel_logo/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnail/',blank=True, null=True)
    views = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')  
    # likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    comments_count = models.IntegerField(default=0, verbose_name='Number of Comments')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.liked_by.count()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.user.username} on {self.video.title}: {self.content[:20]}"  



    
    # likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    # channel = models.ForeignKey('Channel', on_delete=models.CASCADE)

