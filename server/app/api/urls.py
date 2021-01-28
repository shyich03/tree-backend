from django.urls import path, include
from .views import ForestViewSet, UserViewSet, CreateRegionsView, ForestRegionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'forest', ForestViewSet, basename='forests')
router.register(r'user', UserViewSet, basename='users')
# router.register(r'create-regions', CreateRegionsView.as_view(), basename='regions')
# urlpatterns = router.urls 
urlpatterns = [
    path('create-regions', CreateRegionsView.as_view()),
    path('forest-single/<pk>', ForestRegionView.as_view()),
    path('', include(router.urls)),
]
