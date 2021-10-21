import threading
import json
from config.DataBaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.emotion.EmotionModel import EmotionModel
import random

# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin')

# 감정 파악 모델
emotion = EmotionModel(model_name='models/emotion/emotion_model.h5', proprocess=p)

def to_client(conn, addr, params):
    db = params['db']
    try:
        db.connect()

        # 데이터 수신
        read = conn.recv(2048) # 수신 데이터가 있을 때까지 블로킹
        print('=====================')
        print('Connection from : %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0) # 스레드 강제 종료

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 감정 파악
        emotion_predict = emotion.predict_class(query)
        emotion_name = emotion.labels[emotion_predict]

        # 답변 출력
        food0 = ['바나나', '호두', '연어', '아몬드', '아보카도', '고등어', '녹차']
        food1 = ['다크 초콜릿', '따뜻한 차', '떡볶이같은 매운 음식']
        food2 = ['버섯', '오리고기', '굴', '초콜릿', '빵']

        A = random.choice(food0)
        B = random.choice(food1)
        C = random.choice(food2)

        if emotion_predict == 0:
            answer = f"답변 : 불안함을 느끼고 계신가요? 그럴땐 {A}을(를) 드셔보세요! 불안감을 진정시키는데 효과가 있데요!"
        if emotion_predict == 1:
            answer = f"답변 : 혹시 화가 나셨나요? 그럴땐 {B}을(를) 드셔보세요! 화를 가라앉히는데 효과가 있데요!"
        if emotion_predict == 2:
            answer = f"답변 : 마음이 울적하시겠어요..ㅠㅠ 그럴땐 {C}을(를) 드셔보세요! 우울함을 떨쳐내는데 효과만점!!"
        if emotion_predict == 3:
            answer = "답변 : 기쁘고 행복하시군요! 그럴땐 뭘 먹어도 최고!!"
        
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "Emotion" : emotion_name,
        }

        message = json.dumps(send_json_data_str) # json 객체를 전송 가능한 문자열로 변환
        conn.send(message.encode())  # 응답 전송
        
    except Exception as ex:
        print(ex)

    finally:
        if db is not None:   # db 연결 끊기
            db.close()
        conn.close()

if __name__ == '__main__':
    # 질문/답변 학습 db 연결 객체 생성
    db = Database(
        host = DB_HOST, user = DB_USER, password = DB_PASSWORD, db_name = DB_NAME
    )
    print("DB접속")

    # 봇 서버 동작
    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db" : db
        }

        client =threading.Thread(target=to_client, args=(
            conn,   # 클라이언트 연결 소켓
            addr,   # 클라이언트 연결 주소 정보
            params  # 스레드 함수 파라미터
        ))
        client.start() # 스레드 시작