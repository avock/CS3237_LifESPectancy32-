import pickle

with open('test_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

height_to_predict = [[175]] 

predicted_weight = model.predict(height_to_predict)

print(f"Predicted weight: {predicted_weight[0]}kg")
