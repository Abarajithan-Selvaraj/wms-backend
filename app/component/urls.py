"""
URL mappings for the component APIs.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter # type: ignore

from component import views


router = DefaultRouter()
router.register('component', views.ComponentViewSet)

app_name = 'component'

urlpatterns = [
    path('', include(router.urls)),
]
