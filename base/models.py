from django.db import models
from django.contrib.auth.models import User     # using the built-in user model of django
# Create your models here.

# Room is gonna be a child of a Topic, a Topic can have multiple rooms
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Class of chatroom contains many members and they can chat about specific topic
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)      # if the Topic model is written below the Room then we need to write "Topic" inside the parameters
    name = models.CharField(max_length=200)     # by default 
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)   
    "So, in summary, related_name is used to name the reverse relation from the User model to your model, and it's necessary when you have more than one relation from one model to another. It makes your code more readable and intuitive, and it avoids confusion in Django's ORM about which relation to use."
    updated = models.DateTimeField(auto_now=True)       # every time it is updated.
    created = models.DateTimeField(auto_now_add=True)   # just for initial creation

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return self.name
    

# Messages inside the chatroom
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # deleting messages when the user is deleted.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)    # CASCADE => when room is deleted, its messages will also be deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)       
    created = models.DateTimeField(auto_now_add=True)   # just for initial creation

    def __str__(self):
        return self.body[:50]   # only show first 50 characters in admin panel
    
