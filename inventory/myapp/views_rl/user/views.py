from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
from ...models import User
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
# Create your views here.
def create_a_new_user(request):
    if request.method == 'POST' : 
        body = request.POST
        new_name = body.get('name')
        new_email = body.get('email')
        new_password = body.get('password')
        images = request.FILES['img']
        
        
        # if images is not None:
        #     image = images
        # else:
        #     image = 
        
        # print(test)
        # imgResponse = upload_helper(image= image, path='user')
    
    
        try:
            if new_email == None or new_password == None or new_name == None:
                return Http404({"message": "Please provide all the required fields"}, status=400)
          
            new_user = User(
                name=new_name, 
                email=new_email, 
                password=new_password,
                # image=imgResponse[0],
                # public_id=imgResponse[1],
                # original_name=imgResponse[2],
                )
            
            # new_user.save()
            
            return JsonResponse({"message": "User created successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
        
# read all user
def get_all_users(request):
     queryset = User.objects.all()
     data = serializers.serialize('json', queryset)
     return HttpResponse(data)
 
def get_user_by_id(request, user_id):
    try:
      query_set = User.objects.filter(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Restaurant does not exist")
    data = serializers.serialize("json", query_set)
    return HttpResponse(data)

@csrf_exempt   
def update_user(request, user_id):
    if request.method == "PATCH":
        try:
            body = json.loads(request.body.decode("utf-8"))
            new_name = body.get("name")
            new_email = body.get("email")
            new_password = body.get("password")
            try:
                user = User.objects.get(id=user_id)
                
            except User.DoesNotExist:
                return HttpResponse({"error": "User not found"}, status=404)

            if new_name:
                user.name = new_name
            if new_email:
                user.email = new_email
            if new_password:
                user.password = new_password  # Consider hashing passwords before saving

            user.save()
            return JsonResponse({"message": "User updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(["PATCH"])

@csrf_exempt 
def delete_user(request, user_id):
    
    if request.method == 'DELETE' :
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Http404("User does not exist")
         
        print(user.image)
        delete_image_helper(image= user.public, path='user')
        # user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)
    
    else:
        return HttpResponseNotAllowed("Method Not Supported")

def get_profile(request, user_id):
     if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Http404("User does not exist")
        
        data = serializers.serialize('json', [user])
        return HttpResponse(data, content_type='application/json')
     else:
         return HttpResponse("Method Not Supported")