import jigeum.seoul
from mnist.db import select, dml
import os
import requests
import numpy as np
from PIL import Image
from keras.models import load_model

def get_job_img_task():
    sql = """
    SELECT 
        num, file_name, file_path
    FROM image_processing
    WHERE prediction_result is NULL
    ORDER BY num -- 가장 오래된 요청
    LIMIT 1 -- 하나씩
    """

    r = select(sql, 1)
    if len(r) > 0:
        return r[0]
    else:
        return None

    return r[0]

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    # img = 255 - np.array(img)  # 흑백 반전
    img = np.array(img)
    
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

# 예측
def predict_digit(image_path):
    # 모델 로드
    path = os.getenv("M_PATH", "/Users/sujinya/code/mnist/note/mnist240924.keras")
    model = load_model(path)  # 학습된 모델 파일 경로
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit

def prediction(file_path,num):
    sql = """UPDATE image_processing
    SET prediction_result=%s,
        prediction_model='n77',
        prediction_time=%s
    WHERE num=%s
    """
    
    presult = predict_digit(file_path)
    dml(sql,presult, jigeum.seoul.now(), num)
    return presult

def run():
  """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
  # STEP 1
  # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기

  job = get_job_img_task()
  if job is None:
      print(f"{jigeum.seoul.now()}, num")
      return 

  num = job['num']
  file_name = job['file_name']
  file_path = job['file_path']

  # STEP 2
  # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
  # 동시에 prediction_model, prediction_time 도 업데이트
  presult = prediction(file_path,num)


  # STEP 3
  # LINE 으로 처리 결과 전송

  send_line_noti(file_name,presult)
  print(jigeum.seoul.now())

def send_line_noti(file_name='test', presult='-1'):
    KEY = os.getenv('LINE_NOTI_TOKEN', 't5mTs8lD9zRUisWxZrbKHoHWKDUipPur73gYPs1c5IE')
    url = "https://notify-api.line.me/api/notify"
    data = {"message": f"성공적으로 저장했습니다! 예측값은 {presult} 입니다 🎉"}
    headers = {"Authorization": f"Bearer {KEY}"}
    response = requests.post(url, data=data, headers=headers)

    print(response.text)

    return True