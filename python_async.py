# Created by Karthik Ravinatha at 4:14 pm 08/06/23 using PyCharm
import time

import requests
import asyncio
import aiohttp

url_list = ["https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones",
            "https://dummyjson.com/products/category/smartphones"]


async def sub():
    start = time.time()
    response_list = []
    async with aiohttp.ClientSession() as session:
        for i in url_list:
            response = await asyncio.create_task(session.get(str(i), ssl=False))
            response_list.append(await response.json())
    end = time.time()
    print(end - start)
    return response_list

async def main():
    print("main called")
    res = await asyncio.create_task(sub())
    print(res)
    print("main returned")

print("start...")
asyncio.run(main())
print("end...")
