from django.urls import path, include
from .views import LiveDataViewSet, LogDataViewSet, add_data, logsInPeriod
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('livedata', LiveDataViewSet, basename='livedata')
router.register('logdata', LogDataViewSet, basename='logdata')

urlpatterns = [
    path('gateway/', include(router.urls)),
    path('gateway/api/add_data/', add_data),
    path('gateway/api/getLogs/inPeriod/', logsInPeriod)

    
]

