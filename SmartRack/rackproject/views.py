from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from .models import Rack, Rack_User, User, History
from .serializers import RackSerializer, Rack_UserSerializer, UserSerializer, HistorySerializer
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests  # For communicating with Arduino hardware
import logging
from .consumers import ESP32Consumer
# Configure logging
logger = logging.getLogger(__name__)

# Constants for Arduino communication
esp_socket  = None
    
@api_view(['GET'])
def lock_rack_page(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return Response({'message': 'User not authenticated'}, status=401)
    
    page_url = ""
    response_data = {
        "message": "QR code scanner page retrieved successfully",
        "page_url": page_url,
    }
    return Response(response_data)

# QR Code Scanning and Locking Logic
@api_view(['POST'])
def loc(request):
        global esp_socket
        data = request.data
        rack_id = data.get('rack_id')
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            return Response({'message': 'User not authenticated'}, status=401)

        if not rack_id:
            return Response({'message': 'Rack ID is required'}, status=400)

        try:
            user= User.objects.get(id=user_id)
            rack = Rack.objects.get(id=rack_id)
            if rack.status == 'locked':
                return Response({'message': 'Rack is already locked. Please choose another.'}, status=400)

            # Signal Arduino to lock the rack
            if esp_socket:
                ESP32Consumer.esp_socket.send(text_data = {"action":"lock", "rackId": 3})

            # Update rack status and timestamps
            rack.status = 'locked'
            rack.locked_at = timezone.now()
            rack.save()

            # Create a record in Rack_User
            rack_user_data = {
                'user': user.id,
                'rack': rack.id,
            }
            serializer = Rack_UserSerializer(data=rack_user_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Rack locked successfully'})
            else:
                return Response(serializer.errors, status=400)

        except Rack.DoesNotExist:
            logger.error(f"Rack with ID {rack_id} not found")
            return Response({'message': 'Rack not found'}, status=404)


@api_view(['GET'])
def unlock_page(request):
   
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return Response({'message': 'User not authenticated'}, status=401)

    page_url = ""

    # Respond with the URL and optional user details
    return Response({
        "message": "Unlock page URL retrieved successfully",
        "unlock_page_url": page_url,
        "user_id": user_id  # Pass user_id if needed by the frontend
    })

@api_view(['POST'])
# Unlock Logic
def unloc(request):
        global esp_socket
        data = request.data
        rack_id = data.get('rack_id')
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            return Response({'message': 'User not authenticated'}, status=401)

        if not rack_id:
            return Response({'message': 'Rack ID is required'}, status=400)

        try:
            rack_user = Rack_User.objects.get(user_id=user_id, rack_id=rack_id)
            rack = rack_user.rack
            user = rack_user.user

            # Signal Arduino to unlock the rack
            if esp_socket:
                ESP32Consumer.esp_socket.send(text_data = {"action":"unlock", "rackId": rack_id})
                return Response("lock command sent")
                
            # Update rack status and timestamps
            current_time = timezone.now()
            rack.status = 'unlocked'
            rack.unlocked_at = current_time
            rack.save()

            # Move to history
            history_data = {
                'user': user.id,
                'rack': rack.id,
                'locked_at': rack.locked_at,
                'unlocked_at': current_time,
            }
            history_serializer = HistorySerializer(data=history_data)
            if history_serializer.is_valid():
                history_serializer.save()
                rack_user.delete()
                return Response({'message': 'Rack unlocked successfully'})
            else:
                return Response(history_serializer.errors, status=400)

        except Rack_User.DoesNotExist:
            logger.error(f"Rack or user record not found for rack_id {rack_id} and user_id {user_id}")
            return Response({'message': 'Rack or user record not found'}, status=404)


@api_view(['GET'])
def access_get(request):
    """Handles the GET request to return the login/register page message."""
    if request.method == 'GET':
        return Response({
            'status': 'success',
            'message': 'Frontend handles the login/register page.',
            'redirect_url': 'https://frontend-platform.com/login',  # Replace with actual frontend URL
        })

@api_view(['POST'])
def access_post(request):
    if request.method == 'POST':
        action = request.data.get('action')  
        username = request.data.get('name')
        password = request.data.get('password')
        email =  request.data.get('email')
        phonenumber = request.data.get('phonenumber')

        if not username or not password:
            return Response({'message': 'Username and password are required'}, status=400)

        if action == 'login':
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    response = Response({'message': 'Login successful'})
                    response.set_cookie('user_id', user.id, httponly=True, secure=True)
                    return response
                else:
                    return Response({'message': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                # If the user doesn't exist, redirect to the signup page
                logger.error(f"Login attempt failed. User {username} not found.")
                return Response({
                    'message': 'User not found. Redirecting to signup.',
                    'redirect_url': 'https://frontend-platform.com/signup'  # Redirect to signup page
                }, status=400)

        elif action == 'register':
            if User.objects.filter(username=username).exists():
                return Response({'message': 'Username already exists'}, status=400)
            if not email or not phonenumber:
                return Response({'message': 'Email and phone number are required'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'}, status=400)

            user_data = {
                'name': username,
                'password': make_password(password),  # Hash the password
                'email': email,
                'phonenumber': phonenumber,
            }
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Registration successful'})
            else:
                return Response(user_serializer.errors, status=400)

        else:
            return Response({'message': 'Invalid action provided'}, status=400)
