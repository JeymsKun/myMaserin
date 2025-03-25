from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes  # Add permission_classes import
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_users(request):
    users = User.objects.all().values('id', 'username', 'date_joined')
    return Response(list(users))

# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        tokens = get_tokens_for_user(user)
        return Response({"message": "Login successful", "tokens": tokens})
    
    return Response({"error": "Invalid credentials"}, status=400)
