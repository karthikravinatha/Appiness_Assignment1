from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
import PyPDF2

from utils import build_response, generate_pdf


# Create your views here.
class PdfParserViews(APIView):

    def post(self, request, *args, **kwargs):
        request_file = request.FILES.get("pdf_file")
        retrieval_type = request.POST.get("retrieval_type", None)
        file_obj = request_file.open()
        char_string = ""
        word_string = ""
        line_string = ""
        rejection = ['\n', '\t', ',', ' ']
        # with open(request_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file_obj)
        if retrieval_type:
            if retrieval_type == "character":
                try:
                    for page in reader.pages:
                        text = page.extract_text()
                        text = str(text).strip()
                        for each_char in text:
                            cnt = 1
                            if each_char not in rejection:
                                char_string += str(each_char)
                    pdf_data = generate_pdf(input_data=char_string)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": pdf_data}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            elif retrieval_type == "word":
                try:
                    rejection.pop(-1)
                    for page in reader.pages:
                        text = page.extract_text()
                        strip_data = str(text).strip()
                        # word_string += strip_data
                        for each_word in strip_data:
                            if each_word not in rejection:
                                word_string += str(each_word)
                    text = word_string.split(" ")
                    pdf_data = generate_pdf(input_data=text)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": pdf_data}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            elif retrieval_type == "line":
                try:
                    for page in reader.pages:
                        text = page.extract_text()
                        strip = str(text).strip()
                        line_string += strip
                        # for each_line in text:
                        #     line_string += str(each_line) + "\n"
                    line_string = line_string.split("\n")
                    pdf_data = generate_pdf(line_string)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": pdf_data}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            elif retrieval_type == "page":
                paths = []
                try:
                    page_dict = {}
                    for page in reader.pages:
                        text = page.extract_text()
                        page_data = str(text).strip()
                        page_data = str(text).split("\n")
                        pdf_data = generate_pdf(page_data)
                        paths.append(pdf_data)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": paths}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            else:
                return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
