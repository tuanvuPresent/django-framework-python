from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.timesheet import views

router = routers.SimpleRouter()
router.register('timesheet', views.TimeSheetAPIView, basename='timesheet')
urlpatterns = [
    url('', include(router.urls)),
]
