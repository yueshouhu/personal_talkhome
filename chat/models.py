from django.db import models
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator


# Create your models here.
class users(models.Model):
    username=models.CharField(max_length=32,unique=True)
    password=models.CharField(max_length=32)

class register_form(Form):
    '''学生注册验证使用'''
    username = fields.CharField(
        widget=widgets.TextInput(),
        required=True,
        error_messages={
            'required': "不能为空"},
    )
    password = fields.CharField(
        max_length=12,
        min_length=6,
        required=True,
        error_messages={'required': '不能为空',
                        "max_length": "最多12位",
                        "min_length": "最少6位"},
    )






