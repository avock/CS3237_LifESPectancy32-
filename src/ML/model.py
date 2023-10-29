import pickle
from sklearn.linear_model import LinearRegression

# Sample data (height in centimeters and corresponding weight in kilograms)
# 1 inch = 2.54 cm
# 1 pound = 0.453592 kg
height_cm = [[152.4], [157.48], [162.56], [167.64], [172.72], [177.8], [182.88]]
weight_kg = [49.895, 54.431, 58.967, 63.502, 68.038, 72.574, 77.110]

model = LinearRegression()
model.fit(height_cm, weight_kg)

with open('test_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
