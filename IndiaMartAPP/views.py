import time
from urllib.parse import urlparse, urljoin

import bs4
from django.http import JsonResponse
from rest_framework.views import APIView
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class GrabDoorsView(APIView):
    def post(self, request, *args, **kwargs):
        url = request.POST.get("url", None)
        parsed_url = urlparse(url)
        domain_url = parsed_url.netloc
        doors = []
        gsc = get_sub_category_details("https://dir.indiamart.com/impcat/door.html", "f-div r-e-h ft bdr1 ")
        soup = selenium_method(url)
        # elements = soup.find_all('div', {'class': 'right-group flx1 df fww pr'})
        elements = soup.find_all('a', {'class': "clr4 db"})

        for i in elements:
            url = i["href"]
            door_type = i.text
            doors.append({"url": url, "door_type": door_type})
        print(doors)
        JsonResponse(doors, safe=False)


def get_sub_category_details(url, key_element):
    soup = selenium_method(url)
    detail_list = []
    try:
        elements = soup.find_all('div', {'class': "rht"})
        elements1 = soup.find_all('div', {'class': "r-cl"})
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
            sellar = elements1[i].find('a').text
            lead = elements1[i].find_all('p', class_='ig')
            lead0 = lead[0].find('span').text
            sellar_rating = elements1[i].find('span', class_='bg').text
            detail_list.append({
                "sub_category_name": sub_name,
                "price": price,
                "sellar": sellar,
                "lead0": lead0,
                "sellar_rating": sellar_rating
            })
            print(detail_list)
    except:
        pass
    print("FINAL * 3")
    print(detail_list)


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
