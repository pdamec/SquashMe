import re
from datetime import datetime, date, timedelta
import logging
from requests import Session
from lxml import html
from .settings import login_page, admin_page


logger = logging.getLogger(__name__)


class SquashMe:

    def __init__(self, court_number=None, discipline='squash', start="6:00", end="23:30",
                 day=datetime.today().strftime('%Y-%m-%d'), **kwargs):

        if 'config' in kwargs:
            self.config = kwargs['config']

        self.session = None
        self.court_number = court_number
        self.discipline = discipline
        self.start = self.convert_time(start)
        self.end = self.convert_time(end)
        self.day = day
        self.parser = self.create_parser()

    @property
    def free_reservations(self):
        return self.get_free_reservations()

    def create_parser(self):
        payload = dict(log=self.config['login'], pwd=self.config['password'])

        self.session = Session()
        self.session.post(login_page, data=payload)
        content = self.load_reservation_table()
        return html.fromstring(content)

    def get_costs(self):
        regex = r'\d{2} - \d{2}|\d{2} \w{2}'
        table_headers = [i.strip() for i in self.parser.getchildren()[0].itertext() if re.match(regex, i)]
        return {hours: cost for hours, cost in zip(table_headers[0::2], table_headers[1::2])}

    def get_free_reservations(self):
        free_reservations = self.parser.find_class('rez rez_wolne')
        for i in free_reservations:
            court = i.getparent().getchildren()[0].text
            for a in i:
                free_since = self.convert_time(a.attrib.get('data-godz_od'))
                free_until = self.convert_time(a.attrib.get('data-godz_do'))
                if free_since >= self.start and free_until <= self.end:
                    yield {'free_since': a.attrib.get('data-godz_od'), 'free_until': a.attrib.get('data-godz_do'),
                           'id': i.getparent().attrib['data-obie_id'], 'court': court}

    @staticmethod
    def convert_time(res_time):
        # WA for comparing 00:00 hour in get_free_reservations().
        now = date.today()
        if res_time == "00:00":
            now = now.replace(day=now.day + 1)
        return datetime.strptime('{} {}'.format(now, res_time), '%Y-%m-%d %H:%M')

    def load_reservation_table(self):
        payload = {
            'operacja': 'ShowRezerwacjeTable',
            'action': 'ShowRezerwacjeTable',
            'data': self.day,
            'obiekt_typ': self.discipline.lower(),
        }
        req = self.session.post(admin_page, data=payload)
        return req.content

    # @staticmethod
    # def _is_between(time, time_range):
    #     if time_range[1] < time_range[0]:
    #         return time >= time_range[0] or time <= time_range[1]
    #     return time_range[0] <= time <= time_range[1]
    #
    # def ttt(self):
    #     # TBD
    #     # 'godz_od': '15:00' 11:00 06:00
    #     # 'godz_do': '00:00' 20:00 15:00
    #     #
    #     self._is_between('11:00', ('06:00', '16:00'))

    def create_reservation_payload(self, user_reservations):
        print(self.court_number)
        for reservation in self.free_reservations:
            if reservation['free_since'] in user_reservations and int(reservation['court']) == self.court_number:
                yield '{}_{}_{}'.format(reservation['id'], reservation['free_since'], reservation['free_until'])

    def request_reservations(self, reservation_slots):
        for slot in reservation_slots:
            payload = dict(action='RezerwujWybraneZapisz', data=self.day)
            payload.update({'REZ[]': slot})
            self.session.post(admin_page, payload)

            parsed_payload = payload['REZ[]'].split('_')
            logger.info(f'Making reservation for {self.discipline} between {parsed_payload[1]} - {parsed_payload[2]} '
                        f'on court {self.court_number}')

        self.session.post(admin_page, dict(action='Rezerwacje4Datepicker', klie_nick=self.config['user_id']))

    def get_user_reservations(self, reservations):
        reservations = reservations.strip().split(' ')
        for reservation in reservations:
            if re.match(r'\d{2}:\d{2}-\d{2}:\d{2}', reservation):
                starting = self.convert_time(reservation.split('-')[0])
                ending = self.convert_time(reservation.split('-')[1])
                while starting < ending:
                    yield starting.strftime('%H:%M')
                    starting += timedelta(minutes=30)
            elif re.match(r'\d{2}:\d{2}', reservation):
                yield reservation
            else:
                logging.info('Wrong reservation time format: {}.'.format(reservation))

    def show_free_reservations(self):
        if self.court_number:
            reservations = []
            for reservation in self.free_reservations:
                if int(reservation['court']) == self.court_number:
                    reservations.append(reservation)
        else:
            reservations = list(self.free_reservations)
        return reservations

    def automatic_reservation(self):
        # TBD
        pass
