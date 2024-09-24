from typing import Annotated
import os
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
import pymysql.cursors

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]

    upload_dir = "/Users/sujinya/code/mnist/img"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, 'wb') as f:
        f.write(img)
        
    
    connection = pymysql.connect(host="172.17.0.1",
                                 user='mnist',
                                 password='1234',
                                 database='mnistdb',
                                 port=int(53306),
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "INSERT INTO image_processing(`file_name`, `file_path`, `request_time`, `request_user`) VALUES(%s,%s,%s,%s)"

    import jigeum.seoul #시간모듈
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (file.filename, file_full_path, jigeum.seoul.now(), 'n01'))

        connection.commit()
        
    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path,
            "time": jigeum.seoul.now()
            }
