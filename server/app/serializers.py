# from app.models import *
# from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email']

# class OwnerUserSerializer(UserSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email', 'paypalEmail']

# class AuthUserSerializer(UserSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email', 'algorandID']

# class FunderUserSerializer(UserSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email']
#     def create(self, validated_data):
#         return FunderUser.objects.create(**validated_data)
#         # return instance.save()

# class ForestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['name','lat1', 'lat2', 'long1', 'long2', 'owner', 'varified']