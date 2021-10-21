from config.DataBaseConfig import *
from utils.Preprocess import Preprocess
import random

# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin')

# 원문
query = "너무 겁이나고 두려워요"

# 감정 파악
from models.emotion.EmotionModel import EmotionModel
emotion = EmotionModel(model_name='models/emotion/emotion_model.h5', proprocess=p)
predict = emotion.predict_class(query)
emotion_name = emotion.labels[predict]

# 답변 
food0 = ['바나나', '호두', '연어', '아몬드', '아보카도', '고등어', '녹차']
food1 = ['다크 초콜릿', '따뜻한 차', '떡볶이같은 매운 음식']
food2 = ['버섯', '오리고기', '굴', '초콜릿', '빵']

A = random.choice(food0)
B = random.choice(food1)
C = random.choice(food2)

if predict == 0:
    print(f"답변 : 불안함을 느끼고 계신가요? 그럴땐 {A}을(를) 드셔보세요! 불안감을 진정시키는데 효과가 있데요!")
if predict == 1:
    print(f"답변 : 혹시 화가 나셨나요? 그럴땐 {B}을(를) 드셔보세요! 화를 가라앉히는데 효과가 있데요!")
if predict == 2:
    print(f"답변 : 마음이 울적하시겠어요..ㅠㅠ 그럴땐 {C}을(를) 드셔보세요! 우울함을 떨쳐내는데 효과만점!!")
if predict == 3:
    print("답변 : 기쁘고 행복하시군요! 그럴땐 뭘 먹어도 최고!!")