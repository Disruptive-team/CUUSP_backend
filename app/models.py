from peewee import *

from . import db_wrapper


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(db_wrapper.Model):
    class Meta:
        database = db_wrapper.database

class MicroService(BaseModel):
    img_url = CharField(null=True)
    ms_id = AutoField()
    ms_key = CharField(null=True)
    ms_name = CharField(null=True)
    ms_url = CharField(null=True)

    class Meta:
        table_name = 'micro_service'

class WechatBind(BaseModel):
    avatar_url = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(null=True)
    gender = IntegerField(null=True)
    nick_name = CharField(null=True)
    open_id = CharField(null=True)
    secret_key = CharField(null=True)
    update_time = DateTimeField(null=True)
    we_id = AutoField()

    class Meta:
        table_name = 'wechat_bind'

class Student(BaseModel):
    password = CharField(null=True)
    s_id = AutoField()
    student_number = CharField(null=True)
    we = ForeignKeyField(column_name='we_id', field='we_id', model=WechatBind, null=True)

    class Meta:
        table_name = 'student'


if __name__ == '__main__':
    a = Student.get(Student.s_id == 1)
    print(a.password)
