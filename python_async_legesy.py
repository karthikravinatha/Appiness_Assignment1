# # Created by Karthik Ravinatha at 9:06 am 09/06/23 using PyCharm
import time

import requests
# import asyncio
# import time
#
#
# async def main():
#     print("main start...")
#     time.sleep(5)
#     print("main end...")
#
#
# async def master():
#     print("master start")
#     asyncio.create_task(main())
#     print("master end")
#
#
# asyncio.run(master())

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

start = time.time()
res_list = []
for i in url_list:
    response = requests.get(i)
    res_list.append(response)
end = time.time()
print(end - start)


