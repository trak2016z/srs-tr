from django.utils import timezone

from app.settings import BASE_DIR


def save_log(message):
    now = timezone.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H_%M_%S')
    f = open(BASE_DIR + '/app/logs/' + now_str + '.txt', 'w+')
    f.write(message)
    f.close()

