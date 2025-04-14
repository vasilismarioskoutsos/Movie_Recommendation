import json
import pickle

# load the model from file
def init():
    global model
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

def run(json_data):
    try:
        data = json.loads(json_data)
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})
