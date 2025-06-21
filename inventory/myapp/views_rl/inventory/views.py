from django.http import JsonResponse, Http404, HttpResponseNotAllowed, HttpResponse
from ...models import Inventory, Medicine, MultipleUpload
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ...utils.messageHandler import handle_get_request
import json


@csrf_exempt
def create_inventory(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        try:
            med_Id = Medicine.objects.get(pk=body.get("medicine_id"))
        except Medicine.DoesNotExist:
            raise Http404("Medicine does not exist")

        if (
            body.get("quantity") is None
            or int(body.get("quantity")) <= 0
            or not body.get("quantity").isdigit()
        ):
            return JsonResponse(
                {"message": "Please provide a valid quantity"}, status=400
            )
        if (
            body.get("medicine_price") is None
            or float(body.get("medicine_price")) <= 0
            or not body.get("medicine_price").replace(".", "", 1).isdigit()
        ):
            return JsonResponse(
                {"message": "Please provide a valid medicine price"}, status=400
            )

        new_medicine_price = float(body.get("medicine_price"))
        new_quantity = int(body.get("quantity"))
        new_medicine_type = body.get("medicine_type")
        new_medicine_measurement = body.get("medicine_measurement")
        new_manufacturer = body.get("manufacturer")
        new_expiration_date = body.get("expiration_date")

        new_inventory = Inventory(
            medicine_id=med_Id,
            medicine_price=new_medicine_price,
            quantity=new_quantity,
            medicine_type=new_medicine_type,
            medicine_measurement=new_medicine_measurement,
            manufacturer=new_manufacturer,
            expiration_date=new_expiration_date,
        )

        new_inventory.save()

        if Medicine.objects.filter(onActive=False, pk=body.get("medicine_id")).exists():
            Medicine.objects.filter(pk=body.get("medicine_id")).update(onActive=True)
        else:
            print("Medicine is already active")

        return JsonResponse({"message": "Inventory Created Successfully"}, status=200)

    return JsonResponse({"message": "Method not allowed"}, status=405)


def get_all_inventories(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    query_set = Inventory.objects.select_related("medicine_id").order_by("-created_at")

    inventories = {}

    for inv in query_set:
        id_val = inv.medicine_id.id
        images = MultipleUpload.objects.filter(item_id=inv.medicine_id).order_by("-created_at")
        images_list = [
            {
                "id": img.id,
                "url": img.url,
                "original_name": img.original_name,
                "public_id": img.public_id,
            }
            for img in images
        ]
            
        inventory_data = {
            "id": inv.id,
            "medicine_measurement": inv.medicine_measurement,
            "medicine_price": inv.medicine_price,
            "medicine_type": inv.medicine_type,
            "manufacturer": inv.manufacturer,
            "expiration_date": inv.expiration_date,
            "onActive": inv.onActive,
            "quantity": inv.quantity,
            "created_at": inv.created_at,
        }
        if id_val in inventories:
            inventories[id_val]["inventories"].append(inventory_data)
        else:
            inventories[id_val] = {
                "medicine_id": inv.medicine_id.id,
                "medicine_name": inv.medicine_id.medicine_name,
                "medicine_desc": inv.medicine_id.medicine_desc,
                "images": images_list,
                "inventories": [inventory_data],
            }

    inventory = list(inventories.values())
    return JsonResponse(inventory, status=200, safe=False)


def get_single_inventory(request, inventory_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        # Get all inventories for this medicine_id
        inventory_qs = Inventory.objects.select_related("medicine_id").filter(medicine_id=inventory_id).order_by("-created_at")
        if not inventory_qs.exists():
            return JsonResponse(
                {"status": "Error", "message": "No inventories found for this medicine_id", "code": 404},
                status=404
            )

        # Get the medicine object (all inventories have the same medicine)
        medicine = inventory_qs[0].medicine_id

        # Get all images for this medicine
        images = MultipleUpload.objects.filter(item_id=medicine).order_by("-created_at")
        images_list = [
            {
                "id": img.id,
                "url": img.url,
                "original_name": img.original_name,
                "public_id": img.public_id,
            }
            for img in images
        ]

        inventories_list = []
        for inv in inventory_qs:
            inventories_list.append({
                "id": inv.id,
                "medicine_measurement": inv.medicine_measurement,
                "medicine_price": inv.medicine_price,
                "medicine_type": inv.medicine_type,
                "manufacturer": inv.manufacturer,
                "expiration_date": inv.expiration_date,
                "onActive": inv.onActive,
                "quantity": inv.quantity,
                "created_at": inv.created_at,
            })

        result = {
            "medicine_id": medicine.id,
            "medicine_name": medicine.medicine_name,
            "medicine_desc": medicine.medicine_desc,
            "images": images_list,
            "inventories": inventories_list,
        }
        return JsonResponse(result, status=200, safe=False)

    except Exception as e:
        message = {"status": "Error", "message": str(e), "code": 500}
        return handle_get_request(message)


@csrf_exempt
def update_inventory(request, inventory_id):
    if request.method == "PATCH":
        try:
            body = json.loads(request.body.decode("utf-8"))
            new_medicine_price = body.get("medicine_price")
            new_quantity = body.get("quantity")
            new_medicine_type = body.get("medicine_type")
            inventory = Inventory.objects.get(pk=inventory_id)

            if new_medicine_price:
                inventory.medicine_price = new_medicine_price
            if new_quantity:
                inventory.quantity = new_quantity
            if new_medicine_type:
                inventory.medicine_type = new_medicine_type
            inventory.save()

            return JsonResponse(
                {"message": "Inventory Updated Successfully"}, status=200
            )

        except Exception as e:
            message = {"status": "Error", "message": str(e), "code": 500}
        return handle_get_request(message)
    else:
        return HttpResponseNotAllowed(["PATCH"])


@csrf_exempt
def delete_inventory(request, inventory_id):
    if request.method == "DELETE":
        try:
            inventory = Inventory.objects.get(pk=inventory_id)
        except Inventory.doesNotExist:
            return JsonResponse({"message": "Inventory Id does not Exist "}, status=500)
        inventory.delete()
        return JsonResponse({"message": "Inventory Deleted Successfully"}, status=200)

    else:
        return HttpResponseNotAllowed(["DELETE"])
