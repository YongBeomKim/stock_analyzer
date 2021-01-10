# Stock 🔱
- 실시간으로 각 주식시장별 종목의 시세 조회 및 분석
- 누적된 데이터와 머신러닝 모델을 기반으로 주가 예측.  

위의 두 가지 기능을 중점으로 하는 웹 사이트를 목표로 합니다.

## 사용될 스택
- Django & DRF (Django Rest Framework)  
>> 백엔드서버로써 사용합니다.  

- React.js & material ui
> 프론트엔드로써 사용합니다.  
 
- 증권사 API
> 트래픽 제한과 태그변경으로 인한 유지보수의 어려움을 고려하여 증권사 API로 대체 예정. (크레온 api)

- MongoDB  
> MongoDB를 채택한 이유는 스키마의 제약을 덜 받기 위함입니다. 

- Regression (Sklearn)  
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

```
class Post(models.Model):
    user_name = models.CharField(max_length=200)
    # bookmark_item_list = models.CharField(max_length=200) # 연구중..

    def __str__(self):
        return self.user_name
```  

- 주식시장 모델  

```
class StockMarket(models.Model):
    stock_market_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_market_name
```

- 주식종목 모델  

```
class StockItem(models.Model):
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    stock_item_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_item_name
```

#### 1-3. REST API 구현 (DRF 적용)  
DRF는 왜 쓸까? (참고 : https://medium.com/@whj2013123218/django-rest-api%EC%9D%98-%ED%95%84%EC%9A%94%EC%84%B1%EA%B3%BC-%EA%B0%84%EB%8B%A8%ED%95%9C-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95-a95c6dd195fd)  
1. 기존의 native django 방식대로 개발을 한다면 프론트 부분은 백엔드로부터 데이터를 받고 django template에 개발을 해야할 것이다. 이럴 경우, 백엔드와 프론트의 완전한 분리가 어렵다. 그래서 DRF를 사용하면 rest api가 사용가능하기 때문에 **django 백엔드와 react 프론트가 분리가 가능**하다.  
2. 재사용성이 좋아진다. view에서 바로 html로 넘기게 되면 view에는 비슷한 로직도 매번 class-based view로 작성해야 하는 비효율적인 상황이 연출된다. 그러나 api를 적용하면 해당 **api를 재사용**할 수 있다. 

```
pip install djangorestframework
```  

DRF를 설치한 후 settings.py에 다음과 같이 적어준다.  

```
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

```
urlpatterns = [
    ...
    path('rest_api/', include('rest_api.urls')),
]
```  

rest_api의 models.py를 작성해보자.  

```
from django.db import models


# Create your models here.
class StockUser(models.Model):
    user_name = models.CharField(max_length=200)
    # bookmark_item_list = models.CharField(max_length=200) # 연구중..

    def __str__(self):
        return self.user_name


class StockMarket(models.Model):
    stock_market_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_market_name


class StockItem(models.Model):
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    stock_item_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_item_name
```  

그 다음 해당 모델을 serialize해야 한다.  
그 이유는 Django ORM의 Queryset은 Context로써 Django template으로 넘겨지며, HTML로 렌더링되어 Response로 보내지게 된다.
하지만 **JSON으로 데이터를 보내야 하는 RESTful API**는 HTML로 렌더링 되는 Django template를 사용할 수 없다. 그래서 Queryset을 Nested한 JSON
으로 매핑하는 과정을 거쳐야 하기 때문이다. (Queryset >> Json : Serialize)  

rest_api앱에 serializers.py를 작성해보자.  

```
from rest_framework import serializers
from .models import StockUser, StockMarket, StockItem
from django.contrib.auth.models import User


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

```
from rest_framework import viewsets

from .serializers import StockUserSerializer, StockMarketSerializer, StockItemSerializer
from .models import StockUser, StockMarket, StockItem


# Create your views here.
class StockUserViewSet(viewsets.ModelViewSet):
    queryset = StockUser.objects.all()
    serializer_class = StockUserSerializer


class StockMarketViewSet(viewsets.ModelViewSet):
    queryset = StockMarket.objects.all()
    serializer_class = StockMarketSerializer


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
```  

url을 라우팅 시켜보자. viewset을 라우팅할 때에는 CBV, FBV, Mixin, GenericAPIView와는 다르게 router객체로 간편하게 등록할 수 있다.  
rest_api/urls.py  

```
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StockUserViewSet, StockMarketViewSet, StockItemViewSet

router_user = DefaultRouter()
router_user.register('user', StockUserViewSet)

router_market = DefaultRouter()
router_market.register('market', StockMarketViewSet)

router_item = DefaultRouter()
router_item.register('item', StockItemViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router_user.urls)),
    path('', include(router_market.urls)),
    path('', include(router_item.urls)),
]
```  

서버를 실행시킨 후, http://localhost:8000/rest_api/posts/에서 자세한 내용을 확인할 수 있다.  
DRF에 관련된 내용은 drf_tutorial을 확인하면 된다.  

위와 같은 방법으로 재사용이 가능한 어떤 REST API를 구현할까? **각 테이블(모델)에 CRUD API**  



### 2. MongoDB 연동  
1. MongoDB 가입 -> 클러스터 생성 이후 하단의 그림과 같이 인증방식, DB 접근권한 등을 설정하여 Database user를 생성

![db1](https://user-images.githubusercontent.com/36228833/103440836-3dbf1f00-4c8c-11eb-8713-8c96c20b1b1c.PNG)

![db2](https://user-images.githubusercontent.com/36228833/103440843-4c0d3b00-4c8c-11eb-8fba-5fa45642e147.PNG)

2. 왼쪽 메뉴에 Network Access에 들어간 뒤 DB에 접근을 허용할 IP를 등록

![db3](https://user-images.githubusercontent.com/36228833/103440947-6562b700-4c8d-11eb-904e-4935f37f653e.PNG)

![dbdbdb](https://user-images.githubusercontent.com/36228833/103440950-6eec1f00-4c8d-11eb-9184-605af1f29c62.PNG)

**(스킵) 그 후 DB를 만들어야 하지만 파이썬 모델을 이용하여 만들것 이기 때문에 이 부분은 넘어감.

![db4](https://user-images.githubusercontent.com/36228833/103440978-bb375f00-4c8d-11eb-9242-d394583a181c.PNG)

3. 첫 페이지로 돌아와서 현재 Cluster의 Connection string을 복사

![db5](https://user-images.githubusercontent.com/36228833/103440984-d1ddb600-4c8d-11eb-8ef9-97737853dfdc.PNG)

![db6](https://user-images.githubusercontent.com/36228833/103440994-ef128480-4c8d-11eb-9ef4-82e1bcbc3851.PNG)

4. 이제 connection string으로 mongoDB 연동을 위한 모듈들을 설치합니다.

```
$ pip install dnspython
$ pip install djongo
```

5. 장고 프로젝트 내 settings.py 에 mongoDB 연동을 위한 코드 작성

```
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

6. migrate 명령어를 통해 모델의 변동사항을 데이터베이스에 적용합니다.

![db9](https://user-images.githubusercontent.com/36228833/103441103-fab27b00-4c8e-11eb-98d6-87eb8c1502ff.PNG)

7. 첫 페이지의 collections를 눌러 DB가 잘 연동되었는지 확인

![db8](https://user-images.githubusercontent.com/36228833/103441074-c212a180-4c8e-11eb-81b5-787bf727f28e.PNG)

### 2-1. settings.py 기밀정보 관리
settings.py 에는 secret_key, DB 정보 등 외부에 노출되면 안되는 기밀정보들을 담고있다.

SECRET_KEY의 용도 -- [출처](https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key)
- [암호화된 데이터 서명](https://docs.djangoproject.com/en/1.11/topics/signing/)을 포함하고 있다.
- 사용자 세션, 비밀번호 재설정 요청, 메시지 등을위한 고유 토큰을 포함하고 있다.

Django 앱에는 암호화 서명이 필요한 많은 것들이 있으며 'SECRET_KEY' 설정이 그 열쇠라고 볼 수 있다.

해당 기밀 정보들을 다음과 같이 json 파일로 관리하여 따로 호출하게끔 변경한다.

*secrets.json
```
{
    "SECRET_KEY": "your SECRET_KEY",
    "DB_HOST" : "your DB Host",
    "DB_NAME" : "your DB name",
    "DB_USERNAME" : "your DB Username",
    "DB_PASSWORD" : "your DB Password"
}
```

*settings.py
```
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

### 3. 크레온 api를 통한 데이터 수집
(고려사항)

본래는 주가정보 데이터를 가지고 tensorflow를 통해 미래주가를 예측하는 하는 방향으로 진행하려 했으나,

크레온 api가 32bit 만 지원함. (tensorflow는 32bit를 지원하지 않음)

1. 웹 크롤링 (pandas, yahoo-finance)

2. 크레온 api, tensorflow 학습용 서버를 각각 따로 둬서 데이터 결과를 request-response 방식으로 주고받기

3. 다른 api 활용


### 4. 프론트엔드 뷰 구축 (React.js)  
#### 4-1 뷰 설계  
##### 4-1-1 실시간 주가 정보 조회앱의 뷰 설계  

- 주식시장 선택 뷰 (무한스크롤형)  
각 주식시장별 그래프를 띄우며, 해당 주식시장(코스피200, 코스닥150)의 종목별 주가 정보 조회 뷰로 접근할 수 있게 해준다.  
무한스크롤형을 선택한 이유는 주식시장이 추가되는 경우를 고려한 것이다.  

```
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

```
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
  

2020.12.29. 각 주식시장을 표현할 카드 설계중   
<img width="1440" alt="스크린샷 2020-12-29 오후 10 46 30" src="https://user-images.githubusercontent.com/32003817/103288259-d30da980-4a27-11eb-8a1c-fdfab8a6fe86.png">
  
  
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


### 6. 데이터 시각화  

### 7. 다른 머신러닝 모델 적용 및 테스트
