from django.shortcuts import render

# Create your views here.

# Show login page
def login_page(request):
    return render(request, "users/login.html")

# Show register page
def register_page(request):
    return render(request, "users/registration.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import User

# API: Login
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"message": "Invalid password"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

    return JsonResponse({"message": "Invalid request"}, status=400)


# API: Register
@csrf_exempt
def register_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if not all([name, email, username, password]):
            return JsonResponse({"message": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already registered"}, status=400)

        user = User.objects.create(
            name=name,
            email=email,
            username=username,
            password=make_password(password)  # hash the password
        )
        return JsonResponse({"message": "User created successfully"})

    return JsonResponse({"message": "Invalid request"}, status=400)
