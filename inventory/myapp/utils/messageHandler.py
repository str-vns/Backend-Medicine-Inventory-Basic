from django.http import JsonResponse, Http404, HttpResponseNotAllowed, HttpResponse


def handle_get_request(message_set):
    print('message Set:', message_set)
  
    return JsonResponse(message_set, safe=False)