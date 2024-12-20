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
#from datetime import datetime, timedelta
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
        response = requests.post(
            ARDUINO_URL,
            json={"rack_id": rack_id, "action": action},
            timeout=5  # Optional timeout for the request
        )
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Arduino communication failed with status {response.status_code}")
            return {"error": "Failed to communicate with Arduino"}
    except requests.RequestException as e:
        logger.exception("Error communicating with Arduino")
        return {"error": str(e)}
    
@api_view(['GET'])
def get_unlocked_racks(request):
    unlocked_racks = Rack.objects.filter(status='unlocked')
    serializer = RackSerializer(unlocked_racks, many=True)
    return Response(serializer.data)

    

@api_view(['GET'])
def get_locked_racks(request):
    user_id = request.data.get('user_id')  # Retrieve user_id from cookies
    if not user_id:
        return Response({'message': 'User not authenticated'}, status=401)

    try:
        logger.debug(f"Retrieving locked racks for user ID {user_id}")
        locked_racks = Rack_User.objects.filter(user_id=user_id, rack__status='locked')
        logger.debug(f"Locked racks query result: {locked_racks}")

        if not locked_racks.exists():
            logger.debug(f"No locked racks found for user ID {user_id}")
            return Response({'message': 'No locked racks found for this user'}, status=404)
        
        rack_ids = locked_racks.values_list('rack_id', flat=True)
        logger.debug(f"Locked rack IDs: {list(rack_ids)}")
        return Response({'locked_rack_ids': list(rack_ids)})
    except Rack_User.DoesNotExist:
        logger.error(f"No locked racks found for user ID {user_id}")
        return Response({'message': 'No locked racks found for this user'}, status=404)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return Response({'message': 'An unexpected error occurred'}, status=500)


@api_view(['GET'])
def lock_rack_page(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'message': 'User not authenticated'}, status=401)
    
    page_url = "http://localhost:5173/dashboard"
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
        user_id = data.get('user_id')
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
           # arduino_response = send_arduino_signal(rack_id, "lock")
            #if "error" in arduino_response:
               # return Response(arduino_response, status=500)

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

    page_url = "http://localhost:5173/dashboard"

    #Respond with the URL and optional user details
    return Response({
        "message": "Unlock page URL retrieved successfully",
        "unlock_page_url": page_url,
        "user_id": user_id  # Pass user_id if needed by the frontend
    })

@api_view(['POST'])
def unloc(request):
    data = request.data
    rack_id = data.get('rack_id')
    user_id = data.get('user_id')  # Replace with actual user authentication logic
    
    if not user_id:
        return Response({'message': 'User not authenticated'}, status=401)

    if not rack_id:
        return Response({'message': 'Rack ID is required'}, status=400)

    try:
        rack_user = Rack_User.objects.get(user_id=user_id, rack_id=rack_id)
        rack = rack_user.rack
        user = rack_user.user

        # Signal Arduino to unlock the rack (uncomment if required)
        # arduino_response = send_arduino_signal(rack_id, "unlock")
        # if "error" in arduino_response:
        #     return Response(arduino_response, status=500)

        # Update rack status
        rack.status = 'unlocked'
        rack.save()

        # Prepare data for History
        locked_at = rack_user.locked_at  # Ensure this field exists in Rack_User
        current_time =  timezone.now()
        history_data = {
            'user': user.id,
            'rack': rack.id,
            'locked_at':  locked_at,
            'unlocked_at': current_time,
        }

        # Save to History
        history_serializer = HistorySerializer(data=history_data)
        if history_serializer.is_valid():
            history_serializer.save()
            rack_user.delete()
            return Response({'message': 'Rack unlocked successfully'})
        else:
            logger.error(f"History serializer errors: {history_serializer.errors}")
            return Response({'message': 'Failed to save history', 'errors': history_serializer.errors}, status=400)

    except Rack_User.DoesNotExist:
        logger.error(f"Rack or user record not found for rack_id {rack_id} and user_id {user_id}")
        return Response({'message': 'Rack or user record not found'}, status=404)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'message': 'An unexpected error occurred', 'error': str(e)}, status=500)

@api_view(['GET'])
def access_get(request):
    """Handles the GET request to return the login/register page message."""
    if request.method == 'GET':
        return Response({
            'status': 'success',
            'message': 'Frontend handles the login/register page.',
          'redirect_url': 'https://frontend-platform.com/login',  # 'redirect_url': 'http://localhost:5173/dashbord',  # Replace with actual frontend URL
        })
@api_view(['GET'])
def get_user_id(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        return Response({'user_id': user_id})
    else:
        return Response({'message': 'User not logged in'}, status=401)
    

@api_view(['POST'])
def access_post(request):
    if request.method == 'POST':
        action = request.data.get('action')  
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')

        if not username or not password:
            return Response({'message': 'Username and password are required'}, status=400)

        if action == 'login':
            try:
                user = User.objects.get(name=username)
                # Compare plain-text passwords directly
                if user.password == password:
                    response = Response({'message': 'Login successful', 'redirect_url': f'http://localhost:5173/dashboard/{user.id}'})
                    #response.set_cookie('user_id', user.id, httponly=True, secure=True, expires=timedelta(days=1))
                    return response
                else:
                    return Response({'message': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                # If the user doesn't exist, redirect to the signup page
                logger.error(f"Login attempt failed. User {username} not found.")
                return Response({
                    'message': 'User not found. Redirecting to signup.',
                    'redirect_url': 'http://localhost:5173/signup'  # Redirect to signup page
                }, status=400)

        elif action == 'register':
            if User.objects.filter(name=username).exists():
                return Response({'message': 'Username already exists'}, status=400)

            # Store the password as plain text
            user_data = {
                'name': username,
                'email': email,
                'phonenumber': phonenumber,
                'password': password,  # Plain-text password
            }

            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Registration successful'})
            else:
                return Response(user_serializer.errors, status=400)

        else:
            return Response({'message': 'Invalid action provided'}, status=400)