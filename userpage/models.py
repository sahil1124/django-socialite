from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption=models.CharField(max_length=200)
    image=models.ImageField(upload_to='Post')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.date.date())

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    userImage=models.ImageField(upload_to='Profiles',default='default/profile.png')
    bio=models.CharField(max_length=200,blank=True)
    connection=models.CharField(max_length=100,blank=True)
    follower=models.IntegerField(default=0)
    following=models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class  Like(models.Model):
    user=models.ManyToManyField(User,related_name="likingUser")
    post=models.OneToOneField(Post,on_delete=models.CASCADE)


    @classmethod
    def like(cls,post,liking_user):
        obj , create=cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    @classmethod
    def dislike(cls,post,disliking_user):
        obj , create=cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)

    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE,default="",null=True)
    user=models.CharField(max_length=20)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']


    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user)


class Following(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    followed=models.ManyToManyField(User,related_name="followed")
    follower=models.ManyToManyField(User,related_name="follower")


    @classmethod
    def follow(cls,user,another_account):
        obj,create = cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        print("followed")

    @classmethod
    def unfollow(cls,user,another_account):
        obj,create = cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)
        print("unfollow")

    def __str__(self):
        return str(self.user)
