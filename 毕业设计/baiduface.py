import requests
import base64
import os


class BaiduFace():

    def __init__(self):
        self.ak = "6EdKHXpGto1Ger4agphehXjg"
        self.sk = "g99OC68xKlaFYgOgCXFd9t13pjAmE737"
        self.access_path = "./access.txt"
        self.user_dir = "./UserImage"

    def _get_token(self):

        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        self.ak, self.sk)
        response = requests.get(url)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            with open(self.access_path, "w") as f:
                f.write(access_token)
            return access_token

    def face_verify(self, unknown_image):
        # 活体检测模块
        with open(unknown_image, "rb") as f:
            uk_img = base64.b64encode(f.read()).decode()

        params = "[{\"image\": \"%s\", \"image_type\": \"BASE64\", \"option\": \"COMMON\" }]" % (uk_img)
        headers = {'content-type': 'application/json'}
        api = "https://aip.baidubce.com/rest/2.0/face/v3/faceverify?access_token="

        with open(self.access_path, "r") as f:
            access_token = f.read()
        response = requests.post(api + access_token, data=params, headers=headers)
        if response.json()["error_code"] == 110 or 111:
            access_token = self._get_token()
            response = requests.post(api + access_token, data=params, headers=headers)
        if response.json()["error_msg"] == "SUCCESS":
            score = response.json()["result"]["face_liveness"]
            face_token = response.json()["result"]["face_list"][0]["face_token"]
            return score, face_token, access_token
        else:
            return 0

    def face_compare(self, face_token, access_token):
        # 人脸验证模块
        name_list = [i.split(".")[0] for i in os.listdir(self.user_dir)]
        user_image_list = [os.path.join(self.user_dir, i) for i in os.listdir(self.user_dir)]
        params_list = list()
        for user_image in user_image_list:
            with open(user_image, "rb") as f:
                src_img = base64.b64encode(f.read()).decode()
            params = ["[{\"image\": \"%s\", \"image_type\": \"BASE64\", \"face_type\": \"CERT\"}," \
                     " {\"image\": \"%s\", \"image_type\": \"FACE_TOKEN\"}]" % (src_img, face_token)]

            params_list.append(params)

        api = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        score_list = list()
        for data in params_list:
            response = requests.post(api, data=data[0], headers=headers)

            if response.json()["error_msg"] == "SUCCESS":
                score = response.json()["result"]["score"]
                score_list.append(score)
                # print(response.json())
            else:
                print(response.json())
                return 0, "Unknown"
        return max(score_list), name_list[score_list.index(max(score_list))]


if __name__ == "__main__":

    face = BaiduFace()
    score, face_token, access_token = face.face_verify(r"C:\Users\TZK\Desktop\学习\unknow.jpg")
    print(score)
    face.face_compare(face_token, access_token)