import datetime
from hotels.models import Reservation, Chambre
import dateparser


def check_availability(chambre, check_in, check_out):
    avail_list = []
    reservation_list = Reservation.objects.filter(chambre=chambre)
    for reservation in reservation_list:
        if reservation.check_in > dateparser.parse(check_out).date() or reservation.check_out < dateparser.parse(check_in).date() or reservation.status != 'EC':
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
