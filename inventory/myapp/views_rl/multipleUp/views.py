from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
from ...models import Medicine, MultipleUpload
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def createMultiImage (request):
    if request.method == 'POST':
        body = request.POST
        images = request.FILES.getlist('img')
       
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
        
    