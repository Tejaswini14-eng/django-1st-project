from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    type = ( ('Adventure','Adventure'),('RPG','RPG'),('Action','Action'),('Puzzle','Puzzle') )
              
    prod_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=200 , choices=type)
    isAvailable = models.BooleanField(default=True)
    image = models.FileField()


    def __str__(self):
        return self.prod_name

class cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    products = models.ForeignKey(product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1) 

    def __str__(self):
        return self.products.prod_name


class Review(models.Model):
    rate = ((1,1),(2,2),(3,3),(4,4),(5,5))

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    rating = models.IntegerField(choices= rate)
    image = models.FileField(upload_to='reviewimages')
    review = models.CharField(max_length=200)




class orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 
    price = models.FloatField()

 