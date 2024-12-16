from rest_framework import serializers
from .models import User,Rack,Rack_User,History

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name","email","phonenumber","password"]
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = ["id","status","address"]

class Rack_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack_User
        fields = ["user","rack","locked_at"]

class HistorySerializer(serializers.ModelSerializer):  
    User = UserSerializer(read_only =  True)
    class Meta:
        model = History
        fields = ["user","rack","locked_at","unlocked_at"]