from django.urls import path
from measurement.views import sensorsCreate, sensorsView, measurmentCreate, SensorDetail, measurmentList

urlpatterns = [
    path('sensor_create/', sensorsCreate.as_view()),
    path('sensors_list/', sensorsView.as_view()),
    path('measurment_create/', measurmentCreate.as_view()),
    path('measurment_list/', measurmentList.as_view()),
    path('measurment_detail/<pk>', SensorDetail.as_view()),
]
