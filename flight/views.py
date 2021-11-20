from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer , ReservationSerializer, StaffFlightSerializer
from rest_framework import viewsets , filters
from .permissions import IsStuffOrReadOnly
from datetime import datetime , date

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStuffOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("departureCity" , "arrivalCity","dateOfDeparture")
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return FlightSerializer
    
    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('Current Time : ' , current_time)
        today = date.today()
        print('Today : ' , today)
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            queryset = Flight.objects.filter(dateOfDeparture__gte= today).filter(estimatedTimeOfDeparture__gt = current_time)
            return queryset

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset 
        return queryset.filter(user=self.request.user)


    