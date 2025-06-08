from django.http import JsonResponse, Http404, HttpResponseNotAllowed, HttpResponse
from ...models import Inventory, Medicine
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
            return JsonResponse(
                {"message": "The Medicine is already Active"}, status=200
            )
            
        return JsonResponse({"message": "Inventory Created Successfully"}, status=200)

    return JsonResponse({"message": "Method not allowed"}, status=405)


def get_all_inventories(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    query_set = Inventory.objects.all()
    data = serializers.serialize("json", query_set)
    return HttpResponse(data)


def get_single_inventory(request, inventory_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:

        inventory = Inventory.objects.select_related("medicine_id").get(pk=inventory_id)

        data = {
            "id": inventory.id,
            "medicine_id": inventory.medicine_id.id,
            "medicine_name": inventory.medicine_id.medicine_name,
            "medicine_desc": inventory.medicine_id.medicine_desc,
            "medicine_measurement": inventory.medicine_measurement,
            "medicine_price": inventory.medicine_price,
            "medicine_type": inventory.medicine_type,
            "manufacturer": inventory.manufacturer,
            "expiration_date": inventory.expiration_date,
            "medicine_type": inventory.medicine_type,
            "onActive": inventory.onActive,
            "quantity": inventory.quantity,
            "created_at": inventory.created_at,
            "deleted_at": inventory.deleted_at,
        }

        return JsonResponse(data, status=200, safe=False)

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

                
            return JsonResponse({"message" : "Inventory Updated Successfully"}, status=200)

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
             return JsonResponse({"message" : "Inventory Id does not Exist "}, status=500)
        inventory.delete()
        return JsonResponse({"message": "Inventory Deleted Successfully"}, status=200)
    
    else: 
        return HttpResponseNotAllowed(["DELETE"])