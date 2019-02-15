from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ratings=[(1,1),(2,2),(3,3),(4,4),(5,5)]
class movies(models.Model):

    description = models.TextField()
    genre = models.CharField(max_length=100)
    imdb_url = models.CharField(max_length=100)
    img_url=models.CharField(max_length=500)
    movie_id=models.IntegerField(blank=True, null=True)
    title=models.CharField(max_length=100)
    users_rating=models.CharField(max_length=100)
    year=models.CharField(max_length=100)

    class Meta:
       managed = True
       db_table = 'movies'

class rating(models.Model):

    account=models.ForeignKey(User,default=0,on_delete=models.DO_NOTHING)
    movie_id=models.IntegerField(null=True)
    rating=models.IntegerField(choices=ratings,null=True)
    

    class Meta:
        managed=True
        db_table='rating'

    