from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    contact_number = request.data.get('contact_number')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    # Validate that all fields are provided.
    if not all([username, email, contact_number, password, confirm_password]):
        return Response({"error": "All fields are required."}, status=400)
    
    # Validate password match.
    if password != confirm_password:
        return Response({"error": "Passwords do not match."}, status=400)
    
    # Check if a user with the provided email already exists.
    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists."}, status=400)

    # Create the user with the provided fields.
    user = User.objects.create_user(
        email=email,
        password=password,
        username=username,
        contact_number=contact_number
    )
    return Response({"message": "User created successfully"})

@api_view(['POST'])
def login(request):
    print("DEBUG: Received data:", request.data)  # Debug log

    # Use 'login_identifier' if provided, else fall back to 'email'
    login_identifier = request.data.get('login_identifier') or request.data.get('email')
    password = request.data.get('password')

    if not login_identifier or not password:
        return Response({"error": "Both username or email and password are required."}, status=400)

    user = None

    # If the identifier contains an "@" symbol, assume it's an email.
    if "@" in login_identifier:
        user = authenticate(request, username=login_identifier, password=password)
    else:
        # Try to find a user by username and check the password manually.
        try:
            user_obj = User.objects.get(username=login_identifier)
            if user_obj.check_password(password):
                user = user_obj
        except User.DoesNotExist:
            user = None

    if user:
        tokens = get_tokens_for_user(user)
        return Response({"message": "Login successful", "tokens": tokens})
    
    return Response({"error": "Invalid credentials"}, status=400)
