from rest_framework.views import APIView
from .models import StudentModel
from django.http import JsonResponse
from redis_helper import RedisCacheManager
from django.forms.models import model_to_dict
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
import json


class StudentViewset(APIView):
    def __init__(self, cache_key="STUDENT", **kwargs):
        super().__init__(**kwargs)
        self.cache_key = cache_key
        self.rec_per_page = 5
        self.page_no = 1

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST["data"])
        try:
            model = StudentModel.objects.create(**data)
            self.cache_key = self.cache_key + str(model.id)
            redis_ob: RedisCacheManager = RedisCacheManager()
            redis_ob.connect()
            redis_obj = model_to_dict(model)
            redis_obj["created_on"] = model.created_on
            redis_obj["last_updated_on"] = model.last_updated_on
            if not redis_ob.has_cache_key(self.cache_key):
                redis_ob.put_obj_in_cache(self.cache_key, redis_obj)
            return JsonResponse(build_response(status.HTTP_201_CREATED, {'id': model.id}))
        except Exception as ex:
            return JsonResponse({'message': 'Email ID already Exists'}, status=403)

    def get(self, request):
        pk = request.GET.get("id")
        self.rec_per_page = request.GET.get("rec_per_page", self.rec_per_page)
        self.page_no = request.GET.get("page_no", self.page_no)
        redis_ob = RedisCacheManager()
        redis_ob.connect()
        if pk:
            self.cache_key = self.cache_key + pk
            if redis_ob.has_cache_key(self.cache_key):
                redis_data = redis_ob.get_object_cache(self.cache_key)
                return JsonResponse(build_response(status.HTTP_200_OK, redis_data))
            else:
                returned_data = StudentModel.objects.get(pk=pk)
                return JsonResponse(build_response(status.HTTP_200_OK, model_to_dict(returned_data)), safe=False)
        else:
            pattern = 'STUDENT*'
            data_list = redis_ob.get_pattern_keys(pattern)
            sorted_data = sorted(data_list, key=lambda k: k["id"])
            paginator = Paginator(sorted_data, self.rec_per_page)
            page = paginator.get_page(self.page_no)
            return JsonResponse(build_response(status.HTTP_200_OK, list(page)), safe=False)

    def patch(self, request, *args, **kwargs):
        data = request.POST.get("data", None)
        data = json.loads(data)
        pk = data.get("id", None)
        try:
            instance: StudentModel = StudentModel.objects.get(id=pk)
        except Exception as ex:
            raise ex

        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        returned_data = model_to_dict(instance)
        returned_data["created_on"] = instance.created_on
        returned_data["last_updated_on"] = instance.last_updated_on
        self.cache_key = self.cache_key + str(pk)
        redis_ob = RedisCacheManager()
        redis_ob.connect()
        if redis_ob.has_cache_key(self.cache_key):
            redis_ob.put_obj_in_cache(self.cache_key, returned_data)
        return JsonResponse(build_response(status.HTTP_200_OK, returned_data))

    def delete(self, request, *args, **kwargs):
        pk = request.POST.get("id", None)
        instance: StudentModel = StudentModel.objects.get(id=pk)
        instance.delete()
        self.cache_key = self.cache_key + pk
        redis_ob = RedisCacheManager()
        redis_ob.connect()
        if redis_ob.has_cache_key(self.cache_key):
            redis_ob.delete_key(self.cache_key)
        return JsonResponse(build_response(status.HTTP_200_OK, {"id": pk}))


class StudentListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rec_per_page = 5
        self.page_no = 1

    def get(self, request):
        pk = request.GET.get("id", None)
        email = request.GET.get("email", None)
        created_date = request.GET.get("created_date", None)
        dob = request.GET.get("dob", None)
        is_active = request.GET.get("is_active", None)
        gender = request.GET.get("gender", None)
        self.rec_per_page = request.GET.get("rec_per_page", self.rec_per_page)
        self.page_no = request.GET.get("page_no", self.page_no)
        filters = {}
        if email:
            filters["email"] = email
        if created_date:
            filters["created_on"] = created_date
        if dob:
            filters["dob"] = dob
        if is_active:
            filters["is_active"] = is_active
        if gender:
            filters["gender"] = gender
        filtered = StudentModel.objects.filter(Q(**filters)).order_by('id')
        paginator = Paginator(filtered.values(), self.rec_per_page)
        page = paginator.get_page(self.page_no)
        if not filtered:
            return JsonResponse({"status": "No Matchs"})
        return JsonResponse(build_response(status.HTTP_200_OK, list(page)), safe=False)


def build_response(status_code, data):
    if isinstance(data, list):
        return {"response_code": status_code, "total_records": len(data), "data": data}
    else:
        return {"response_code": status_code, "total_records": 1, "data": data}
