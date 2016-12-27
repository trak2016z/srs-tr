import datetime

from app.models import Availability_Room


def availability_by_date(room_id, day, month, year):
    dat = datetime.datetime(year=year, month=month, day=day)
    day_of_week = int(dat.strftime("%w"))
    day_of_week = day_of_week if day_of_week > 0 else 7
    return Availability_Room.objects.filter(room__id=room_id, day_of_week=day_of_week, since__lte=dat, until__gte=dat).count() > 0


def availability_hours_by_date(room_id, day, month, year):
    dat = datetime.datetime(year=year, month=month, day=day)
    day_of_week = int(dat.strftime("%w"))
    day_of_week = day_of_week if day_of_week > 0 else 7
    lst = []
    for r in Availability_Room.objects.filter(room__id=room_id, day_of_week=day_of_week, since__lte=dat, until__gte=dat).order_by('hour_from', '-hour_to'):
        begin_sp = r.hour_from.split(":")
        end_sp = r.hour_to.split(":")
        begin = (int(begin_sp[0]), int(begin_sp[1]))
        end = (int(end_sp[0]), int(end_sp[1]))
        lst.append((begin, end))
    return lst

def availability_inrange(tab_ava, hour, minute):
    ih = "0" + str(hour) if hour < 10 else str(hour)
    im = "0" + str(minute) if minute < 10 else str(minute)
    istr = ih+":"+im
    for t in tab_ava:
        ((bh, bm), (eh, em)) = t
        bh_str = "0" + str(bh) if bh < 10 else str(bh)
        bm_str = "0" + str(bm) if bm < 10 else str(bm)
        b_str = bh_str+":"+bm_str
        eh_str = "0" + str(eh) if eh < 10 else str(eh)
        em_str = "0" + str(em) if em < 10 else str(em)
        e_str = eh_str + ":" + em_str
        if istr >= b_str and istr < e_str:
            return True
    return False
