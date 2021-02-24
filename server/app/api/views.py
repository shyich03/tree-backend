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
from CertificateIndexer import CertificateIndexer
from CertificateMaker import CertificateMaker
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics, mixins
import numpy as np
import json
import urllib.request
import shutil
import datetime
import hashlib

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
        maps_image_url = request.data.pop('maps_image')
        print(maps_image_url)
        # with urllib.request.urlopen(maps_image_url) as response, open('satelite.png', 'wb') as out_file:
        #     shutil.copyfileobj(response, out_file)
        a=urllib.request.urlretrieve(maps_image_url, filename='files/'+filename+'satelite.png')
        # print(a)
        maps_image = File(open(a[0], 'rb'))
        s = self.get_serializer(data={
            **request.data, 
            'maps_image': maps_image,
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
        gee_image.close()
        gee_loss.close()
        maps_image.close()
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

class CreateRegionsView(generics.CreateAPIView):
    # serializer_class = RegionSerializer
    # queryset = Region.objects.all()
    # Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    authentication_classes = [authentication.TokenAuthentication]
    def create(self, request, *args, **kwargs):
        print("create region")
        image_map = np.array(request.data.get("image_map"))
        print(request.data)
        print(request.data.get("forest_id"))
        forest = Forest.objects.get(id=request.data.get("forest_id"))
        print("pk", forest.pk)
        all_data = request.data.get("data")
        block_size = request.data.get("block_size")
        
        CI = CertificateIndexer()
        for i in range(1,4):
            data = all_data[i-1]
            user = request.user
            bitmap =np.where(image_map==i, 1,0)
            res = (bitmap, 1, ,forest.lat1, forest.long1, datetime.datetime.now())
            # ci.checkMarkingCorrectness(res)
    # add return error if dup
            ci.writeHashValue( res)
            # print(image_map,np.where(image_map==i, 1,0))
            # print(np.where(image_map==i, 1,0).tolist())
            # print(json.dumps(np.where(image_map==i, 1,0).tolist()))
            s = RegionSerializer(data={
                **data, 
                'forest':forest.pk, 
                'block_size': block_size,
                'area': json.dumps(bitmap.tolist()),
                'certificates': json.dumps([])}
            })
            s.is_valid(raise_exception=False)
            print (s.errors,"3")
            s.save()
        return HttpResponse(status=200)

class ForestRegionView(generics.RetrieveAPIView):
    # serializer_class = ForestRegionSerializer
    # queryset = Forest.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    # def get_queryset(self):
    #     Forest.object
    def retrieve(self, request, *args, **kwargs):
        print("get single forest", kwargs.get('pk'))
        pk= kwargs.get('pk')
        region = Region.objects.filter(forest=pk)
        print(region)
        s = RegionSerializer(region, many=True)
        return Response(s.data)

# under production
class FundRegionView(generics.UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    def partial_update(self, request, *args, **kwargs):
        print("funding view")
        pk= kwargs.get('pk')
        region = Region.objects.get(pk=pk)
        forest = Region.forest
        CM = CertificateMaker()
        data=(region.area,1,forest.lat1, forest.long1, datetime.datetime.now())
        h=hashlib.sha256(str(data).encode())
        asset = CM.createCertificate(h, forest.name, "temp url")
        certificates = json.loads(region.certificates)
        certificates.append(asset)
        region.certificates=certificates
        region.save(update_fields=['certificates'])
        return Response({"certificates": certificates})



# under production
class CheckRegionView(generics.RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    def retrieve(self, request, *args, **kwargs):
        print("funding check")
        pk= kwargs.get('pk')
        region = Region.objects.get(pk=pk)
        forest = Region.forest
        s= ForestSerializer(forest)
        print('1',s.data['certificates'])
        print('2', region.certificates)
        CI = CertificateIndexer()
        correct = CI.checkMarkingCorrectness((region.area, 1,forest.lat1, forest.long1,datetime.datetime.now()))
        if correct:
            certificates = json.loads(region.certificates)
            return Response({"certificates": certificates})
