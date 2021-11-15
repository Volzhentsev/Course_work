import json
import requests
import time
from tqdm import tqdm
from pprint import pprint
with open('access.txt', 'r') as f:
    vk_token = f.read().strip()

class VKUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, vk_token, version):
        self.params = {
            'access_token': vk_token,
            'v': version
        }

    def get_foto(self, user_id):
        foto_url = self.url + 'photos.get'
        foto_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 'likes',
            'photo_sizes': 1
        }
        req = requests.get(foto_url, params={**self.params, **foto_params}).json()
        foto = {}
        req = req['response']['items']
        for el in tqdm(req):
            time.sleep(1)
            if str(el['likes']['count']) in foto:
                foto[str(el['likes']['count']) +'-' + str(el['date'])] = str(el['sizes'][-1]['url']), str(el['sizes'][-1]['type'])
            else:
                foto[str(el['likes']['count'])] = str(el['sizes'][-1]['url']), str(el['sizes'][-1]['type'])
        return foto

def get_info_file(dict):
    info_file = []
    for k, v in tqdm(dict.items()):
        time.sleep(1)
        info_file.append({'file_name': k, 'size': v[1]})
    print(info_file)
    with open('data.txt', 'w') as f:
        json.dump(info_file, f, ensure_ascii=False, indent=2)

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload(self, foto_dict):
        for k, v in tqdm(foto_dict.items()):
            time.sleep(1)
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = self.get_headers()
            params = {"path": "/netology/" + k + ".jpg",
                      "url": v[0],
                      "overwrite": "true"}
            response = requests.post(url=url, headers=headers, params=params)
            res = response.json()
        print(response.status_code)
        print(res)

if __name__ == '__main__':
    user_id = None
    vk_client_photo = VKUser(vk_token, '5.131')
    i = vk_client_photo.get_foto(user_id)
    pprint(i)
    get_info_file(i)
    ya_token = 'AQAAAABaHNkNAADLW_Vtj3l1T0uXrsv96Tg3UsI'
    uploader = YaUploader(ya_token)
    uploader.upload(i)
