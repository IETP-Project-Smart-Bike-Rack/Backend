from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import Rack, Rack_User, User, History
from django.contrib.auth.hashers import check_password, make_password
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
        rack_id (str): The ID of the rack.
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

# QR Code Scanning and Locking Logic
def loc(request):
    if request.method == 'POST':
        rack_id = request.POST.get('rack_id')
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            return JsonResponse({'message': 'User not authenticated'}, status=401)

        if not rack_id:
            return JsonResponse({'message': 'Rack ID is required'}, status=400)

        try:
            rack = Rack.objects.get(rack_id=rack_id)
            if rack.status == 'locked':
                return JsonResponse({'message': 'Rack is already locked. Please choose another.'}, status=400)

            # Signal Arduino to lock the rack
            arduino_response = send_arduino_signal(rack_id, "lock")
            if "error" in arduino_response:
                return JsonResponse(arduino_response, status=500)

            # Update rack status and save to database
            rack.status = 'locked'
            rack.save()
            Rack_User.objects.create(user_id=user_id, rack=rack)
            return JsonResponse({'message': 'Rack locked successfully'})
        except Rack.DoesNotExist:
            logger.error(f"Rack with ID {rack_id} not found")
            return JsonResponse({'message': 'Rack not found'}, status=404)

# Unlock Logic
def unloc(request):
    if request.method == 'POST':
        rack_id = request.POST.get('rack_id')
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            return JsonResponse({'message': 'User not authenticated'}, status=401)

        if not rack_id:
            return JsonResponse({'message': 'Rack ID is required'}, status=400)

        try:
            rack_user = Rack_User.objects.get(user_id=user_id, rack__rack_id=rack_id)
            rack = rack_user.rack

            # Signal Arduino to unlock the rack
            arduino_response = send_arduino_signal(rack_id, "unlock")
            if "error" in arduino_response:
                return JsonResponse(arduino_response, status=500)

            # Update rack status and save to database
            rack.status = 'unlocked'
            rack.save()

            # Move to history
            History.objects.create(
                user_id=user_id, rack=rack, locked_at=rack_user.locked_at
            )
            rack_user.delete()
            return JsonResponse({'message': 'Rack unlocked successfully'})
        except Rack_User.DoesNotExist:
            logger.error(f"Rack or user record not found for rack_id {rack_id} and user_id {user_id}")
            return JsonResponse({'message': 'Rack or user record not found'}, status=404)

# Login/Register Page
def access(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'message': 'Username and password are required'}, status=400)

        if action == 'login':
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    response = JsonResponse({'message': 'Login successful'})
                    response.set_cookie('user_id', user.id, httponly=True, secure=True)
                    return response
                return JsonResponse({'message': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                logger.error(f"Login attempt failed. User {username} not found.")
                return JsonResponse({'message': 'User not found'}, status=400)

        elif action == 'register':
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists'}, status=400)

            hashed_password = make_password(password)
            User.objects.create(username=username, password=hashed_password)
            return JsonResponse({'message': 'Registration successful'})
