from app.models import *
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OwnerUser
#         fields = ['username', 'password', 'email']

class OwnerUserSerializer(serializers.ModelSerializer):
    paypal_email = serializers.CharField(source='owner_detail.paypal_email')
    organization_name = serializers.CharField(source='owner_detail.organization_name')
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type', 'paypal_email', 'organization_name']
    def create(self, validated_data):
        print(validated_data)
        owner_detail = validated_data.pop('owner_detail')
        paypal = owner_detail['paypal_email']
        organization_name =  owner_detail['organization_name']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        OwnerUser.objects.create(user=user, paypal_email=paypal, organization_name=organization_name)
        return user

class AuthUserSerializer(serializers.ModelSerializer):
    # algorand_id = serializers.CharField(source='auth_detail.algorand_id')
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type']
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        AuthUser.objects.create(user=user)
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
class FunderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunderUser
        fields = "__all__"
class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = "__all__"
class ForestSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='owner.organization_name', required=False)
    funding = FundingSerializer(many=True, required=False)
    class Meta:
        model = Forest
        fields = "__all__"

class RegionSerializer(serializers.ModelSerializer):
    funding = FundingSerializer(many=True, required=False)
    class Meta:
        model = Region
        fields = "__all__"

# class ForestRegionSerializer(serializers.ModelSerializer):
#     regions = RegionSerializer(many=True, read_only=True)
#     class Meta: 
#         model = Region
#         fields = ["regions"]


