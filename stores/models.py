from django.db import models
from users.models import Profile

from . paystack import Paystack
import uuid
import secrets


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category')
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
 
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main = models.ImageField(upload_to='products')
    photo1 = models.ImageField(upload_to='products')
    photo2 = models.ImageField(upload_to='products')
    photo3 = models.ImageField(upload_to='products')
    photo4 = models.ImageField(upload_to='products')
    photo5 = models.ImageField(upload_to='products')
    delivery_date = models.CharField(max_length=50)
    product_id = models.UUIDField(unique=True, default=uuid.uuid4)
    is_available = models.BooleanField(default=True)
    in_stock = models.IntegerField()
    rating = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = uuid.uuid4()
        super().save(*args,**kwargs)

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart - {self.total}'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart product - {self.cart.id}'

ORDER_STATUS=(
    ('Pending','Pending'),
    ('Complete','Complete'),
    ('Cancel','Cancel'),
)
PAYMENT_METHOD=(
    ('paystack','paystack'),
    ('card','card'),
    ('transfer','transfer'),
)
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    order_by = models.CharField(max_length=50)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subtotal = models.PositiveBigIntegerField()
    amount = models.PositiveBigIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='paystack')
    payment_complete = models.BooleanField(default=False, null=True,blank=True)
    ref = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f'{self.amount}- {str(self.id)}'
    
    # generate ref
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)
    
    # amount
    def amount_value(self)->int:
        return self.amount * 100
    
    # verify payment
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref)

        if status and result.get('status') == 'success':
            # Ensure the amount matches
            if result['amount'] / 100 == self.amount:
                self.payment_complete = True
                self.save()
                return True
        
        # If payment was not successful, return False
        return False