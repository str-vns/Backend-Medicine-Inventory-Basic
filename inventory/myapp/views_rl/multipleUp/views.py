from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
from ...models import Medicine, MultipleUpload
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import traceback
import json

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createMultiImage (request):
    if request.method == 'POST':
        body = request.POST
        if not body:
            return JsonResponse({"message": "Please Provide all the required fields"}, status=400)
        images = request.FILES.getlist('img')
        print(images, "test")
        try:
            med_Id = Medicine.objects.get(pk=body.get("item_id"))
            
            for image in images: 
                imgResponse = upload_helper(image=image, path='medicine')
                new_multi_img = MultipleUpload(
                    item_id=med_Id,
                    url=imgResponse[0],
                    public_id=imgResponse[1],
                    original_name=imgResponse[2]
                )
                
                new_multi_img.save()
                
            return JsonResponse({"message": "Image uploaded successfully"}, status=200)
         
        except Exception as e: 
            return JsonResponse({"Error": str(e)}, status=500)
        except Medicine.DoesNotExist:
            raise Http404("Id does not exist")
      
@csrf_exempt  
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteMultiImage(request, id):
    if request.method == 'DELETE':
        path = request.GET.get('path')
        if not path:
            return JsonResponse({"message": "Please provide the 'path' parameter."}, status=400)
        try:
            multi_img = MultipleUpload.objects.get(pk=id)
            print(multi_img.public_id, "public_id")  # Debug print
            delete_image_helper(multi_img.public_id, path=path)
            multi_img.delete()
            return JsonResponse({"message": "Image deleted successfully"}, status=200)
        except MultipleUpload.DoesNotExist:
            return JsonResponse({"error": "Id does not exist"}, status=404)
        except Exception as e:
            print(traceback.format_exc())  # This will print the full error in your server log
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return HttpResponseNotAllowed(['DELETE'], "Method not allowed, only DELETE is allowed")

    