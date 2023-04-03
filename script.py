from datetime import datetime
import uuid
from bs4 import BeautifulSoup
import calendar
import pandas as pd
from decimal import *


df = pd.read_csv('~/Downloads/print - data.csv')
bs_data = BeautifulSoup('<smses></smses>', 'xml')
smses = bs_data.smses
phone="+79091234567"
address="900"
current_money = Decimal('2204.83').quantize(Decimal('.01'), rounding=ROUND_DOWN)
getcontext().prec = 8
df = df.reindex(index=df.index[::-1])
counter = 0

for index, row in df.iterrows():
    counter+=1
    # print(row)
    sms_date_time = datetime.strptime(row['Дата операции'], "%d.%m.%Y %H:%M")
    row_money = row['Сумма в валюте счёта'].replace(',', '.')
    # print(row_money)
    money = Decimal(row_money).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    operation_type=row['Описание операции']
    income: bool = money > 0
    abs_money = abs(money)
    current_money += money
    current_money = current_money
    if not income:
        sms_body = "VISA0000 Покупка " + str(abs_money) + " " + operation_type + " Баланс: " + str(current_money)
    else:
        sms_body = "VISA0000 Зачисление " + str(abs_money) + " " + operation_type + " Баланс: " + str(current_money)

    # print('current={} ; operation money={}'.format(current_money, money))
    sms_tag = bs_data.new_tag("sms",
        protocol="0",
        address=address,
        date=str(int(sms_date_time.timestamp())) + "000",
        type="1", 
        subject="null",
        toa="null", 
        sc_toa="null",
        service_center=phone,
        read="1",
        status="-1",
        locked="0",
        date_sent=str(int(sms_date_time.timestamp())) + "000",
        sub_id="1",
        readable_date=calendar.month_name[sms_date_time.month] + sms_date_time.strftime(' %d, %Y %H:%M:00'),
        body=sms_body,
        contact_name="(Unknown)")
    smses.append(sms_tag)
    # print(smses)
smses['count'] = counter
smses['backup_set'] = str(uuid.uuid4())
smses['backup_date'] = "1680197799000"
smses['type'] = "full"
# backup_date="1680197799000" type="full"
with open('test.xml', 'w') as f:
    f.write(smses.prettify())