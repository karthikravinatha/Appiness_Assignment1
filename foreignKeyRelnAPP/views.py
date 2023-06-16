from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import AuthorModels, BookModel
from django.http import JsonResponse, HttpResponse
import json
from django.core import serializers
from utils import build_response
from django.forms.models import model_to_dict


# Create your views here.


class AuthorViews(APIView):
    def post(self, request, *args, **kwargs):
        data = request.POST.get("data", None)
        if data:
            data = json.loads(data)
            author_model = AuthorModels(**data)
            author_model.save()
            response_data = {
                "message": "Created",
                "status": status.HTTP_201_CREATED,
                "id": author_model.id
            }
            return JsonResponse(build_response(status.HTTP_201_CREATED, response_data), safe=False)
        else:
            return JsonResponse(build_response(status.HTTP_204_NO_CONTENT, {}), safe=False)

    def get(self, request, *args, **kwargs):
        author = AuthorModels.objects.get(id=1)
        return JsonResponse(build_response(status.HTTP_200_OK, model_to_dict(author)))


class BookViews(APIView):
    def post(self, request, *args, **kwargs):
        data = request.POST.get("data", None)
        if data:
            data = json.loads(data)
            author_model = AuthorModels.objects.get(id=1)
            book_model = BookModel(author=author_model, book_name=data['book_name'])
            book_model.save()
            response_data = {
                "message": "Created",
                "status": status.HTTP_201_CREATED,
                "id": book_model.id
            }
            return JsonResponse(response_data, safe=False)

    def get(self,*args, **kwargs):
        # book_data = BookModel.objects.get(id=1)
        # author = AuthorModels.objects.prefetch_related("book_name").get(id=1)
        author = AuthorModels.objects.all().prefetch_related("book").get(id=1)
        # json_data = serializers.serialize('json', [author], use_natural_foreign_keys=True)
        # books = author.book.all()
        # json_data = json.dumps(model_to_dict(author))
        # return HttpResponse(json_data, content_type='application/json')
        # s = author.book_name.all()
        data = {
            'id': author.id,
            'name': author.author_name,
            'books': [
                {
                    'id': b.id,
                    'title': b.book_name
                }
                for b in author.book.all()
            ]
        }
        # json_data = json.dumps(data)
        return JsonResponse(data, safe=False)
