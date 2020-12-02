# stock
실시간 주가 정보 및 예측

## 사용될 스택
- Django  
>> 백엔드서버로써 사용.  

- React.js
>> 프론트엔드로써 사용.  

- Selenium  
>> 데이터 크롤링 엔진.  

- MongoDB or ElasticSearch  
>> DB로써 사용. MongoDB를 테스트로 사용한 후, 주가 데이터의 양을 커버할 수 있을 속도가 나오면 유지. 그렇지 않을 경우 ElasticSearch를 사용할 예정.  

- Logistic Regression (Sklearn)  
>> 주가 데이터를 선형회귀 분석을 통해 예측. 전체적인 서비스가 구현이 되면 다른 모델을 도입하며 정확도를 높여나갈 예정.  

- Matplotlib  
>> 데이터 시각화 모듈.

## 계획 및 진행과정  

### 1. 백엔드서버 구축  
#### 1-1. 앱 설계  
django 프로젝트는 여러 app들로 구성되어 있다. 즉, 프로젝트는 하나의 웹사이트이고, 각 앱들은 하나의 웹사이트에 속해있는 기능들이라고 생각하면 된다. e.g) 게시판, 이메일, 결제..  
현재 진행할 주제에는 기능이 **실시간 주가 정보 조회, 주가 정보 예측**이 있다. 고로 나는 두 가지의 앱을 생성할 것이다.  

```
python manage.py startapp stock_inquiry
python manage.py startapp stock_prediction
```

#### 1-2 뷰 설계  
##### 1-2-1 실시간 주가 정보 조회앱의 뷰 설계
##### 1-2-1 주가 정보 예측앱의 뷰 설계

#### 1-3 모델 설계  

### 2. DB 연동  

### 3. 네이버 금융 주가 데이터 크롤링  
#### 3-1. CRUD 테스트 : MongoDB vs ElasticSearch  

### 4. 프론트엔드 뷰 구축  

### 5. Logistic Regression 적용  

### 6. 데이터 시각화  

### 7. 다른 머신러닝 모델 적용 및 테스트
