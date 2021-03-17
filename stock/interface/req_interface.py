import requests

# http://127.0.0.1:8000/rest_api/user/10/
from django.views.decorators.csrf import csrf_exempt


class BaseReq:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/rest_api/'
        self.login_url = self.url + 'auth/login/'
        # 2021.02.14.hsk : 추후에 screts.json으로 통합
        self.id = 'admin'
        self.password = 'admin'
        self.data = None
        self.client, self.login_res = self._login(self.login_url, self.id, self.password)
        
    @staticmethod
    def _login(login_url, id, password):
        client = requests.session()
        client.get(login_url)
        csrf_token = client.cookies['csrftoken']
        login_data = {'Username': id, 'Password': password, 'csrfmiddlewaretoken': csrf_token}
        login_res = client.post(login_url, data=login_data)
        return client, login_res

    @staticmethod
    def _ret(res):
        if res.status_code in (200, 201):
            return res
        else:
            print('Status Code : [{0}]'.format(res.status_code))

    def set_param(self, data):
        self.data = data

    def get_param(self):
        return self.data


class BaseCreate(BaseReq):
    def __init__(self):
        super().__init__()

    @csrf_exempt
    def send_post(self):
        res = self.client.post(self.url, json=self.data)  # self.client(현재 활성화된 로그인 세션)를 사용한 요청
        res = self._ret(res)
        print(res, datum)


class BaseRead(BaseReq):
    def __init__(self):
        super().__init__()

    def send_get(self):
        res = self.client.get(self.url)
        return self._ret(res)


class BaseUpdate(BaseReq):
    """
    2021.02.14.hsk : 추후 변경 필요
    """
    def __init__(self):
        super().__init__()

    def send_put(self):
        res = self.client.put(self.url, json=self.data)
        return self._ret(res)

    def send_patch(self):
        res = self.client.patch(self.url, json=self.data)
        return self._ret(res)


class BaseDelete(BaseReq):
    """
    2021.02.14.hsk : 추후 변경 필요
    """
    def __init__(self):
        super().__init__()

    def send_delete(self):
        res = self.client.delete(self.url)
        return self._ret(res)

class CreateMarketReq(BaseCreate):
    def __init__(self):
        super().__init__()
        self.url += 'market/'


# 주식시장
class ReadMarketReq(BaseRead):
    def __init__(self):
        super().__init__()
        self.url += 'market/'


class UpdateMarketReq(BaseUpdate):
    def __init__(self):
        super().__init__()
        self.url += 'market/'


class DeleteMarketReq(BaseDelete):
    def __init__(self):
        super().__init__()
        self.url += 'market/'


# 주식종목
class CreateItemListReq(BaseCreate):
    def __init__(self):
        super().__init__()
        self.url += 'item_list/'


class ReadItemListReq(BaseRead):
    def __init__(self, stock_market_name):
        super().__init__()
        self.url += ('item_list/?stock_market_name=' + stock_market_name)


class UpdateItemListReq(BaseUpdate):
    def __init__(self):
        super().__init__()
        self.url += 'item_list/'


class DeleteItemListReq(BaseDelete):
    def __init__(self):
        super().__init__()
        self.url += 'item_list/'


# 주식종목 데이터
class CreateItemReq(BaseCreate):
    def __init__(self):
        super().__init__()
        self.url += 'item/'


class ReadItemReq(BaseRead):
    def __init__(self):
        super().__init__()
        self.url += 'item/'


class UpdateItemReq(BaseUpdate):
    def __init__(self):
        super().__init__()
        self.url += 'item/'


class DeleteItemReq(BaseDelete):
    def __init__(self):
        super().__init__()
        self.url += 'item/'
