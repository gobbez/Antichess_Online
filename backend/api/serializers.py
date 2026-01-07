from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Game

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['elo', 'avatar', 'highest_elo', 'games_played', 'wins', 'losses', 'draws']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user

class GameSerializer(serializers.ModelSerializer):
    white_player = UserSerializer(read_only=True)
    black_player = UserSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = '__all__'
