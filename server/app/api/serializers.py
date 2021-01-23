from app.models import *
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email']

class OwnerUserSerializer(serializers.ModelSerializer):
    paypal_email = serializers.CharField(source='owner_detail.paypal_email')
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type', 'paypal_email']
    def create(self, validated_data):
        print(validated_data)
        paypal = validated_data.pop('owner_detail')['paypal_email']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        OwnerUser.objects.create(user=user, paypal_email=paypal)
        return user

class AuthUserSerializer(serializers.ModelSerializer):
    algorand_id = serializers.CharField(source='auth_detail.algorand_id')
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type', 'algorand_id']
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        AuthUser.objects.create(user=user, algorand_id=validated_data['algorand_id'])
        return user

class FunderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type']
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        FunderUser.objects.create(user=user)
        return user

class ForestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = ['id', 'name','description','lat1', 'lat2', 'long1', 'long2', 'owner', 'varified', 'gee_image', 'gee_loss']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"