import requests

def send():
    requests.post(
        "https://api.alertover.com/v1/alert",
        data={
            "source": "s-40960cea-419e-4670-bc2f-c48829a5",
            "receiver": "g-20671ffc-7c02-4e74-bd13-1060cc3f",
            "content": "你好",
            "title": "hello",
            "url": "https://sm.ms/image/qdhsaTBceE4O5pZ"
        }
    )

def get_content():

    # token_response = requests.post("https://sm.ms/api/v2/token", data={
    #     "username" : "tangzekun",
    #     "password" : "LZS...1230"
    # })
    # print(token_response.json())
    # token = token_response.json()["data"]["token"]
    with open(r"G:\onedrive\图片\证件\证件照.jpg", "rb") as f:
        image = f.read()

    header = {
        "Content-Type": "multipart/form-data",
        "Authorization": "WL2weyAtF3X7jNipIeZMMOqwuY0nKIHh"
        }
    param = {"smfile": image}

    response = requests.post("https://sm.ms/api/v2/upload", files=param, data=header)
    print(response.json())
    if response.json()["success"]:
        image_url = response.json()["data"]["url"]
        print(imaga_url)


get_content()
