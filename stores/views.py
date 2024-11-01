import requests
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

from . serializers import *
from . models import *

# :::::::: CATEGORY  :::::::::
class CategoryListView(APIView):
    parser_classes = [MultiPartParser, FormParser,JSONParser]  # Add parsers for handling files
    # GET all category
    def get(self,request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # create category
    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class CategoryDetailView(APIView):
    # GET SINGLE
    def get(self, request, pk):
        try:
            category = get_object_or_404(Category,pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # UPDATE
    def put(self, request,pk):
        try:
            category = get_object_or_404(Category,pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Delete
    def delete(self, request,pk):
        try:
            category = get_object_or_404(Category,pk=pk)
            category.delete()
            return Response({"Message":"Category deleted successful"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# :::::::: PRODUCT  :::::::::
class ProductListView(APIView):
    parser_classes = [MultiPartParser, FormParser,JSONParser]  # Add parsers for handling files
    # GET all product
    def get(self,request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # create product
    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductDetailView(APIView):
    # GET SINGLE
    def get(self, request, pk):
        try:
            product = get_object_or_404(Product,pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # UPDATE
    def put(self, request,pk):
        try:
            product = get_object_or_404(Product,pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Delete
    def delete(self, request,pk):
        try:
            product = get_object_or_404(Product,pk=pk)
            product.delete()
            return Response({"Message":"product deleted successful"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::::::: ADD CART  :::::::::
class AddToCartView(APIView):
    def post(self, request, id):
        try:
            # Fetch the product or return 404 if it doesn't exist
            product = get_object_or_404(Product, id=id)
            # Get the cart ID from the session
            cart_id = request.session.get('cart_id', None)
            
            # Start a transaction to ensure atomic updates
            with transaction.atomic():
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()
                    
                    # If cart is None, it means the cart ID is invalid
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id
                    
                    # Check if the product is already in the cart
                    this_product_in_cart = cart.cartproduct_set.filter(product=product)
                    
                    # assigning cart to a user 
                    if request.user.is_authenticated and hasattr(request.user,'profile'):
                        cart.profile = request.user.profile
                        cart.save()
                    if this_product_in_cart.exists():
                        # If the product exists in the cart, update its quantity and subtotal
                        cartproduct = this_product_in_cart.last()  # Get the existing cartproduct
                        cartproduct.quantity += 1
                        cartproduct.subtotal += product.price
                        cartproduct.save()
                        
                        # Update the cart's total
                        cart.total += product.price
                        cart.save()
                        
                        return Response({'Message': 'Item quantity increased in cart'}, status=status.HTTP_200_OK)
                    else:
                        # Add the new product to the cart
                        cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                        cartproduct.save()
                        # Update the cart's total
                        cart.total += product.price
                        cart.save()
                        
                        return Response({'Message': 'New item added to cart'}, status=status.HTTP_200_OK)
                
                else:
                    # Create a new cart and add the first product to it
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                    cartproduct.save()
                    # Update the cart's total
                    cart.total += product.price
                    cart.save()
                    
                    return Response({'Message': 'Cart created and item added to cart'}, status=status.HTTP_201_CREATED)
        
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::::::: MY CART  :::::::::
class MyCartView(APIView):
    def get(self,request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart,id=cart_id)
                # assigning cart to a user 
                if request.user.is_authenticated and hasattr(request.user,'profile'):
                    cart.profile = request.user.profile
                    cart.save()
                serializer = CartSerializer(cart)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error":"cart not found"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::::::: MANAGE CART  :::::::::
class ManageCartView(APIView):
    def post(self,request,id):
        action = request.data.get('action')
        try:
            cart_obj = get_object_or_404(CartProduct,id=id)
            cart = cart_obj.cart
            if action == "inc":
                cart_obj.quantity +=1
                cart_obj.subtotal += cart_obj.product.price
                cart_obj.save()
                cart.total+= cart_obj.product.price
                cart.save()
                return Response({'Message':'Item increase in cart quantity'},status=status.HTTP_200_OK)
            
            elif action == "dcr":
                if cart_obj.quantity > 0:
                    cart_obj.quantity -= 1
                    cart_obj.subtotal -= cart_obj.product.price
                    cart_obj.save()
                    cart.total-= cart_obj.product.price
                    cart.save()

                    if cart_obj.quantity == 0:
                        cart_obj.delete()
                    return Response({'Message':'Item decrease in cart quantity'},status=status.HTTP_200_OK)
                else:
                    return Response({'Message':'Quantity can not be less than zero'},status=status.HTTP_404_NOT_FOUND)
            
            elif action == "rmv":
                cart.total -= cart_obj.subtotal
                cart.save()
                cart_obj.delete()
                return Response({'Message':'Product removed from cart'},status=status.HTTP_200_OK)
            
            else:
                return Response({'Message':'Invalid selection'},status=status.HTTP_400_BAD_REQUEST)
            


        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::::::: CHECKOUT  :::::::::
@method_decorator(csrf_exempt, name='dispatch')
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            return Response({"error": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_obj = get_object_or_404(Cart,id=cart_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CheckoutSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save(
                cart=cart_obj,
                amount=cart_obj.total,
                subtotal=cart_obj.total,
                order_status='pending'
            )
            del request.session['cart_id']
            
            if order.payment_method == 'paystack':
                # Return payment URL or redirect based on API/Frontend needs
                payment_url = reverse('payment', args=[order.id])
                return Response({"redirect_url": payment_url}, status=status.HTTP_302_FOUND)
                
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# :::::::: PAYMENT  :::::::::    
class PaymentPageView(APIView):
    def get(self, request, id):
        # Retrieve the order by ID
        try:
            order = get_object_or_404(Order,id=id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Return the order details and Paystack public key
        return Response({
            'order': order.id,
            'total': order.amount,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        }, status=status.HTTP_200_OK)

# :::::::: VERIFY PAYMENT  :::::::::    
class VerifyPaymentView(APIView):
    def get(self, request, ref):
        try:
            # Query the Order model with the provided reference
            order = get_object_or_404(Order,ref=ref)
            
            # Verify with Paystack (or another payment provider)
            url = f"https://api.paystack.co/transaction/verify/{ref}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            # Check if verification was successful
            if response_data["status"] and response_data["data"]["status"] == "success":
                order.payment_complete = True
                order.save()
                return Response({"message": "Payment verified successfully"}, status=200)
            else:
                return Response({"error": "Payment verification failed"}, status=400)
        
        except Order.DoesNotExist:
            return Response({"error": "Invalid payment reference"}, status=404)
        except Exception as e:
            return Response({"error": "An error occurred while verifying payment"}, status=500)