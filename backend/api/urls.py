from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CurrentUserView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
