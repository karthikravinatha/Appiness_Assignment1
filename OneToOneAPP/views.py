from django.shortcuts import render
from rest_framework.views import APIView
import json
from rest_framework import status
from utils import build_json_response, build_response
from .models import UserModel, UserAddress
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Create your views here.
class OneToOneViews(APIView):
    def post(self, request, *args, **kwargs):
        data = request.POST.get("data", None)
        if data:
            data = json.loads(data)
            user_address = data.pop("address")
            try:
                user_model = UserModel.objects.create(**data)
                address_model = UserAddress.objects.create(user=user_model, address=user_address["address"],
                                                           street=user_address["street"],
                                                           pincode=user_address["pincode"])
                response_data = {
                    "message": "Created",
                    "id": user_model.id
                }
                return JsonResponse(build_response(status.HTTP_201_CREATED, response_data), safe=False)
            except Exception as ex:
                return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}), safe=False)
        else:
            return JsonResponse(
                build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, Exception("Data not exists in the request")),
                safe=False)

    def get(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(id=1)
            address = UserAddress.objects.get(id=1)
            return JsonResponse(build_response(status.HTTP_200_OK, model_to_dict(address)), safe=False)
        except Exception as ex:
            raise ex
