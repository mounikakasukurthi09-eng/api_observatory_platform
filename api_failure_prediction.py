import numpy as np
from pyod.models.iforest import IForest

X_train = np.array([
    [100, 30, 0],
    [120, 35, 0],
    [140, 40, 1],
    [160, 45, 0],
    [180, 50, 1],
    [2000, 95, 10],
    [2500, 99, 15],
    [3000, 97, 20]
])


model = IForest()

model.fit(X_train)

new_data = np.array([
    [5000, 100, 50]
])

prediction = model.predict(new_data)

if prediction[0] == 1:
    print("HIGH FAILURE RISK")
else:
    print("NORMAL API")