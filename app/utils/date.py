# -*- coding: utf-8 -*-
import calendar
import datetime


def date_format_short(datetime):
    day = str(datetime.day) if datetime.day >= 10 else '0'+str(datetime.day)
    month = str(datetime.month) if datetime.month >= 10 else '0'+str(datetime.month)
    hour = str(datetime.hour) if datetime.hour >= 10 else '0'+str(datetime.hour)
    minute = str(datetime.minute) if datetime.minute >= 10 else '0'+str(datetime.minute)
    return day + '.' + month + '.' + str(datetime.year) + ' ' + hour + ':' + minute


def month_name(month):
    lmn = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
    return lmn[month-1]


def dayw_name(day_of_week):
    lmn = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    return lmn[day_of_week - 1]


# indeks numeru tygodnia pierwszego dnia (1 - Pon, 7 - Nd)
def dayw_name_date(day, month, year):
    dat = datetime.datetime(year=year, month=month, day=day)
    dat_w = int(dat.strftime("%w"))
    dat_w2 = dat_w if dat_w > 0 else 7
    return dayw_name(dat_w2)


# indeks numeru tygodnia pierwszego dnia (1 - Pon, 7 - Nd)
def w_first_day(month, year):
    dat = datetime.datetime(year=year, month=month, day=1)
    dat_w = int(dat.strftime("%w"))
    return dat_w if dat_w > 0 else 7


def month_days(month, year):
    return calendar.monthrange(year, month)[1]
