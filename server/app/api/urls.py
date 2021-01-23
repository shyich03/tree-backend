from django.urls import path
from .views import ForestViewSet, UserViewSet, CreateRegionsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'forest', ForestViewSet, basename='forests')
router.register(r'user', UserViewSet, basename='users')
router.register(r'create-regions', CreateRegionsView, basename='regions')
urlpatterns = router.urls