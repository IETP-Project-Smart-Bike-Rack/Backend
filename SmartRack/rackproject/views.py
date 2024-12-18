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

# Configure logging
logger = logging.getLogger(__name__)

# Constants for Arduino communication
ARDUINO_URL = "http://arduino.local/api/lock"

def send_arduino_signal(rack_id, action):
    """
    Sends a signal to the Arduino hardware to lock or unlock the rack.

    Args:
        rack_id (int): The ID of the rack.
        action (str): The action to perform ('lock' or 'unlock').

    Returns:
        dict: Response from the Arduino or an error message.
    """
    try:
        response = requests.post(ARDUINO_URL, json={"rack_id": rack_id, "action": action})
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Arduino communication failed with status {response.status_code}")
            return {"error": "Failed to communicate with Arduino"}
    except requests.RequestException as e:
        logger.exception("Error communicating with Arduino")
        return {"error": str(e)}

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
            arduino_response = send_arduino_signal(rack_id, "lock")
            if "error" in arduino_response:
                return Response(arduino_response, status=500)

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
            arduino_response = send_arduino_signal(rack_id, "unlock")
            if "error" in arduino_response:
                return Response(arduino_response, status=500)

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
# Login/Register Page
def access_post(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return Response({'message': 'Username and password are required'}, status=400)

        if action == 'login':
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    response = Response({'message': 'Login successful'})
                    response.set_cookie('user_id', user.id, httponly=True, secure=True)
                    return response
                return Response({'message': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                logger.error(f"Login attempt failed. User {username} not found.")
                return Response({'message': 'User not found'}, status=400)

        elif action == 'register':
            if User.objects.filter(username=username).exists():
                return Response({'message': 'Username already exists'}, status=400)

            user_data = {
                'username': username,
                'password': make_password(password),
            }
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Registration successful'})
            else:
                return Response(user_serializer.errors, status=400)
