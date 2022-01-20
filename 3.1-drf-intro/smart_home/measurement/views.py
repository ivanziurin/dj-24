# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer

from measurement.models import Sensor, Measurement



class sensorsCreate(APIView):
        def post(self, request):
                ser = SensorSerializer(data=request.data)
                ser.is_valid(raise_exception=True)
                ser.save()
                return Response({'status': 'Ok'})


class sensorsView(APIView):
        def get(self, request):
                sensors = Sensor.objects.all()
                ser = SensorSerializer(sensors, many=True)
                return Response(ser.data)


class measurmentCreate(APIView):
        def post(self, request):
                ser = MeasurementSerializer(data=request.data)
                ser.is_valid(raise_exception=True)
                ser.save()
                return Response({'status': 'Ok'})


class measurmentList(generics.ListCreateAPIView):
        queryset = Measurement.objects.all()
        serializer_class = MeasurementSerializer

        def sensor_create(self, serializer):
                serializer.save()



class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = Sensor.objects.all()
        serializer_class = SensorDetailSerializer