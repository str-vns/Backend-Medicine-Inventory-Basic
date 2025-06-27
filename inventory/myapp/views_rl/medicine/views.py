from django.http import JsonResponse, Http404, HttpResponseNotAllowed, HttpResponse
from django.core import serializers
from ...utils.upload.uploadImage import upload_helper, delete_image_helper
from ...models import Medicine, MultipleUpload
from django.views.decorators.csrf import csrf_exempt
from ...utils.upload.uploadImage import upload_helper
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)
import json


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_medicine(request):

    if request.method == "POST":
        body = request.data
        print("Request body:", body)
        if not body:
            return JsonResponse(
                {"message": "Please Provide all the required fields"}, status=400
            )

        new_medicine_name = body.get("medicine_name")
        new_medicine_desc = body.get("medicine_desc")

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

                data = {
                    "id": new_medicine.id,
                    "medicine_name": new_medicine.medicine_name,
                    "medicine_desc": new_medicine.medicine_desc,
                    "created_at": (
                        new_medicine.created_at
                        if hasattr(new_medicine, "created_at")
                        else None
                    ),
                }
                return JsonResponse(data, status=200)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return HttpResponseNotAllowed(["POST"])


@csrf_exempt
@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_all_medicines(request):
    try:
        if request.method != "GET":
            return HttpResponseNotAllowed(["GET"])
        query_set = MultipleUpload.objects.select_related("item_id").order_by("-created_at")
        medicine_dict = {}

        for med in query_set:
            id_val = med.item_id.id
            if id_val in medicine_dict:
                medicine_dict[id_val]["images"].append({
                    "id": med.id,
                    "url": med.url,
                    "original_name": med.original_name,
                    "public_id": med.public_id
                })
            else:
                medicine_dict[id_val] = {
                    "id": med.item_id.id,
                    "medicine_name": med.item_id.medicine_name,
                    "medicine_desc": med.item_id.medicine_desc,
                    "images": [{
                        "id": med.id,
                        "url": med.url,
                        "original_name": med.original_name,
                        "public_id": med.public_id
                    }],
                    "created_at": med.created_at,
                    "onActive": med.item_id.onActive,
                }
        medicine_list = list(medicine_dict.values())
        return JsonResponse(medicine_list, status=200, safe=False)
    except Exception as error:
        logger.error(f'Error fetching medicines: {error}')
        return JsonResponse(
            {"Error": "Fetching Medicines Failed", "Information": str(error)},
            status=500,
        )


@csrf_exempt
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_Update_medicines(request, medicine_id):
    if request.method == "PATCH":
        try:

            body = request.data
            if not body:
             return JsonResponse(
                {"message": "Please Provide all the required fields"}, status=400
            )
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
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_medicine(request, medicine_id):
    print("delete_medicine called with medicine_id:", medicine_id)
    if request.method == "DELETE":
        try:
            medicine = Medicine.objects.get(pk=medicine_id)
            print("Medicine object found:", medicine)
        except Medicine.DoesNotExist:
            return JsonResponse({"Error": "The id you provided does not Exist"}, status=404)

        medicine.delete()
        return JsonResponse({"message": "Medicine Deleted Successfully"}, status=200)
    else:
        return HttpResponseNotAllowed(["DELETE"])


@csrf_exempt
def single_medicine(request, medicine_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        medicine = Medicine.objects.get(pk=medicine_id)
    except Medicine.DoesNotExist:
        return JsonResponse({"error": "The ID you provided does not exist."}, status=404)

    query_set = MultipleUpload.objects.select_related("item_id") \
        .filter(item_id=medicine) \
        .order_by("-created_at")

    medicine_dict = {
        "id": medicine.id,
        "medicine_name": medicine.medicine_name,
        "medicine_desc": medicine.medicine_desc,
        "onActive": medicine.onActive,
        "created_at": medicine.created_at,
        "images": [],
    }

    for img in query_set:
        medicine_dict["images"].append({
            "id": img.id,
            "url": img.url,
            "original_name": img.original_name,
            "public_id": img.public_id
        })

    return JsonResponse(medicine_dict, safe=False)
