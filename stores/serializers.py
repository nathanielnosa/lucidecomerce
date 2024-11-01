from rest_framework import serializers
from . models import Product,CartProduct,Cart,Category,Order
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields = '__all__'
        
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartProduct
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['cart', 'amount', 'order_status','subtotal', 'payment_complete', 'ref']

