from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from imdb.models import TitleBasics
# Create your views here.

# Show start_page page
def start_page(request):
    return render(request, "users/start_page.html")

# Show home page
def home_page(request):
    return render(request, "users/home.html")

# Show login page
def login_page(request):
    return render(request, "users/login.html")

# Show register page
def register_page(request):
    return render(request, "users/registration.html")

# Show search result
def search(request):
    query = request.GET.get("q", "").strip()  # remove whitespace safely

    if query:
        results = TitleBasics.objects.filter(
            Q(primary_title__icontains=query) |
            Q(original_title__icontains=query)
        )
    else:
        # Default to latest releases if no search term
        results = TitleBasics.objects.order_by("-start_year")

    paginator = Paginator(results, 24)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/home.html",
        {"page_obj": page_obj, "query": query}
    )


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
