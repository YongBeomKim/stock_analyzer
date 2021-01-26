import requests

# http://127.0.0.1:8000/rest_api/user/10/

class ReqBase:
    def __init__(self):
        self.url = 'https://localhost.com/rest_api/'
        self.data = None

    def send_get(self):
        res = requests.get(self.url)
        return self._ret(res)

    def send_post(self):
        res = requests.post(self.url, json=self.data)
        return self._ret(res)

    def send_put(self):
        res = requests.put(self.url, json=self.data)
        return self._ret(res)

    def send_patch(self):
        res = requests.patch(self.url, json=self.data)
        return self._ret(res)

    def send_delete(self):
        res = requests.delete(self.url)
        return self._ret(res)

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


class RetrieveItemReq(ReqBase):

    pass


class DeleteItemReq(ReqBase):
    pass


class UpdateItemReq(ReqBase):
    pass


class InsertItemReq(ReqBase):
    pass
