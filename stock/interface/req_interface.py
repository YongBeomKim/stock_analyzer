import abc
import requests

# http://127.0.0.1:8000/rest_api/user/10/

class BaseReq:
    def __init__(self):
        self.url = 'https://localhost.com/rest_api/'
        self.data = None

    @staticmethod
    def _ret(res):
        if res.status_code == 200:
            return res
        else:
            print('[{0}] Error Occurred'.format(res.status_code))

    def set_param(self, data):
        self.data = data

    def get_param(self):
        return self.data

class BaseCreate(BaseReq):
    def send_post(self):
        res = requests.post(self.url, json=self.data)
        return self._ret(res)

class BaseRead(BaseReq):
    def send_get(self):
        res = requests.get(self.url)
        return self._ret(res)

class BaseUpdate(BaseReq):
    def send_put(self):
        res = requests.put(self.url, json=self.data)
        return self._ret(res)

    def send_patch(self):
        res = requests.patch(self.url, json=self.data)
        return self._ret(res)

class BaseDelete(BaseReq):
    def send_delete(self):
        res = requests.delete(self.url)
        return self._ret(res)

class CreateItemReq(BaseCreate):
    pass

class ReadItemReq(BaseRead):
    pass

class UpdateItemReq(BaseUpdate):
    pass

class DeleteItemReq(BaseDelete):
    pass
