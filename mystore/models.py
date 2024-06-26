from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    # def __str__(self) -> str:
    #     return self.name
    
    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    # here digital means digital products like software, music. Non-Digital products include shirts, watches etc.
    digital = models.BooleanField(default=False, null=True, blank=True)   

    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)  #refers t0 weather the order is finished ot not
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.id)  
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum([item.quantity for item in orderitems])

        return total_items
    
    @property
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        cart_total = sum([item.get_product_total for item in orderitems])

        return cart_total
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_product_total(self):
        product_total = self.product.price * self.quantity

        return product_total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address
    
