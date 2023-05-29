import time
from urllib.parse import urlparse, urljoin
import bs4
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max, Sum, Subquery, F, Count
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import url_validate, build_response
from .models import DoorsHeaderModel, DoorsDetailModel
from redis_helper import RedisCacheManager


class GrabDoorsView(APIView):
    def __init__(self, cache_key="IND_MART_DOORS", **kwargs):
        super().__init__(**kwargs)
        self.cache_key = cache_key
        self.rec_per_page = 5
        self.page_no = 1
        self.redis_object = RedisCacheManager()
        self.redis_object.connect()

    def post(self, request, *args, **kwargs):
        request_url = request.POST.get("url", None)
        parsed_url = urlparse(request_url)
        domain_url = parsed_url.scheme + "://" + parsed_url.netloc
        doors = []
        # sss = self.get_sub_category_details("https://dir.indiamart.com/impcat/dutch-doors.html", "")
        soup = selenium_method(request_url)
        elements = soup.find_all('a', {'class': "clr4 db"})
        for i in elements:
            detail_url = i["href"]
            door_type = i.text
            if url_validate(detail_url):
                gsc = self.get_sub_category_details(detail_url, "f-div r-e-h ft bdr1 ")
            else:
                detail_url = urljoin(domain_url, detail_url)
                gsc = self.get_sub_category_details(detail_url, "f-div r-e-h ft bdr1 ")
            db_insert = {"url": detail_url, "door_type": door_type, "detail_category": gsc}
            insert_header = DoorsHeaderModel.objects.create(type=db_insert["door_type"], url=db_insert["url"])
            header_dict = model_to_dict(insert_header)
            header_id = insert_header.id
            header_dict["created_on"] = insert_header.created_on
            header_dict["last_updated_on"] = insert_header.last_updated_on
            detail_data = db_insert["detail_category"]
            detail_dict_list = []
            if detail_data:
                for each_data in detail_data:
                    insert_detail = DoorsDetailModel.objects.create(
                        header_id=header_id, sub_category_name=each_data["sub_category_name"],
                        price=each_data["price"], seller_name=each_data["sellar"],
                        seller_description=each_data["lead0"], seller_rating=each_data["sellar_rating"]
                    )
                    detail_dict = model_to_dict(insert_detail)
                    detail_dict_list.append(detail_dict)
                header_dict["detail_category"] = detail_dict_list
            cache_key = self.cache_key
            cache_key = cache_key + str(header_id)
            if not self.redis_object.has_cache_key(cache_key):
                self.redis_object.put_obj_in_cache(cache_key, header_dict)
            doors.append(header_dict)
        return JsonResponse(build_response(status.HTTP_201_CREATED, "Sucess"), safe=False)

    def get(self, request, *args, **kwargs):
        pk = request.GET.get("id", None)
        type = request.GET.get("type", None)
        self.rec_per_page = request.GET.get("rec_per_page", self.rec_per_page)
        self.page_no = request.GET.get("page_no", self.page_no)
        if pk:
            cache_key = self.cache_key + str(pk)
            if self.redis_object.has_cache_key(cache_key):
                returned_data = self.redis_object.get_object_cache(cache_key)
                return JsonResponse(build_response(status.HTTP_200_OK, returned_data), safe=False)
            else:
                get_qs = DoorsHeaderModel.objects.get(id=pk)
                header = model_to_dict(get_qs)
                returned_data = []
                if isinstance(header, list):
                    for i in header:
                        try:
                            get_detail_qs = DoorsDetailModel.objects.filter(header_id=i["id"])
                            i["detail_category"] = list(get_detail_qs.values())
                            returned_data.append(i)
                        except Exception as ex:
                            pass
                else:
                    header["detail_category"] = []
                    returned_data.append(header)
                return JsonResponse(build_response(status.HTTP_200_OK, returned_data), safe=False)
        else:
            if type:
                if type == "*":
                    get_qs = DoorsHeaderModel.objects.all().order_by("id")
                    header = list(get_qs.values())
                    returned_data = []
                    for i in header:
                        try:
                            get_detail_qs = DoorsDetailModel.objects.filter(header_id=i["id"])
                            i["detail_category"] = list(get_detail_qs.values())
                            returned_data.append(i)
                        except Exception as ex:
                            pass
                    paginator = Paginator(returned_data, self.rec_per_page)
                    page = paginator.get_page(self.page_no)
                    return JsonResponse(build_response(status.HTTP_200_OK, list(page)), safe=False)
                else:
                    filters = {}
                    if type:
                        filters["type"] = type
                    get_qs = DoorsHeaderModel.objects.filter(Q(**filters)).order_by("id")
                    header = list(get_qs.values())
                    returned_data = []
                    for i in header:
                        try:
                            get_detail_qs = DoorsDetailModel.objects.filter(header_id=i["id"])
                            i["detail_category"] = list(get_detail_qs.values())
                            returned_data.append(i)
                        except Exception as ex:
                            pass
                    paginator = Paginator(returned_data, self.rec_per_page)
                    page = paginator.get_page(self.page_no)
                    return JsonResponse(build_response(status.HTTP_200_OK, list(page)), safe=False)
            else:
                pattern = self.cache_key + "*"
                data_list = self.redis_object.get_pattern_keys(pattern)
                sorted_list = sorted(data_list, key=lambda k: k["id"])
                paginator = Paginator(sorted_list, self.rec_per_page)
                page = paginator.get_page(self.page_no)
                return JsonResponse(build_response(status.HTTP_200_OK, list(page)))

    def delete(self, request, *args, **kwargs):
        header: DoorsHeaderModel = DoorsHeaderModel.objects.all()
        header.delete()
        detail: DoorsDetailModel = DoorsDetailModel.objects.all()
        detail.delete()
        cache_key = self.cache_key
        pattern = cache_key + "*"
        redis_keys = self.redis_object.get_pattern_keys(pattern)
        for i in redis_keys:
            key = cache_key + str(i["id"])
            op = self.redis_object.delete_key(key)
        return JsonResponse(build_response(status.HTTP_200_OK, "Success"))

    def get_sub_category_details(self, url, key_element):
        soup = selenium_method(url)
        detail_list = []
        try:
            elements = soup.find_all('div', {'class': "rht"})
            elements1 = soup.find_all('div', {'class': "r-cl"})
        except:
            pass
        for i in range(len(elements)):
            try:
                sub_name = elements[i].find('span', class_='lg').text
            except:
                pass
            try:
                price = elements[i].find('span', class_='prc').text
                price = str(price).replace("\xa0", "")
            except:
                pass
            try:
                sellar = elements1[i].find('a').text
            except:
                pass
            try:
                lead = elements1[i].find_all('p', class_='ig')
                lead0 = lead[0].find('span').text
            except:
                pass
            try:
                sellar_rating = elements1[i].find('span', class_='bg').text
            except:
                pass
            if sellar_rating == lead0:
                lead0 = ""
            detail_list.append({
                "sub_category_name": sub_name,
                "price": price,
                "sellar": sellar,
                "lead0": lead0,
                "sellar_rating": sellar_rating
            })
        return detail_list


class GrabDoorTypesView(APIView):
    def get(self, request, *args, **kwargs):
        data = DoorsHeaderModel.objects.all().values('id', 'type')
        # data = DoorsHeaderModel.objects.aggregate(Sum('id'))
        returned_data = list(data.union(data))

        # header = DoorsHeaderModel.objects.order_by('id')
        # detail = DoorsDetailModel.objects.filter(header_id=182).values('header_id').annotate(header_id_count=Count('header_id'))
        detail = DoorsDetailModel.objects.values('header_id').annotate(
            header_id_count=Count("header_id")).filter(header_id_count__gt=1)  # .order_by()
        return JsonResponse(build_response(status.HTTP_200_OK, list(detail)))


def selenium_method(url):
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('-no-sandbox')
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    try:
        driver.get(url)
        time.sleep(2)
        content = driver.page_source
        soup = bs4.BeautifulSoup(content, "html.parser")
    except TimeoutError:
        soup = "Loading took too much time!"
    except Exception as e:
        soup = "Something went wrong while parsing URL!"
    driver.quit()
    return soup
