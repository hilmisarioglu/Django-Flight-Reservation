from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer , ReservationSerializer
from rest_framework import viewsets
from .permissions import IsStuffOrReadOnly

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStuffOrReadOnly,)

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer