from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Additional fields if needed
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    elo = models.IntegerField(default=1500)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    highest_elo = models.IntegerField(default=1500)
    
    # Simple stats
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} ({self.elo})"

class Game(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    )
    CADENCE_CHOICES = (
        ('1+0', '1+0'),
        ('2+1', '2+1'),
        ('3+0', '3+0'),
        ('5+0', '5+0'),
    )

    white_player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_white', null=True, blank=True)
    black_player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_black', null=True, blank=True)
    
    fen = models.CharField(max_length=255, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') # Standard start, will override for antichess if needed
    pgn = models.TextField(blank=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    cadence = models.CharField(max_length=10, choices=CADENCE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.id} ({self.white_player} vs {self.black_player})"

