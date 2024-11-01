from rest_framework import serializers

from . models import Profile
from django.contrib.auth.models import User
from .utils import send_welcome_message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['fullname','phone','age','profile_pix']

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model= Profile
        fields = ['fullname','username','email','password1','password2','phone','age','profile_pix']

    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password do not match')
        return data
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')

        user = User.objects.create_user(username=username,email=email,password=password)
        profile = Profile.objects.create(
            user=user,
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            age=validated_data['age'],
            profile_pix=validated_data['profile_pix'],
            )
        print(f"Created Profile:{profile}")
        send_welcome_message(user.email,profile.fullname)
        return profile
    


class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    class Meta:
        model=Profile
        fields=['fullname','phone','age','profile_pix','username','email']

    def update(self,instance,validated_data):
        user_data = validated_data.pop('user',{})
        user = instance.user

        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()

        instance.fullname = validated_data.get('fullname',instance.fullname)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.age = validated_data.get('age',instance.age)
        instance.profile_pix = validated_data.get('profile_pix',instance.profile_pix)
        instance.save()

        return instance
            

