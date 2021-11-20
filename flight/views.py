from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer
from rest_framework import viewsets

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer