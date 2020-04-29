import leancloud


def post(class_name:str, data_key:str, data):

    leancloud.init("tLdWjcuTkiqUOSN33wknu4Xw-gzGzoHsz", "Jkj5V5zCR7MeV3tWMq8JUJse")
    DataBase = leancloud.Object.extend(class_name)
    db = DataBase()
    db.set(data_key, data)
    db.save()

def iter_post(data_list):

    leancloud.init("tLdWjcuTkiqUOSN33wknu4Xw-gzGzoHsz", "Jkj5V5zCR7MeV3tWMq8JUJse")
    DataBase = leancloud.Object.extend(class_name)
    db = DataBase()
    for data in data_list:
        for i in data:
            db.set()
    