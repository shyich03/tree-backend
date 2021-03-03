from django.urls import path, include
from .views import RegionViewSet, ForestViewSet, UserViewSet, CreateRegionsView, ForestRegionView, FundRegionView, CheckRegionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'forest', ForestViewSet, basename='forests')
router.register(r'user', UserViewSet, basename='users')
router.register(r'region', RegionViewSet, basename='regions')
# router.register(r'create-regions', CreateRegionsView.as_view(), basename='regions')
# urlpatterns = router.urls 
urlpatterns = [
    path('create-regions', CreateRegionsView.as_view()),
    path('forest-single/<pk>', ForestRegionView.as_view()),
    path('fund-region/<pk>', FundRegionView.as_view()),
    path('check-region/<pk>', CheckRegionView.as_view()),
    path('', include(router.urls)),
]
