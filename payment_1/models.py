from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save


class ShippingAddress(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null= True , blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255 , null= True , blank=True)
    shipping_zipcode = models.CharField(max_length=255 , null= True , blank=True)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f'Shipping Address- {str(self.id)} . {self.user}'
    
# Create a user Profile by default when user signs up 
def create_shipping(sender , instance , created , **kwargs):
    if created:
        user_profile = ShippingAddress(user = instance)
        user_profile.save()
        
# Automate the profile thing
post_save.connect(create_shipping , sender=User)
    
# Create Order Models
class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null= True , blank=True)
    full_name = models.CharField(max_length=200, blank=True , null=True)
    email = models.EmailField(max_length=100)
    Order_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7 , decimal_places=2)
    date_order = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order = {str(self.id)}'
    
# Create Order Items Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , null= True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , null= True)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null= True , blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    
    def __str__(self):
        return f'Order Item = {str(self.id)}'
    
    
