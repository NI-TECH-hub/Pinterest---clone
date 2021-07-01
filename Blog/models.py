from django.db import models
# from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.constraints import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class AddPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='Blog/')
    published = models.DateTimeField(auto_now_add=True)
    likes= models.ManyToManyField(User,related_name='likes',blank=True)
    dislikes = models.ManyToManyField(User,related_name='dislikes',blank=True)

    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self):
        return self.title

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone = models.IntegerField(null=True)
    birth_date = models.DateField(null=True,blank=True)
    photo = models.ImageField(upload_to = 'profile/')


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile.objects.create(user = instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()



class comment(models.Model):
    post = models.ForeignKey(AddPost,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

