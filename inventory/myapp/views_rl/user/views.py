from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
from ...models import User
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import json


@csrf_exempt
@api_view(['POST'])
# Create your views here.
def create_a_new_user(request):

    if request.method == "POST":
        body = request.POST
        new_email = body.get("email")
        new_first_name = body.get("first_name")
        new_last_name = body.get("last_name")
        new_password = body.get("password")
        images = request.FILES.getlist("img")

        if new_email is None :
            return JsonResponse({"message": "Please Provide Email "}, status=400)
        if new_password is None:
            return JsonResponse({"message": "Please Provide Password "}, status=400)
        if new_first_name is None:
            return JsonResponse({"message": "Please Provide First Name "}, status=400)
        if new_last_name is None:
            return JsonResponse({"message": "Please Provide Last Name "}, status=400)
        
        if images is not None:
            image = images
        else:
            image = []

        for image in images:
            imgResponse = upload_helper(image=image, path="user")

        try:

            new_user = User(
                email=new_email,
                password=make_password(new_password),
                first_name=new_first_name,
                last_name=new_last_name,
                image=imgResponse[0],
                public_id=imgResponse[1],
                original_name=imgResponse[2],
            )

            new_user.save()

            return JsonResponse({"message": "User created successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)


def create_super_user(request, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True." , status=400)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.", status=400)   
   
        return User.create_a_new_user(request, **extra_fields)

# read all user
def get_all_users(request):
    queryset = User.objects.all()
    data = serializers.serialize("json", queryset)
    return HttpResponse(data)


def get_user_by_id(request, user_id):
    try:
        query_set = User.objects.filter(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Restaurant does not exist")
    data = serializers.serialize("json", query_set)
    return HttpResponse(data)


@csrf_exempt
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if request.method == "PATCH":
        try:
            body = request.data
            new_first_name = body.get("first_name")
            new_last_name = body.get("last_name")
            images = request.FILES.getlist("img")
            try:
                user = User.objects.get(id=user_id)
                
                if images is not None:
                    image = images
                else:
                    image = []

                for image in images:
                    imgResponse = upload_helper(image=image, path="user")

   
            except User.DoesNotExist:
                return HttpResponse({"error": "User not found"}, status=404)

            if new_first_name:
                user.first_name = new_first_name
            if new_last_name:
                user.last_name = new_last_name
            if images:
                user.image = imgResponse[0]
                user.public_id = imgResponse[1]
                user.original_name = imgResponse[2]

            user.save()
            return JsonResponse({"message": "User updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(["PATCH"])


@csrf_exempt
def delete_user(request, user_id):

    if request.method == "DELETE":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Http404("User does not exist")

        print(user.image)
        delete_image_helper(image=user.public, path="user")
        # user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)

    else:
        return HttpResponseNotAllowed("Method Not Supported")


def get_profile(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Http404("User does not exist")

        data = serializers.serialize("json", [user])
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse("Method Not Supported")


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        body = request.POST
        email = body.get("email")
        password = body.get("password")
        print(email, password)
        if email is None or password is None:
            return JsonResponse(
                {"message": "Please provide all the required fields"}, status=400
            )

        user = authenticate(email=email, password=password)
        
        if user is user.is_active == False:
            return JsonResponse({"message": "Your Account is Disable please contact Admin"}, status=403)
        
        if user is not None:
           
            currentUser = User.objects.get(id=user.id)
            currentUser.last_login = timezone.now()
            currentUser.save()
            currentUser.refresh_from_db()
            
            token, created = Token.objects.get_or_create(user=user)
            if not created and token.created < timezone.now() - timedelta(days=1):
                token.delete()
                token = Token.objects.create(user=user)
                
            datas = {
                "id" : currentUser.id,
                "email": currentUser.email,
                "password" : currentUser.password, 
                "first_name": currentUser.first_name,
                "last_name": currentUser.last_name,
                "isActive" : currentUser.is_active,
                "group": [group.name for group in currentUser.groups.all()],
                "user_permissions": [perm.codename for perm in currentUser.user_permissions.all()],
                "url" : currentUser.image,
                "public_id": currentUser.public_id,
                "created_at" : currentUser.created_at,
                "last_login": currentUser.last_login,
                "token": token.key  
            }


            return JsonResponse(datas,  content_type="application/json")
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)
    else:
        return HttpResponseNotAllowed(["POST"])

