# import pandas as pd
# import tensorflow as tf

# 1. 과거의 데이터 준비 - 2021.02.04 : mongodb에서 가져온 값으로 대체 예
# lemonade_path = 'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/lemonade.csv'
# lemonade = pd.read_csv(lemonade_path)
# print(lemonade.shape)
# lemonade_independent_variable = lemonade[['온도']]
# lemonade_dependent_variable = lemonade[['판매량']]

# 2. 모델의 구조를 만든다.
# X = tf.keras.layers.Input(shape=[1])  # Volume
# Y = tf.keras.layers.Dense(1)(X)  # Predicted cost
# model = tf.keras.models.Model(X, Y)
# model.compile(loss='mse')

# 3. 모델을 학습(FIT)시킨다.
# model.fit(x=volumes, y=predicted_cost, epochs=1000)

# 4. 모델을 이용한다.
# prediction = model.predict([[current_volume]])
# print(prediction)