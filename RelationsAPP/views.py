from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import RelationsHeaderModel
from .models import RelationsDetailModel
from utils import build_response
from django.db.transaction import commit, set_rollback
from django.contrib import messages
import json


class RelationsView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.POST.get("data", None)
        if data:
            data = json.loads(data)
        detail_data = data.pop("detail")
        try:
            header = RelationsHeaderModel.objects.create(**data)
            for i in detail_data:
                detail_data = RelationsDetailModel.object.create(invoice_header_id=header,
                                                                 category_id=i["category_id"],
                                                                 quantity=i["quantity"],
                                                                 uom=i["uom"], price=i["price"], tax=i["tax"],
                                                                 total=i["total"])
            commit()
            return JsonResponse(build_response(status.HTTP_201_CREATED, {"id": header.pk}))
        except Exception as Ex:
            set_rollback(True)
            return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(Ex)))

    def get(self, request, *args, **kwargs):
        print("View is called")
        # raise Exception("Exception triggered")
        # data = RelationsHeaderModel.objects.filter()
        data = RelationsHeaderModel.objects.all()
        # raise Exception
        return JsonResponse(build_response(status.HTTP_200_OK, list(data.values())))
