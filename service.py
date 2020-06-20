# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, IntegerField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms import validators, ValidationError

class ServiceForm(Form):
    id = IntegerField(u'شماره سرویس')
    name = TextField(u'نام انگلیسی', [validators.Required("لطفا نام را وارد نمایید")])
    description = TextField(u'نام فارسی', [validators.Required("لطفا نام را وارد نمایید")])
    city_id = SelectField(u'دیتاسنتر', choices = [('1', u'شریعتی'), ('2', u'مشهد'), ('3',u'سئول'), ('4',u'رایتل'),
                                                  ('5',u'نصراللهی'), ('6',u'بهشتی'), ('7',u'پیک آسا'), ('8',u'همراه اول انارستان')])
    dnid = IntegerField(u'شماره تلفن سرویس')
    service_number = IntegerField(u'سر شماره تلفن سرویس')
    start_date = DateTimeField(u'تاریخ شروع سرویس', format='%Y-%m-%d')  #TextField(u'تاریخ شروع سرویس')
    company_name = TextField(u'نام شرکت')
    enable = BooleanField(u'فعال')
    submit = SubmitField(u'ارسال')