# Stock
- 실시간으로 각 주식시장별 종목의 시세 조회 및 분석
- 누적된 데이터와 머신러닝 모델을 기반으로 주가 예측.  

위의 두 가지 기능을 중점으로 하는 웹 사이트를 목표로 합니다.

## 사용될 스택
- Django & DRF (Django Rest Framework)  
> 백엔드서버로써 사용합니다.  

- React.js & material ui
> 프론트엔드로써 사용합니다.  
 
- PyKrx
> 주가 정보 수집 모듈로써 사용됩니다.

- MongoDB  
> MongoDB를 채택한 이유는 스키마의 제약을 덜 받기 위함입니다. 

- Sklearn (Regression)  
> 주가 데이터를 회귀 분석을 통해 예측.  
Linear Regression > Ridge Regression > Lasso Regression  
전체적인 서비스가 구현이 되면 다른 모델을 도입하며 정확도를 높여나갈 예정입니다. 주가에 영향으 주는 독립변수(feature)들을 찾아야 합니다.  

- Matplotlib  
> 데이터 시각화 모듈.

## Case Rule  
클래스명 : Upper Camel case  
메소드, 속성 : Snake case

## 모듈 관리
모듈 관리는 requirements.txt를 통해 이루어진다.  
```
# 패키지 목록과 버전 텍스트로 저장하기
pip freeze > requirements.txt

# 텍스트 파일에 있는 패키지를 설치하기
pip install -r requirements.txt
```

## 계획 및 진행과정  

### 1. 백엔드서버 구축  
#### 1-1. 앱 설계  
django 프로젝트는 여러 app들로 구성되어 있다. 즉, 프로젝트는 하나의 웹사이트이고, 각 앱들은 하나의 웹사이트에 속해있는 기능들이라고 생각하면 된다. e.g) 게시판, 이메일, 결제..  
현재 진행할 주제에는 기능이 **실시간 주가 정보 조회, 주가 정보 예측**이 있다. 고로 두 가지의 앱을 생성할 것이다.  

```
python manage.py startapp stock_inquiry
python manage.py startapp stock_prediction
```  

2020-12-04 : API 서버로 사용할 rest_api 앱도 생성한다.  

```
python manage.py startapp rest_api
```


#### 1-2 모델 설계  
- 사용자 정보 모델 (즐겨찾기 종목 포함)  

```python
class Post(models.Model):
    user_name = models.CharField(max_length=200)
    # bookmark_item_list = models.CharField(max_length=200) # 연구중..

    def __str__(self):
        return self.user_name
```  

- 주식시장 모델  

```python
class StockMarket(models.Model):
    stock_market_name = models.CharField(primary_key=True, max_length=200)

    def __str__(self):
        return self.stock_market_name
```

- 주식종목 목록 모델
```python
class StockItemList(models.Model):
    stock_market_name = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    stock_item_name = models.CharField(primary_key=True, max_length=200)
    stock_item_code = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_item_name
```

- 주식종목 모델  

```python
class StockItem(models.Model):
    stock_item_name = models.ForeignKey(StockItemList, on_delete=models.CASCADE)
    reg_date = models.DateField(default=timezone.now(), null=True)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    open = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
```

#### 1-3. REST API 구현 (DRF 적용)  
DRF는 왜 쓸까? (참고 : https://medium.com/@whj2013123218/django-rest-api%EC%9D%98-%ED%95%84%EC%9A%94%EC%84%B1%EA%B3%BC-%EA%B0%84%EB%8B%A8%ED%95%9C-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95-a95c6dd195fd)  
1. 기존의 native django 방식대로 개발을 한다면 프론트 부분은 백엔드로부터 데이터를 받고 django template에 개발을 해야할 것이다. 이럴 경우, 백엔드와 프론트의 완전한 분리가 어렵다. 그래서 DRF를 사용하면 rest api가 사용가능하기 때문에 **django 백엔드와 react 프론트가 분리가 가능**하다.  
2. 재사용성이 좋아진다. view에서 바로 html로 넘기게 되면 view에는 비슷한 로직도 매번 class-based view로 작성해야 하는 비효율적인 상황이 연출된다. 그러나 api를 적용하면 해당 **api를 재사용**할 수 있다. 

```
pip install djangorestframework
```  

DRF를 설치한 후 settings.py에 다음과 같이 적어준다.  

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock_inquiry',
    'stock_prediction',
    'rest_framework', # DRF를 앱으로 등록
    'rest_api' # api 서버로 사용할 앱
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```  

rest_api앱에 urls.py를 생성한 뒤, 루트 urls.py에 다음과 같은 경로를 라우팅한다.  

```python
urlpatterns = [
    ...
    path('rest_api/', include('rest_api.urls')),
]
```  

그 다음 해당 모델을 serialize해야 한다.  
그 이유는 Django ORM의 Queryset은 Context로써 Django template으로 넘겨지며, HTML로 렌더링되어 Response로 보내지게 된다.
하지만 **JSON으로 데이터를 보내야 하는 RESTful API**는 HTML로 렌더링 되는 Django template를 사용할 수 없다. 그래서 Queryset을 Nested한 JSON
으로 매핑하는 과정을 거쳐야 하기 때문이다. (Queryset >> Json : Serialize)  

rest_api앱에 serializers.py를 작성해보자.  

```python
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import StockUser
from .models import StockMarket
from .models import StockItemList
from .models import StockItem



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class StockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUser
        fields = '__all__'


class StockMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMarket
        fields = '__all__'


class StockItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItemList
        fields = '__all__'


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'

```  

model과 serializer를 완성시켰으니 이제 view를 작성할 차례이다.  

(참고 : https://ssungkang.tistory.com/entry/Django-APIView-Mixins-generics-APIView-ViewSet%EC%9D%84-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90)  

DRF View 종류  
- CBV(Class-Based View, APIView 상속)
- FBV(Function-Based View, @api_view 데코레이터 사용)
- Mixin(요청마다 serializer 정의하는 것을 최소화)
- generic APIView
- ViewSet

rest_api/views.py  

```python
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets 

from .serializers import StockUserSerializer
from .serializers import StockMarketSerializer
from .serializers import StockItemListSerializer
from .serializers import StockItemSerializer


from .models import StockUser
from .models import StockMarket
from .models import StockItemList
from .models import StockItem


# Create your views here.
class StockUserViewSet(viewsets.ModelViewSet):
    queryset = StockUser.objects.all()
    serializer_class = StockUserSerializer


class StockMarketViewSet(viewsets.ModelViewSet):
    queryset = StockMarket.objects.all()
    serializer_class = StockMarketSerializer


class StockItemListViewSet(viewsets.ModelViewSet):
    queryset = StockItemList.objects.all()
    serializer_class = StockItemListSerializer

    def get_queryset(self):
        stock_market_name = self.request.query_params.get('stock_market_name', None)
        if stock_market_name is not None:
            self.queryset = self.queryset.filter(stock_market_name=stock_market_name)
        return self.queryset


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

    def get_queryset(self):
        stock_item_name = self.request.query_params.get('stock_item_name', None)
        if stock_item_name is not None:
            self.queryset = self.queryset.filter(stock_item_name=stock_item_name)
        return self.queryset

```  

url을 라우팅 시켜보자. viewset을 라우팅할 때에는 CBV, FBV, Mixin, GenericAPIView와는 다르게 router객체로 간편하게 등록할 수 있다.  
rest_api/urls.py  

```python
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StockUserViewSet
from .views import StockMarketViewSet
from .views import StockItemListViewSet
from .views import StockItemViewSet

router_user = DefaultRouter()
router_user.register('user', StockUserViewSet)

router_market = DefaultRouter()
router_market.register('market', StockMarketViewSet)

router_item_list = DefaultRouter()
router_item_list.register('item_list', StockItemListViewSet)

router_item = DefaultRouter()
router_item.register('item', StockItemViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router_user.urls)),
    path('', include(router_market.urls)),
    path('', include(router_item_list.urls)),
    path('', include(router_item.urls)),
]
```  

서버를 실행시킨 후, http://localhost:8000/rest_api/posts/에서 자세한 내용을 확인할 수 있다.  
DRF에 관련된 내용은 drf_tutorial을 확인하면 된다.  

위와 같은 방법으로 재사용이 가능한 어떤 REST API를 구현할까? **각 테이블(모델)에 CRUD API**  

#### 1-4. URL Patterns
현재 DRF의 ViewSets를 통해 요청 CRUD URL을 구현해놓은 상태이다. 그러나 코드의 추상화 수준이 너무 높아서 문서로 직접 정리를 하려고 한다.  

- 사용자 목록 조회
[GET] rest_api/user/  

- 사용자 추가  
[POST] rest_api/user/  

```
{
    "user_name": "Test"
}  
```  

- 특정 사용자 조회  
[GET] rest_api/user/[id]  

- 특정 사용자 정보 업데이트  
[PUT] rest_api/user/[id]  

```
{
    "id": 10,
    "user_name": "Test U"
}
```  

- 특정 사용자 제거  
[DELETE] rest_api/user/[id]  

사용자 이외의 다른 모델(market, item)도 같은 URL Pattern을 가진다.  

### 2. MongoDB 연동  
1. MongoDB 가입 -> 클러스터 생성 이후 하단의 그림과 같이 인증방식, DB 접근권한 등을 설정하여 Database user를 생성

![db1](https://user-images.githubusercontent.com/36228833/103440836-3dbf1f00-4c8c-11eb-8713-8c96c20b1b1c.PNG)

![db2](https://user-images.githubusercontent.com/36228833/103440843-4c0d3b00-4c8c-11eb-8fba-5fa45642e147.PNG)

2. 왼쪽 메뉴에 Network Access에 들어간 뒤 DB에 접근을 허용할 IP를 등록

![db3](https://user-images.githubusercontent.com/36228833/103440947-6562b700-4c8d-11eb-904e-4935f37f653e.PNG)

![dbdbdb](https://user-images.githubusercontent.com/36228833/103440950-6eec1f00-4c8d-11eb-9184-605af1f29c62.PNG)

**(스킵) Django 모델을 migration하는 과정에서 데이터베이스가 자동으로 생성되므로 스킵

![db4](https://user-images.githubusercontent.com/36228833/103440978-bb375f00-4c8d-11eb-9242-d394583a181c.PNG)

3. 첫 페이지로 돌아와서 현재 Cluster의 Connection string을 복사

![db5](https://user-images.githubusercontent.com/36228833/103440984-d1ddb600-4c8d-11eb-8ef9-97737853dfdc.PNG)

![db6](https://user-images.githubusercontent.com/36228833/103440994-ef128480-4c8d-11eb-9ef4-82e1bcbc3851.PNG)

4. connection string으로 mongoDB 연동을 위한 모듈들을 설치

```
$ pip install dnspython
$ pip install djongo
```

5. 장고 프로젝트 내 settings.py 에 mongoDB 연동을 위한 코드 작성

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        "CLIENT": {
           "name": "testDB",   # Database 이름입니다.
           "host": "mongodb+srv://admin:<password>@cluster0.lvfxw.mongodb.net/<dbname>?retryWrites=true&w=majority",   # 방금 복사한 Connection string
           "username": "admin",   # Database username
           "password": "admin",   # Database user's password
           "authMechanism": "SCRAM-SHA-1",   # 인증방식
        },
    }
}
```

6. migrate 명령어를 통해 모델의 변동사항을 데이터베이스에 적용

![db9](https://user-images.githubusercontent.com/36228833/103441103-fab27b00-4c8e-11eb-98d6-87eb8c1502ff.PNG)

7. 첫 페이지의 collections를 눌러 DB가 잘 연동되었는지 확인

![db8](https://user-images.githubusercontent.com/36228833/103441074-c212a180-4c8e-11eb-81b5-787bf727f28e.PNG)

### 2-1. settings.py 기밀정보 관리
settings.py 에는 secret_key, DB 정보 등 외부에 노출되면 안되는 기밀정보들을 담고있다.

SECRET_KEY의 용도 -- [출처](https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key)
- [암호화된 데이터 서명](https://docs.djangoproject.com/en/1.11/topics/signing/)을 포함하고 있다.
- 사용자 세션, 비밀번호 재설정 요청, 메시지 등을위한 고유 토큰을 포함하고 있다.

Django 앱에는 암호화 서명이 필요한 많은 것들이 있으며 'SECRET_KEY' 설정이 그 열쇠라고 볼 수 있다. 해당 기밀 정보들을 다음과 같이 json 파일로 관리하여 따로 호출하게끔 변경한다.

* secrets.json
```json
{
    "SECRET_KEY": "your SECRET_KEY",
    "DB_HOST" : "your DB Host",
    "DB_NAME" : "your DB name",
    "DB_USERNAME" : "your DB Username",
    "DB_PASSWORD" : "your DB Password"
}
```

* settings.py
```python
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """
    secrets.json을 통해 값을 가져온다.
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "secrets.json 파일에 {} 값이 존재하지 않습니다.".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
```

### 3. PyKrx를 통한 데이터 수집
#### 3-1 주식 종목 코드 수집
```python
class StockItemCodeCollector:
    def __init__(self):
        self.markets = ['KOSPI', 'KOSDAQ', 'KONEX', 'ALL']
        self.tickers = dict()
        for market in self.markets:
            self.tickers[market] = self.__collect_tickers(market)

    @staticmethod
    def __collect_tickers(market='KOSPI'):
        """
        stock.get_market_ticker_list()
        >> ['095570', '006840', '027410', '282330', '138930', ...]

        stock.get_market_ticker_name(ticker)
        >> SK하이닉스
        """
        tickers = dict()
        today = datetime.today().strftime("%Y%m%d")

        for ticker in stock.get_market_ticker_list(today, market):
            ticker_name = stock.get_market_ticker_name(ticker)
            tickers[ticker_name] = ticker
        return tickers

    def get_code(self, market, ticker_name):
        return self.tickers[market][ticker_name]
```
StockItemCodeCollector 인스턴스는 각 주식시장(KOSPI, KOSDAQ, KONEX, 전체)별로 딕셔너리에 각 종목의 이름과 코드를 보관하고 있다. get_code() 메소드를 통해 주식시장과 종목명을 입력하면 해당 종목 코드를 반환한다.  

#### 3-2 주식 종목 데이터 수집
```python
class StockItemDataFrameCollector:
    def __init__(self, code):
        self.code = code
        self.today = datetime.now()
        self.today_str = self.today.strftime("%Y%m%d")

    def get_dataframe_from_previous(self, days=1):
        interval = timedelta(days)
        previous = self.today - interval
        previous_str = previous.strftime("%Y%m%d")
        dataframe = stock.get_market_ohlcv_by_date(previous_str, self.today_str, self.code)
        return dataframe
```
StockItemDataFrameCollector 인스턴스는 생성자에서 어떤 종목의 정보를 수집할지 정한다. get_dataframe_from_previous() 메소드를 통해 오늘날짜로부터 원하는 날 이전까지의 주가 정보를 데이터 프레임으로 반환한다.  

![image](https://user-images.githubusercontent.com/32003817/107649815-30507800-6cc1-11eb-9c41-57bfaef96eb8.png)
삼성전자의 주가를 일정한 주기(10초)로 수집하는 모습  

#### 3-3 DRF를 활용한 데이터 삽입 (CREATE)
데이터 삽입을 위해 우선 django 모델의 포맷에 적합하도록 변환하는 과정을 진행했다.  
```python
class Converter:
    @classmethod
    def convert_to_json_for_item(cls, df: DataFrame, market: int, company: str):
        json_list = list()
        for index in df.index:
            # 각 날짜별 행을 딕셔너리로 가져오는 과정
            index_per_date: str = index.strftime('%Y-%m-%d')  # index: TimeStamp
            series_per_date: Series = df.loc[index_per_date]
            json_str_per_date: str = series_per_date.to_json(force_ascii=False)
            json_per_date: dict = json.loads(json_str_per_date)

            # 주식시장, 종목, 등록일 삽입
            json_per_date['stock_market'] = market
            json_per_date['stock_item_name'] = company
            json_per_date['reg_date'] = index_per_date

            # 한글로 된 키를 영문으로 변경
            json_per_date = cls.__convert_key_from_kor_to_eng_for_item(json_per_date)

            json_list.append(json_per_date)
        return json_list

    @staticmethod
    def __convert_key_from_kor_to_eng_for_item(json_per_date: dict):
        replacements = {'시가': 'open',
                        '종가': 'close',
                        '고가': 'high',
                        '저가': 'low',
                        '거래량': 'volume'}

        for key_kor, key_eng in replacements.items():
            json_per_date[key_eng] = json_per_date.pop(key_kor)

        return json_per_date
```  

간단히 설명하자면 PyKrx를 통해 가져온 데이터프레임을 requests 모듈의 인자로 보낼 수 있도록 딕셔너리로 변환하는 작업이다. 그리고 requests 모듈의 get 요청은 원할했지만 post요청을 하자 403 에러가 나타나는 것을 알 수 있었다. 오류내용은 다음과 같았다.  
```python
{
    "detail": "CSRF Failed: CSRF token missing or incorrect."
}
```  

결론부터 이야기 하면 이와 같은 오류가 나는 이유는 **로그인 세션**이 존재하지 않기 때문이다. 우리는 로그인 세션을 활성화하기 위한 토큰을 먼저 준비해야한다. (로그인을 위한 데이터라고 이해하면 쉽다.) 우선, 토큰을 통한 인증방식을 진행할 것이기 때문에 settings.py에서는 다음과 같이 설정해주어야 한다.  
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
```  

다음으로는 로그인 세션을 생성해야한다.  
```python
class BaseReq:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/rest_api/'
        self.login_url = self.url + 'auth/login/'
        # 2021.02.14.hsk : 추후에 screts.json으로 통합
        self.id = ...
        self.password = ...
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
    
    ...
```  

그리고 지금부터는 requests 모듈이 아닌 self.client 객체 (즉, 현재 활성화된 로그인 세션)을 통해서 요청을 해야한다.  
```python
class BaseCreate(BaseReq):
    def __init__(self):
        super().__init__()

    @csrf_exempt
    def send_post(self):
        for datum in self.data:
            res = self.client.post(self.url, json=datum)  # self.client(현재 활성화된 로그인 세션)를 사용한 요청
            res = self._ret(res)
            print(res, datum)
```  

![image](https://user-images.githubusercontent.com/32003817/107878707-cc73bc80-6f17-11eb-9a0d-1adba26d3ec9.png)  
![image](https://user-images.githubusercontent.com/32003817/107878749-05139600-6f18-11eb-93b9-bb83d640e97b.png)  
성공적으로 데이터가 삽입된 모습

* 참고  
CSRF는 무엇인가? CSRF는 Cross-site request forgery의 약자로 '사이트 간 요청 위조'를 의미한다. 사이트 간 스크립팅(XSS) 공격은 공격자가 웹 사이트에 악의적인 스크립트를 교묘하게 끼워넣어 사용자가 특정 웹사이트를 신용하는 점을 노린 것이라면, CSRF는 그와 반대로 특정 웹사이트가 사용자의 웹 브라우저를 신용하는 상태를 노린 것이다. 일단 사용자가 웹사이트에 로그인한 상태에서 사이트간 요청 위조 공격 코드가 삽입된 페이지를 열면, 공격 대상이 되는 웹사이트는 위조된 공격 명령이 믿을 수 있는 사용자로부터 발송된 것으로 판단하게 되어 공격에 노출된다. **CSRF 토큰이 존재하는 이유는 CSRF 공격을 방지하기 위해 고유한 값을 대조하여 사용자와 대조하기 위함이다.**




### 4. 프론트엔드 뷰 구축 (React.js)  
#### 4-1 뷰 설계  
##### 4-1-1 실시간 주가 정보 조회앱의 뷰 설계  

- 주식시장 선택 뷰 (무한스크롤형)  
각 주식시장별 그래프를 띄우며, 해당 주식시장(코스피200, 코스닥150)의 종목별 주가 정보 조회 뷰로 접근할 수 있게 해준다.  
무한스크롤형을 선택한 이유는 주식시장이 추가되는 경우를 고려한 것이다.  

```javascript
import React, { Component } from 'react'
import CardStockMarket from '../card/cardStockMarket'

class ListStockMarket extends Component {
    render() {
        var markets = [];
        var marketDatas = this.props.data;
        var i = 0;

        for (i = 0; i < marketDatas.length; i++){
            marketData = marketDatas[i]
            markets.push(
            <li key = {marketData.id}>
                <CardStockMarket name={marketData.name}></CardStockMarket>
            </li>
            );
        }

        return (
        <nav>
            <ul>
            {markets}
            </ul>
        </nav>
        );
    }
  }

  export default ListStockMarket;

```

```javascript
// 리스트의 각 항목의 역할을 하는 카드 컴포넌트
import React, { Component } from 'react'

import './cardStockMarket.css'

import {Card, CardHeader, CardContent, CardActions, CardMedia} from '@material-ui/core'
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button'

class CardStockMarket extends Component {
    render() {
        var marketName = this.props.name;
        
        return (
            <Card className="root">
                <CardHeader>  
                </CardHeader>
                <CardContent>
                    <Typography className="content">I'm {marketName}. </Typography>
                </CardContent>
                <CardActions>
                    <Button size="small">GO TO</Button>
                </CardActions>
            </Card>
        );
    }
  }

  export default CardStockMarket;

```  
  

**2020.12.29**  
각 주식시장을 표현할 카드 설계중   
<img width="1440" alt="스크린샷 2020-12-29 오후 10 46 30" src="https://user-images.githubusercontent.com/32003817/103288259-d30da980-4a27-11eb-8a1c-fdfab8a6fe86.png">

**2021.02.24**  
![image](https://user-images.githubusercontent.com/32003817/108954001-750be400-76af-11eb-94f8-31755fea7d8a.png)
참고 : https://www.zerocho.com/category/React/post/579b5ec26958781500ed9955  
mongodb로부터 가져온 주식시장 정보를 바탕으로 CardStockMarket 컴포넌트를 출력한 내용이다. 우선 React 컴포넌트의 라이프사이클에 대한 간단한 설명을 하자면, 컴포넌트가 최초로 실행되면 mount된다고 표현한다. 이 대, context, defaultProps와 state를 저장한다. 그리고 **componentWillMount** 메소드가 호출된다. 이때는 컴포넌트가 DOM에 부착되기 전이므로 state나 props를 바꿔선 안된다. **render** 메소드를 통해 DOM에 부착된 후, **componentDidMount** 메소드가 호출된다. componentDidMount 메소드는 컴포넌트가 최초로 실행되고 DOM에 부착된 후에 실행되므로 각 컴포넌트가 생성된 후 최초 한번만 호출된다. 이때는 DOM에 부착되어 있는 상태이기 때문에 AJAX요청이나 setTimeout, setInterval과 같은 행동을 한다.  

그리고 axios 모듈을 통해 react로부터 django 서버를 거쳐 mongodb에 있는 데이터를 요청해왔다. python의 requests 모듈과 같다고 생각하면 된다. **아직 원인은 파악하지 못했지만 render에서 axios를 통해 요청할 경우 2번씩 요청되는 현상이 발생했다.** componentDidMount 라이프사이클에서 요청하자 이와같은 문제는 해결됬다.  
```javascript
// App.js 

...

  componentDidMount(){
    console.log('im didmount!');
    axios({
      method : "get",
      url : "http://127.0.0.1:8000/rest_api/market/"
    })
    .then(response => {
      console.log(response);
      let _markets = [];
      response.data.forEach(element => {
        let _id = element["id"];
        let _name = element["stock_market_name"];
        let market = <CardStockMarket name={_name}/>
        _markets = _markets.concat(market);
      });
      console.log('hello', _markets);
      this.setState({markets: _markets});
    })
    .catch(error => {
      console.log("error", error);
    })
  }
```
setState를 함으로써 render를 한번더 유발시킨다. 이때 우리가 요청한 데이터를 토대로 카드를 화면에 출력하게 된다.  

**2021.03.07**  
```javascript
// App.js

class App extends Component{

  state = {
    view_mode: 'market',
  }

  constructor(props){
    super(props);
  }

  // shouldComponentUpdate(){
  // }

  render(){
    let template = null;
    if (this.state.view_mode == 'market') {
      template = <ListStockMarket/>;
    }

    return (
      <div className="App">
        {template}
      </div>
    );
  }
}
```

```javascript
// listStockMarket.js

class ListStockMarket extends Component {
    state = {
        markets: []
      }
    
    constructor(props){
    super(props);
    }

    render(){
        return (
          <div id="grid">
            <ul className="stockMarkets">
              {this.state.markets}
            </ul>
          </div>
        );
      }
    
    componentDidMount(){
    axios({
        method : "get",
        url : "http://127.0.0.1:8000/rest_api/market/"
    })
    .then(response => {
        console.log(response);
        let _markets = [];
        response.data.forEach(element => {
        let _id = element["id"];
        let _name = element["stock_market_name"];
        let market = <CardStockMarket name={_name}/>
        _markets = _markets.concat(market);
        });
        this.setState({markets: _markets});
    })
    .catch(error => {
        console.log("error", error);
    })
    }
}
```
App.js 의 App 클래스에 view_mode 속성을 지닌 state를 세팅함으로써 상황에따라 동적으로 보여질 컴포넌트를 렌더링할 것이다. 기존의 로직은 listStockList.js로 옮기면서 구조를 리팩토링했다.
  
**2021.03.14**  
이번 시간에는 주식시장에 해당하는 주식종목만 가져오는 것이 목표이다. 그러나 http://127.0.0.1:8000/rest_api/item/ url로 GET 요청을 보내면 조건에 관계없이 종목을 전부 가져오는 불상사가 일어난다. 그래서 우리는 특정 조건을 설정해줄 필요가 있다.  

```python
class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

    def get_queryset(self):
        reg_date = self.request.query_params.get('reg_date', None)  # 쿼리스트링
        if reg_date is not None:
            self.queryset = self.queryset.filter(reg_date=reg_date)
        return self.queryset
```
위 코드는 viewset으로 구현된 요청 url에 쿼리스트링을 받아 모델로부터 해당하는 데이터만 queryset으로 반환한다. 테스트로 등록일자만 쿼리해보았다.  
![image](https://user-images.githubusercontent.com/32003817/111063782-f529aa80-84f3-11eb-9312-37b39e857e12.png)

- 종목별 주가 정보 조회 뷰 (List)  
현재 시점 해당 주식시장의 여러 종목의 주가를 조회 가능.  
해당 종목에 하이퍼링크를 달아 상세 정보 조회 뷰로 넘어갈 수 있게 한다.  

- 해당 종목 상세 정보 조회 뷰 (Detail)  
해당 종목의 주가를 기간별로 조회 가능 (그래프 적용)  
e.g) 1년전, 6개월전, 3개월전, 1개월전  

~~- 기능 패널  
모든 뷰의 우측에 패널로써 존재. 해당 패널에는 기능(Util)들이 속해있다.  
깔끔한 디자인을 위해 무한스크롤형 리스트에 기능을 추가한다. (기능의 확장 고려)~~

~~- 즐겨찾기 관리    
기능 패널에 속해있는 기능.  
사용자가 등록해둔 종목의 상세 정보 조회 뷰로 이동할 수 있게 한다.~~

~~- 종목별 주가 비교  
기능 패널에 속해있는 기능.  
종목별 주가 비교 뷰로 이동할 수 있게 한다.~~

~~- 종목별 주가 비교 뷰  
사용자가 원하는 종목을 추가하면 그래프를 겹쳐서 그림~~

##### 4-1-2 주가 정보 예측앱의 뷰 설계  

- 해당 종목 주가 예측 뷰  
해당 종목의 예측주가를 그래프로 시각화  
종목별로 뷰가 동일할 것으로 예상되므로 **템플릿** 적용  

### 5. Regression 적용  
참고 : https://steemit.com/kr/@phuzion7/volume  
pandas_datareader의 get_data_yahoo()를 통해 각 주식종목별 정보를 데이터 프레임 형태로 가져왔다. 그리고 여기서 volume의 의미는 다음 링크를 참고했다. 간략하게 설명하자면, volume은 일정기간의 거래량을 의미한다. 일반적으로 주가가 상승할 때에는 거래량이 증가한다고 한다. (거래를 시도하는 세력들에 의해) 크게 상승 볼륨, 하락 볼륨, U볼륨, 돔볼륨, 랜덤볼륨으로 나뉜다. 이중 볼륨의 상승과 하락은 선형회귀를 통해 파악할 수 있다.

### 6. 데이터 시각화  

### 7. 다른 머신러닝 모델 적용 및 테스트
