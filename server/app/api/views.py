from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.files import File
import sys
import util
sys.path.insert(0, util.path)
from CertificationInterface import CertificationInterface
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import authentication, permissions

class ForestViewSet(ModelViewSet):
    queryset = Forest.objects.all()
    serializer_class = ForestSerializer
    # def retrieve(self, request, *args, **kwargs):
        
        
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        # if (request.data.type=="register"):
        print ("1", request.data)
        c = CertificationInterface()
        print(type(request.data.get("lat1")))
        filename = c.getArea(
            request.data.get("long1"), 
            request.data.get("long2"),
            request.data.get("lat1"), 
            request.data.get("lat2"))
        gee_image = File(open('files/'+filename+'.png', 'rb'))
        gee_loss = File(open('files/'+filename+'loss.png', 'rb'))
        token = request.data['user_token']
        user = Token.objects.get(key=token).user
        print("")
        s = self.get_serializer(data={
            **request.data, 
            'gee_image': gee_image,
            'gee_loss': gee_loss,
            'owner': user})
        print ("2")
        s.is_valid(raise_exception=False)
        print (s.errors,"3")
        self.perform_create(s)
        print ("4")
        headers = self.get_success_headers(s.data)
        print ("5")
        return Response(s.data)
        # elif (request.data.type=="login"):
        #     return "0"

class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(user_type=1)
    # queryset = User.objects.all()
    # serializer_class = FunderUserSerializer
    def get_serializer_class(self):
        if self.request.data.get('type') == 'funder':
            print("return f se")
            return FunderUserSerializer
        elif self.request.data.get('type') == 'owner':
            print("return o se")
            return OwnerUserSerializer
        else:
            print("return a se")
            return AuthUserSerializer

    def create(self, request, *args, **kwargs):
        # if (request.data.type=="register"):
        print ("1", request.data)
        type_switch = {'funder':1, 'owner':2, 'auth':3}
        s = self.get_serializer(data={**request.data, 'user_type': type_switch.get(request.data['type'])})
        print ("2")
        s.is_valid(raise_exception=False)
        print (s.errors,"3")
        self.perform_create(s)
        print ("4")
        headers = self.get_success_headers(s.data)
        print ("5")
        return HttpResponse(status=200)
        # elif (request.data.type=="login"):
        #     return "0"

class CreateRegionsView(ViewSet):
    # Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    # authentication_classes = [authentication.TokenAuthentication]
    def Create(self, request, format=None):
        imageMap = request.data.get("image_map")
        forest = Forest.object.get(id=request.data.get("forest_id"))
        for i in range(1,4):
            data = request.data.get(str(i))
            user = request.user
            s = RegionSerializer(data={**data, 'forest':forest})
            s.is_valid(raise_exception=False)
            s.save()
        return HttpResponse(status=200)





