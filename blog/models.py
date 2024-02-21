from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='postImage',null=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    tag = models.ManyToManyField('Tag',related_name='post_tags')
    slug = models.SlugField(null=True)
    author = models.ForeignKey(User, related_name='post_author',on_delete=models.CASCADE,null=True)
    
class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email  = models.EmailField(max_length=100)
    website = models.CharField(max_length=200,null=True)
    post = models.ForeignKey(Post,related_name='commentPost',on_delete=models.DO_NOTHING,null=True)
    author = models.ForeignKey(User,related_name='author',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name='commentReply',on_delete=models.DO_NOTHING,null=True)
    
class Subscripe(models.Model):
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(Tag, self).save(*args, **kwargs) # Call the real save() method
       
    def __str__(self):
        return self.name
    
       
class Profile(models.Model):
    profile = models.OneToOneField(User, related_name="profileUser",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='userImage',null=True)
    bio = models.CharField(max_length=150,null=True)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.profile.username)
       super(Profile, self).save(*args, **kwargs) # Call the real save() method
    
@receiver(post_save, sender=User)
def saveprofile(sender,instance,created,**kwargs):
    user = instance
    if created:
        profile = Profile(profile=user)
        profile.save()
        
class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    about = models.TextField()