def date_format_short(datetime):
    day = str(datetime.day) if datetime.day >= 10 else '0'+str(datetime.day)
    month = str(datetime.month) if datetime.month >= 10 else '0'+str(datetime.month)
    hour = str(datetime.hour) if datetime.hour >= 10 else '0'+str(datetime.hour)
    minute = str(datetime.minute) if datetime.minute >= 10 else '0'+str(datetime.minute)
    return day + '.' + month + '.' + str(datetime.year) + ' ' + hour + ':' + minute
