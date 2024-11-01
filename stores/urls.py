from django.urls import path
from . import views
urlpatterns = [
    path('category/',views.CategoryListView.as_view()),
    path('category/<str:pk>/',views.CategoryDetailView.as_view()),

    path('product/',views.ProductListView.as_view()),
    path('product/<str:pk>/',views.ProductDetailView.as_view()),

    path('addtocart/<str:id>/',views.AddToCartView.as_view()),

    path('mycart/',views.MyCartView.as_view()),
    
    path('managecart/<str:id>/',views.ManageCartView.as_view()),

    path('checkout/',views.CheckoutView.as_view()),

    path('payment/<str:id>/',views.PaymentPageView.as_view(), name='payment'),
    
    path('<str:ref>/',views.VerifyPaymentView.as_view()),

]