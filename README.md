# stock_prediction
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

1. 백엔드서버 구축  
2. DB 연동  
3. 네이버 금융 주가 데이터 크롤링  
3-1. CRUD 테스트 : MongoDB vs ElasticSearch  
4. 프론트엔드 뷰 구축  
5. Logistic Regression 적용  
6. 데이터 시각화  
