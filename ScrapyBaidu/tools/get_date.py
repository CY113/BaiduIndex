# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.6.1
# @ Date: 2019/11/6 10:50
# @ Desc
import calendar
import datetime
from dateutil.relativedelta import relativedelta
begin = "2019-01"
end = "2019-10"
r = calendar.monthrange(int(begin.split("-")[0]),int(begin.split("-")[1]))[1]


datetime_now = datetime.datetime.strptime(begin,'%Y-%m')
datetime_three_month_ago = datetime_now - relativedelta(months=1)
print()
