from django.urls import path
from . import views

urlpatterns = [
path('register/',views.Register.as_view()),
path('login/',views.Login.as_view()),
path('logout/',views.Logout.as_view()),
path('dashboard/',views.Dashboard.as_view(),name='dashboard'),
path('update/',views.UpdateProfile.as_view()),
]