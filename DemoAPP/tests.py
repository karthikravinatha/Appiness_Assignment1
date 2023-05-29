# Created by Karthik Ravinatha at 1:05 pm 25/05/23 using PyCharm
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class StudentCreateApiViewTestCase(APITestCase):
    url = reverse('student')

    def setUp(self):
        self.test_session = self.client.session

    def test_student_create(self):
        response = self.client.post(self.url, {
            "data": {
                "first_name": "react1",
                "last_name": "nagdgdgtive",
                "email": "test14@gmail12.com",
                "dob": "2023-06-06",
                "gender": "Male"
            }
        }, format='json')
        print("test")
        print(response.content)
        res_dict = json.loads(response.content.decode('utf-8'))
        self.test_session["inserted_id"] = res_dict["data"]["id"]
        self.test_session.save()

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_student_get(self):
        # print("GET", type(self.test_session))
        # print("GET", self.test_session.GET.get("inserted_id"))
        response = self.client.get(self.url, {"id": 1})
        print("test - GET")
        print(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
