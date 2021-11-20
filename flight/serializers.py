from rest_framework import serializers
from .models import Flight , Passenger , Reservation 

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight 
        fields = '__all__'  