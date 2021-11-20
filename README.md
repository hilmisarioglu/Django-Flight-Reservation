python -m venv env
source ./env/Scripts/activate
pip install django
django-admin startproject main .
python manage.py startapp app
python manage.py migrate
python manage.py createsuperuser
pip install dj-rest-auth

from django.contrib import admin
from django.urls import path,include

main.urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
     path('app/', include('app.urls')),
]

INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'dj_rest_auth',
    'app'
)

urlpatterns = [
    ...,
    path('dj-rest-auth/', include('dj_rest_auth.urls'))
]

pip install django-rest-auth

serializers.py

from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
        )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
        style={'input_type': 'password'}
        )
    
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password2'}
        )
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'          
        ]
        
        extra_kwargs = {
            "password" : {"write_only":True},
            "password2" : {"write_only":True}
        }
        
    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password")
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': "Password field didn't match."}
            )
        return data

views.py 
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView

# Create your views here.

class RegisterApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

urls.py
from django.urls import path, include
from .views import RegisterApi

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterApi.as_view()),
]

views.py i degistir
class RegisterApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message" : "User successfully created."
        })

serializers.py
from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
        )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
        )
    
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
        )
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'          
        ]
        
        extra_kwargs = {
            "password" : {"write_only":True},
            "password2" : {"write_only":True}
        }
        
    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': "Password field didn't match."}
            )
        return data
    
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {'id' , 'email' , 'first_name' , 'last_name'}
    
class CustomTokenSerializer(TokenSerializer):
    user = UserTokenSerializer(read_only=True)
    class Meta(TokenSerializer.Meta):
        fields = ('key','user')

settings.py ekle 
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'app.serializers.CustomTokenSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

python manage.py manage.py startapp flight

Settings Installed app ekle 

    'flight',

flight app altina > urls.py


models.py 
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    flightNumber = models.IntegerField()
    operatingAirlines = models.CharField(max_length=25)
    departureCity = models.CharField(max_length=30)
    arrivalCity = models.CharField(max_length=30)
    dateOfDeparture = models.DateField()
    estimatedTimeOfDeparture= models.TimeField()
    
    def __str__(self):
        return f"{self.flightNumber} - {self.departureCity} - {self.arrivalCity}"
    
class Passenger(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=60)
    email = models.EmailField()
    phoneNumber = models.IntegerField()
    updatedDate = models.DateTimeField(auto_now = True)
    createdDate = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.firstName} - {self.lastName}"

class Reservation(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , blank=True , null=True)
    passanger = models.ManyToManyField(Passenger, related_name = 'passenger')  
    flight = models.ForeignKey(Flight, on_delete = models.CASCADE , related_name = 'reservations')
    
    def __str__(self):
        return f"{self.flight}"

python manage.py makemigrations

admin.py ekle 
from django.contrib import admin
from .models import Flight, Passenger, Reservation

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Reservation)

flight > serializers.py ekle
from rest_framework import serializers
from .models import Flight , Passenger , Reservation 

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight 
        fields = '__all__'  


views.py 
from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer
from rest_framework import viewsets

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

main urls.py ekle 
path('flights/', include('flight.urls')),

flight > urls.py git 
from django.urls import path
from .views import FlightView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('flights', FlightView)

urlpatterns = [

]
urlpatterns += router.urls

python manage.py migrate

permissions.py olustur
from rest_framework import permissions

class IsStuffOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

views.py degistir 
from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer
from rest_framework import viewsets
from .permissions import IsStuffOrReadOnly

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStuffOrReadOnly,)

serializers.py ekle 
from rest_framework import serializers
from .models import Flight , Passenger , Reservation 

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight 
        fields = '__all__'  
        
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):
    passanger = PassengerSerializer(many = True, required = False)
    flight_id =serializers.IntegerField()
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(required=False , write_only = True)
    
    class Meta :
        model = Reservation
        fields = {
            'id',
            'flight_id',
            'passenger',
            'user',
            'user_id'
        }
    
    def create(self , validated_data):
        print(validated_data)
        passenger_data = validated_data.pop('passenger')
        print(validated_data)
        validated_data['user_id'] = self.context['request'].user.id
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            reservation.passenger.add(Passenger.objects.create(**passenger))
        reservation.save()
        return reservation
       
        # [
        #     {
        #         },
        #     {},
        # ]
    
views.py ekle 
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


urls.py ekle 
from django.urls import path
from .views import FlightView , ReservationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('flights', FlightView)
router.register('resv', ReservationView)

urlpatterns = [

]

urlpatterns += router.urls

views.py degistir 
from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer , ReservationSerializer
from rest_framework import viewsets , filters
from .permissions import IsStuffOrReadOnly

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStuffOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("departureCity" , "arrivalCity","dateOfDeparture")

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset 
        return queryset.filter(user=self.request.user)

serializer degistir 
from rest_framework import serializers
from .models import Flight , Passenger , Reservation 

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight 
        fields = '__all__'  
        
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):
    passanger = PassengerSerializer(many = True, required = False)
    flight_id =serializers.IntegerField()
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(required=False , write_only = True)
    
    class Meta :
        model = Reservation
        fields = {
            'id',
            'flight_id',
            'passenger',
            'user',
            'user_id'
        }
    
    def create(self , validated_data):
        print(validated_data)
        passenger_data = validated_data.pop('passenger')
        print(validated_data)
        validated_data['user_id'] = self.context['request'].user.id
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            reservation.passenger.add(Passenger.objects.create(**passenger))
        reservation.save()
        return reservation
       
        # [
        #     {
        #         },
        #     {},
        # ]
class StaffFlightSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = (
            'flightNumber',
            'operatingAirlines',
            'departureCity',
            'arrivalCity'
            'dateOfDeparture',
            'estimatedTimeOfDeparture',
            'reservations'
        )
    
views.py degistir
from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer , ReservationSerializer, StaffFlightSerializer
from rest_framework import viewsets , filters
from .permissions import IsStuffOrReadOnly

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

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset 
        return queryset.filter(user=self.request.user)


    