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
from django.db.models.query import QuerySet

class ForestViewSet(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Forest.objects.all()
    serializer_class = ForestSerializer
    # def retrieve(self, request, *args, **kwargs):
        
        
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    def get_queryset(self):
        for f,v in  self.request.GET.items():
            print(f,v)

        token =self.request.META.get('HTTP_AUTHORIZATION')
        print("list",token)

        token = token.split()[-1] if token else ""
        print(token)
        
        if token:
            user = Token.objects.get(key=token).user
            if user.user_type == 2 :
                print("ow", user)
                queryset = Forest.objects.filter(owner__user=user)
            else:
                queryset = self.queryset
        else:
            queryset = self.queryset

        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


    def create(self, request, *args, **kwargs):
        data={}
        for key, value in request.data.lists():
            data[key] = value[0]
        # if (request.data.type=="register"):
        print ("1", data)
        c = CertificationInterface()
        print(type(data.get("lat1")))
        filename = c.getArea(
            float(data.get("long1")), 
            float(data.get("long2")),
            float(data.get("lat1")), 
            float(data.get("lat2")))
        gee_image = File(open('files/'+filename+'.png', 'rb'))
        gee_loss = File(open('files/'+filename+'loss.png', 'rb'))
        token = data['user_token']
        user = Token.objects.get(key=token).user
        maps_image_url = data.pop('maps_image')
        print(maps_image_url)
        # with urllib.request.urlopen(maps_image_url) as response, open('satelite.png', 'wb') as out_file:
        #     shutil.copyfileobj(response, out_file)
        a=urllib.request.urlretrieve(maps_image_url, filename='files/'+filename+'satelite.png')
        # print(a)
        maps_image = File(open(a[0], 'rb'))
        s = self.get_serializer(data={
            **data, 
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
class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        if 'funding_goal' in request.data:
            forest = instance.forest
            all_regions = forest.region.all()
            for region in all_regions:
                if region.funding_goal == None:
                    return Response(serializer.data)
            forest.state = Forest.STATE_COMPLETED
            forest.save(update_fields=['state'])
            return Response(serializer.data)

        
        
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
        # integer_fields = ['biodiversity_benefit', 'livelihood_benefit', 'local_benefit', 'carbon_credit_status', 'minised_leakage']
        print("create region",request.user)
        image_map = np.array(request.data.get("image_map"))
        print(request.data)
        print(request.data.get("forest_id"))
        forest = Forest.objects.get(id=request.data.get("forest_id"))
        print("pk", forest.pk)
        all_data = request.data.get("data")
        block_size = request.data.get("block_size")
        
        CI = CertificateIndexer()
        print(all_data)
        for i in range(len(all_data)):
            data = all_data[i]
            user = request.user
            bitmap =np.where(image_map==i+1, 1,0)
            res = (bitmap, 1, forest.lat1, forest.long1, datetime.datetime.now())
            # ci.checkMarkingCorrectness(res)
    # todo: add return error if dup
            CI.writeHashValue( res)
            print(data)
            s = RegionSerializer(data={
                **data, 
                'forest':forest.pk, 
                'block_size': block_size,
                'area': json.dumps(bitmap.tolist()),
                'certificates': json.dumps([])
            })
            s.is_valid(raise_exception=False)
            print (s.errors,"3")
            s.save()
        forest.state=forest.STATE_VARIFIED
        forest.save(update_fields=['state'])
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
        forest = region.forest
        user = request.user
        print(user)
        s = FundingSerializer
        CM = CertificateMaker()
        data=(region.area,1,forest.lat1, forest.long1, datetime.datetime.now())
        h=hashlib.sha256(str(data).encode())
        asset = CM.createCertificate(h, forest.name, "temp url")
        certificates = region.certificates
        print(certificates)
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
