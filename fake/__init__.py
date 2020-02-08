'''
数据库的虚拟数据，开发测试用
'''
# student表
student = [
    {"s_id": 1, "student_number": "5120170001", "password": "5120170001pwd", "we_id": 1},
    {"s_id": 2, "student_number": "5120170002", "password": "5120170002pwd", "we_id": 2},
    {"s_id": 3, "student_number": "5120170003", "password": "5120170003pwd", "we_id": 3}
]

# wechat_bind表
wechat_bind = [
    {'we_id':1,"open_id":"open_id_1","secret_key":"key_1","nick_name":"Li(1)",
     "gender":"0","avatar_url":"http:a.com","country":"四川","city":"绵阳"},
    {'we_id':2,"open_id":"open_id_2","secret_key":"key_2","nick_name":"Li(2)",
     "gender":"1","avatar_url":"http:a.com","country":"四川","city":"成都"},
    {'we_id':3,"open_id":"open_id_3","secret_key":"key_3","nick_name":"Li(3)",
     "gender":"2","avatar_url":"http:a.com","country":"四川","city":"德阳"},
    {'we_id':4,"open_id":"open_id_4","secret_key":"key_3","nick_name":"Li(4)",
     "gender":"2","avatar_url":"http:a.com","country":"四川","city":"德阳"},
    {'we_id':5,"open_id":"open_id_5","secret_key":"key_3","nick_name":"Li(5)",
     "gender":"2","avatar_url":"http:a.com","country":"四川","city":"德阳"}
]
# micro_service表
micro_service = [
    {"ms_id":1,"ms_name":"课表","ms_key":"key1","ms_url":"a1.com","img_url":"b1.com"},
    {"ms_id":2,"ms_name":"成绩","ms_key":"key2","ms_url":"a2.com","img_url":"b2.com"},
    {"ms_id":3,"ms_name":"失物招领","ms_key":"key3","ms_url":"a3.com","img_url":"b3.com"},
    {"ms_id":4,"ms_name":"校历","ms_key":"key4","ms_url":"a4.com","img_url":"b4.com"},
    {"ms_id":5,"ms_name":"考试","ms_key":"key5","ms_url":"a5.com","img_url":"b5.com"}
]
