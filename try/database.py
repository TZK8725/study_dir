import leancloud
import asyncio, time
import grequests


def post(class_name:str, data_key:str, data):

    leancloud.init("tLdWjcuTkiqUOSN33wknu4Xw-gzGzoHsz", "Jkj5V5zCR7MeV3tWMq8JUJse")
    DataBase = leancloud.Object.extend(class_name)
    db = DataBase()
    db.set(data_key, data)

    db.save()

async def post_database(data:dict, class_name="Unlock"):

    leancloud.init("tLdWjcuTkiqUOSN33wknu4Xw-gzGzoHsz", "Jkj5V5zCR7MeV3tWMq8JUJse")
    DataBase = leancloud.Object.extend(class_name)
    db = DataBase()
    db.set("detail", data)
    db.save()
    print("post done")

async def time_sleep(x):

    await asyncio.sleep(x)
    print("sleep done")

data = {
    "time" : "123",
    "successful" : False,
    "img" : "www.dadasdada.com"
}
loop = asyncio.get_event_loop()
start = time.time()
loop.run_until_complete(asyncio.gather( time_sleep(10), post_database(data)))
print(time.time()-start)

