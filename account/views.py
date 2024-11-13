
from datetime import timedelta , datetime
from django.shortcuts import render, get_object_or_404 
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .serializers import SingUpSerializer, UserSerializer


# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    user = SingUpSerializer(data = data)
    
    if user.is_valid():
        if not User.objects.filter(username = data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password']) ,
            )
            return Response(
                {'details' : 'Your account registered successfuly! '},
                    status = status.HTTP_201_CREATED
                    )
        else : 
            return Response(
                {'eroor' : 'This email already existed! '},
                    status = status.HTTP_400_BAD_REQUEST
                    )
    else :
        return Response(user.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many = False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    user.first_name = data['first_name']
    user.username = data['email']
    user.last_name = data['last_name']
    user.email = data['email']
    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)



def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol = protocol, host = host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email = data['email'])
    token = get_random_string(40)
    expire_date = datetime.now()+ timedelta(minutes = 30)
    user.profile.rest_password_token = token
    user.profile.rest_password_expire = expire_date
    user.profile.save()
    host = get_current_host(request)
    link = "http://localhost:8000/api/rest_password/{token}".format(token = token)
    body = "Your password rest link is : {link}".format(link = link)
    send_mail(
        "Password rest from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response({'details' : 'Password rest sent to {email}'.format(email = [data['email']])})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__rest_password_token = token)
    
    if user.profile.rest_password_expire.replace(tzinfo = None) < datetime.now():
        return Response({'error': 'Token is expired'}, status = status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'password are not same'}, status = status.HTTP_400_BAD_REQUEST)
    user.password = make_password(data['password'])
    user.profile.rest_password_token = ""
    user.profile.rest_password_expire = None
    
    user.profile.save()
    user.save()
    return Response({'details' : 'Password rest done'})
