# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from rest_framework import permissions
# from app.serializers import *
# from app.models import *
# from django.db import connection
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate

# class UserView(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('username')
#     serializer_class = UserSerializer

# class OwnerUserView(viewsets.ModelViewSet):
#     queryset = OwnerUser.objects.all().order_by('username')
#     serializer_class = OwnerUserSerializer

# class AuthUserView(viewsets.ModelViewSet):
#     queryset = AuthUser.objects.all().order_by('username')
#     serializer_class = AuthUserSerializer

# class FunderUserView(viewsets.ModelViewSet):
#     queryset = FunderUser.objects.all().order_by('username')
#     serializer_class = FunderUserSerializer
#     def get_queryset(self):
#         # user = authenticate(username='john', password='secret')
#         # if user is not None:
#         #     # A backend authenticated the credentials
#         # else:
#         #     # No backend authenticated the credentials
#         return FunderUser.objects.all()
        
#     def create(self, request, *args, **kwargs):
#         if (request.data.type=="register"):
#             # print ("1")
#             s = self.get_serializer(data=request.data)
#             # print ("2")
#             s.is_valid()
#             # print (s.errors,"3")
#             self.perform_create(serializer)
#             # print ("4")
#             headers = self.get_success_headers(serializer.data)
#             # print ("5")
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         elif (request.data.type=="login"):
#             return "0"
#     def perform_create(self, serializer):
#         print (connection.queries[-1])
#         serializer.save()

# class ForestView(viewsets.ModelViewSet):
#     queryset = Forest.objects.all().order_by('name')
#     serializer_class = ForestSerializer
#     permission_classes = [permissions.IsAuthenticated]
# # Create your views here.
