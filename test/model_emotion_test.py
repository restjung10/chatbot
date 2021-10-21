from utils.Preprocess import Preprocess
from models.emotion.EmotionModel import EmotionModel

p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin')

emotion = EmotionModel(model_name='models/emotion/emotion_model.h5', proprocess=p)

query = "오늘 굉장히 신나"
predict = emotion.predict_class(query)
predict_label = emotion.labels[predict]

print(query)
print("감정 예측 클래스 : ", predict)
print("감정 예측 레이블 : ", predict_label)