from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'', views.OrderViewSet, basename='')
urlpatterns = [
    path('khalti-initiate/',views.InitiateKhaltiPayment.as_view(),name="initiate"),
   path('khalti-verify/',views.VerifyKhalti.as_view(),name="verify"),
    path('', include(router.urls)),
]