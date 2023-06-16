from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
import PyPDF2
from io import StringIO

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
        hyper_link = "© www.englishgrammar.org"
        # with open(request_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file_obj)
        if retrieval_type:
            if retrieval_type == "character":
                try:
                    for page in reader.pages:
                        text = page.extract_text()
                        text = str(text).strip()
                        text = text.replace(hyper_link, " ")
                        for each_char in text:
                            cnt = 1
                            if each_char not in rejection:
                                char_string += str(each_char)
                            else:
                                char_string += str("")
                        char_string += " " + hyper_link + " "
                    pdf_data = generate_pdf(input_data=char_string)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": pdf_data}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            elif retrieval_type == "word":
                try:
                    page_list = []
                    rejection.pop(-1)
                    for page in reader.pages:
                        word_string1 = ""
                        text = page.extract_text()
                        # strip_data = str(text).strip()
                        strip_data = text.replace("\n", " ")
                        strip_data = text.replace(hyper_link, " ")
                        # word_string += strip_data

                        for each_word in strip_data:
                            if each_word not in rejection:
                                word_string += str(each_word)
                                # word_string1 += str(each_word)
                            else:
                                word_string += str(" ")
                        word_string += " " + hyper_link + " "
                        # page_list.append(word_string1.split(' '))
                    text = str(word_string)
                    # text = StringIO(word_string)
                    text = word_string.split(" ")
                    pdf_data = generate_pdf(input_data=text)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": pdf_data}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            elif retrieval_type == "line":
                rejection = ['\n', '\t']
                try:
                    for page in reader.pages:
                        text = page.extract_text()
                        strip = str(text).strip()
                        strip = strip.replace(hyper_link, " ")
                        line_string += strip
                        for each_word in strip:
                            if each_word not in rejection:
                                word_string += str(each_word)
                            else:
                                if each_word == "\n":
                                    word_string += str(each_word)
                                else:
                                    word_string += str(each_word)
                        line_string += "\n"
                        # for each_line in text:
                        #     line_string += str(each_line) + "\n"
                    line_string += " " + hyper_link + " "
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
                        page_data = page_data.replace(hyper_link, " ")
                        page_data += "\n" + hyper_link + " "
                        page_data = str(page_data).split("\n")
                        pdf_data = generate_pdf(page_data)
                        paths.append(pdf_data)
                    return JsonResponse(build_response(status.HTTP_200_OK, {"data": paths}))
                except Exception as ex:
                    return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
            else:
                return JsonResponse(build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, {}))
