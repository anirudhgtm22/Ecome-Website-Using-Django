from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    product_desc=models.TextField()
    pub_date=models.DateField()
    category=models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="shop/images",default="")
    
    def __str__(self):
        return self.product_name

class Category(models.Model):
    category_id=models.AutoField
    name=models.CharField(max_length=50)
    desc=models.TextField()
    image=models.ImageField(upload_to="category")
    
    def __str__(self):
        return self.name
class CakeManager(models.Manager):
    def get_cakes_by_id(self, ids):
        return self.filter(id__in=ids)
        
class Cake(models.Model):
    cake_id=models.AutoField
    name = models.CharField(max_length=255)
    description = models.TextField()
    category=models.CharField(max_length=50,default="")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='cakes/images/')
    weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    objects = CakeManager()
    
    def __str__(self):
        return self.name
    


      
class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        customer = self.model(username=username, **extra_fields)
        #customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class Customer(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default = False)
    is_authenticated = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'email']

    def __str__(self):
        return self.username



    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True
    
# class CustomUser(AbstractUser):
#     class Meta:
#         app_label = 'shop'
class OrderManager(models.Manager):
    def get_orders_by_customer(self,customer_id):
        print(customer_id)
        return Order.objects.filter(customer_id=customer_id)    
        
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price=models.IntegerField(max_length=5,default=0)
    address=models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=12,default="")
    order_date = models.DateField(default=datetime.datetime.today)

    objects = OrderManager()
    
    def __str__(self):
        return f"{self.quantity} {self.cake.name}(s) by {self.customer.username}"
    def placeOrder(self):
        self.save()
        