from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from django.views.static import serve
# from app import views

# router = routers.DefaultRouter()
# router.register(r'user', views.UserView)
# router.register(r'funder', views.FunderUserView)

urlpatterns = [
    path('api/', include('app.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^files/(?P<path>.*)$', serve, {'document_root': 'files/',})
]
