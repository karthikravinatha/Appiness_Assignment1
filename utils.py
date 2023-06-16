# -*- coding: utf-8 -*-
import os
import re
import time
from textwrap import wrap

import PyPDF2
import bs4
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, inch
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.colors import blue, black
from reportlab.platypus import SimpleDocTemplate, Paragraph
from datetime import datetime
import unicodedata

from DemoProject.settings import BASE_DIR


def url_validate(url):
    # Regular expression pattern for URL validation
    pattern = re.compile(
        r'^https?://'
        r'(([A-Za-z0-9-]+)\.)+'
        r'([A-Za-z]{2,})'
        r'(:\d+)?'
        r'(\/\S*)?$'
    )
    return bool(re.match(pattern, url))


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


def build_response(status_code, data):
    if isinstance(data, list):
        return {"response_code": status_code, "total_records": len(data), "data": data}
    else:
        return {"response_code": status_code, "total_records": 1, "data": data}


def generate_pdf(input_data):
    path = os.path.join(BASE_DIR, "PdfParserAPP", "downloads")
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = "output" + datetime.now().strftime("%d-%m-%Y:%H:%M:%S:%f") + ".pdf"
    output_path = os.path.join(path, file_name)
    pdf_canvas = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    # left_margin = 0.5 * inch
    # right_margin = 0.5 * inch
    top_margin = 0.5 * inch
    # bottom_margin = 0.5 * inch

    y = height - top_margin
    ct = 1
    for row in input_data:
        y -= 0.5 * inch
        left_margin = 0.5 * inch
        if ct == 21:
            pdf_canvas.showPage()
            left_margin = 0.5 * inch
            # right_margin = 0.5 * inch
            top_margin = 0.5 * inch
            # bottom_margin = 0.5 * inch
            y = height - top_margin
            # y -= 0.2 * inch
            ct = 1
        if not row == "  " or row == "\n":
            pdf_canvas.drawString(left_margin, y, unicodedata.normalize("NFKD", str(row)))
        left_margin += width
        ct += 1

    pdf_canvas.save()
    return output_path
