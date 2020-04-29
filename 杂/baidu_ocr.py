from aip import AipOcr

APP_ID = '11538030'
API_KEY = 'qFXoApbGYFpeNUgRrVhHFBz6'
SECRET_KEY = 'dzA3hD7CgQ6529uYuwlqV448MOYCq7Bf'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_text(option):
    with open ('picture.png','rb') as f:
        picture=f.read()
    try:
        response=client.basicGeneral(picture)
        texts=response["words_result"]
        allText=''
        for text in texts:
            if option:
                allText+=(text['words']+'\n')
            else:
                allText+=(text['words'])
        print(allText)
    except:
        allText='网络垃圾，再试一次啦！！！'
        print(allText)
    finally:
        return allText


if __name__ == "__main__":
    get_text()