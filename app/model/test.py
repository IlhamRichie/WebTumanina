import numpy as np
import pickle
import tensorflow as tf

# Load resources
model = tf.keras.models.load_model('app/model/chatbot_model.h5')
with open('app/model/words.pkl', 'rb') as f:
    words = pickle.load(f)
with open('app/model/classes.pkl', 'rb') as f:
    classes = pickle.load(f)

# Tes model
def bow(sentence, words):
    sentence_words = sentence.split()
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

# Input tes
message = "pembuat tumanina"
input_data = bow(message, words)
res = model.predict(np.array([input_data]))[0]
index = np.argmax(res)
tag = classes[index]
print("Predicted tag:", tag)
print("Confidence score:", res[index])


# import tensorflow as tf
# model = tf.keras.models.load_model('app/model/chatbot_model.h5')
# print("Model loaded successfully.")
