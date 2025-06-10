from django.http import JsonResponse, Http404, HttpResponseNotAllowed, HttpResponse
from django.core import serializers
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from ...models import Medicine, MultipleUpload
from django.views.decorators.csrf import csrf_exempt
from ...utils.upload.uploadImage import upload_helper
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json


@csrf_exempt
def create_medicine(request):

    if request.method == "POST":
        body = request.POST
        new_medicine_name = body.get("medicine_name")
        new_medicine_desc = body.get("medicine_desc")
        images = request.FILES.getlist("img")

        try:
            if new_medicine_name is None or new_medicine_desc is None:
                return JsonResponse(
                    {"message": "Please Provide all the required fields"}, status=400
                )
            else:
                new_medicine = Medicine(
                    medicine_name=new_medicine_name, medicine_desc=new_medicine_desc
                )

                new_medicine.save()
                # data = serializers.serialize('json', [new_medicine])
                data = json.loads(serializers.serialize("json", [new_medicine]))

                return HttpResponse(data, status=200)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return HttpResponseNotAllowed(["POST"])

@csrf_exempt
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_all_medicines(request):
    
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    query_set = MultipleUpload.objects.select_related("item_id").order_by("-created_at")
    medicine_dict = {}

    for med in query_set:
        id_val = med.item_id.id
        if id_val in medicine_dict:
            medicine_dict[id_val]["images"].append(med.url)
        else:
            medicine_dict[id_val] = {
                "id": med.item_id.id,
                "medicine_name": med.item_id.medicine_name,
                "medicine_desc": med.item_id.medicine_desc,
                "images": [med.url],
                "created_at": med.created_at,
                "onActive": med.item_id.onActive,
            }

    medicine_list = list(medicine_dict.values())
    return JsonResponse(medicine_list, status=200, safe=False)


@csrf_exempt
def get_Update_medicines(request, medicine_id):
    if request.method == "PATCH":
        try:

            body = json.loads(request.body.decode("utf-8"))
            new_medicine_name = body.get("medicine_name")
            new_medicine_desc = body.get("medicine_desc")

            try:
                query_set = Medicine.objects.get(id=medicine_id)
            except Medicine.DoesNotExist:
                JsonResponse(
                    {"Error": "The id you provided does not Exist"}, status=404
                )

            if new_medicine_name:
                query_set.medicine_name = new_medicine_name
            if new_medicine_desc:
                query_set.medicine_desc = new_medicine_desc

            query_set.save()

            return JsonResponse(
                {"message": "Medicine Updated Successfully"}, status=200
            )

        except Exception as e:
            return HttpResponse({"Error": str(e)}, status=500)

    else:
        return HttpResponseNotAllowed(["PATCH"])


@csrf_exempt
def delete_medicine(request, medicine_id):
    if request.method == "DELETE":
        try:
            query_set = Medicine.objects.get(pk=medicine_id)
        except Medicine.DoesNotExist:
            JsonResponse({"Error": "The id you provided does not Exist"}, status=404)

        query_set.delete()
        return JsonResponse({"message": "Medicine Deleted Successfully"}, status=200)
    else:
        return HttpResponseNotAllowed(["DELETE"])


def single_medicine(request, medicine_id):
    if request.method == "GET":
        try:
            medicineId = Medicine.objects.get(pk=medicine_id)
        except Medicine.DoesNotExist:
            JsonResponse({"Error": "The id you provided does not Exist"}, status=404)

        data = serializers.serialize("json", [medicineId])
        return HttpResponse(data)
    else:
        return HttpResponseNotAllowed(["GET"])
