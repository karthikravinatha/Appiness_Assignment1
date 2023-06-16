# Created by Karthik Ravinatha at 9:51 am 09/06/23 using PyCharm
import asyncio

class Asyncronus:
    def normal_methos(self):
        print("normal method")

    async def asyncio_method(self):
        print("async method start")
        print("async method end")


async def main():
    my_obj = Asyncronus()
    result = await my_obj.asyncio_method()

asyncio.run(main())
