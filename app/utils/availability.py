import datetime

from app.models import Availability_Room


def make_string(hour, minute):
    ih = "0" + str(hour) if hour < 10 else str(hour)
    im = "0" + str(minute) if minute < 10 else str(minute)
    return ih+":"+im


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
    istr = make_string(hour, minute)
    if tab_ava is not None:
        for t in tab_ava:
            ((bh, bm), (eh, em)) = t
            b_str = make_string(bh, bm)
            e_str = make_string(eh, em)
            if istr >= b_str and istr < e_str:
                return True
    return False


def availability_inrange2(tab_ava, from_hour, from_minute, to_hour, to_minute):
    from_str = make_string(from_hour, from_minute)
    to_str = make_string(to_hour, to_minute)
    if tab_ava is not None:
        for t in tab_ava:
            ((bh, bm), (eh, em)) = t
            b_str = make_string(bh, bm)
            e_str = make_string(eh, em)
            if from_str >= b_str and to_str <= e_str:
                return True
    return False