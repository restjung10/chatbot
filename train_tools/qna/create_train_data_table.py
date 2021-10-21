import pymysql
from config.DataBaseConfig import *

db = None
try:
    db = pymysql.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        db = DB_NAME,
        charset = 'utf8'
    )

    # 테이블 생성 sql 정의
    sql = '''
        CREATE TABLE IF NOT EXISTS `chatbot_train_data` (
        `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `emotion` VARCHAR(45) NULL,
        `query` TEXT NULL,
        `answer` TEXT NOT NULL,
        `answer_image` VARCHAR(2048) NULL,
        PRIMARY KEY (`id`))
    ENGINE = InnoDB DEFAULT CHARSET = utf8
    '''

    # 테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()