from django.db import models
import string
import random


def code_generator():
    length=6
    character_combination=string.digits+string.ascii_uppercase
    while True:
        code=''.join(random.choices(character_combination,k=length))
        if Room.objects.filter(room_code=code).count()==0:
            break
    return code
# Create your models here.
class Room(models.Model):
    room_code = models.CharField(max_length=8,default='',unique=True)
    room_host=models.CharField(max_length=50,unique=True)
    guest_can_pause=models.BooleanField(null=False,default=False)
    votes_to_skip=models.IntegerField(null=False,default=1)
    created_at=models.DateTimeField(auto_now_add=True)