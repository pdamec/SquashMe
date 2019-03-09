import re
import os
import datetime
import logging
from lxml import html
from requests import session
from .settings import login_page, reservation_page


class SquashMe:

    ASD = ['Squash', 'Badminton', 'Tenis stolowy']

    def __init__(self, court_number=None, discipline=None, start="6:00", end="23:30"):
        self.court_number = court_number
        self.discipline = discipline
        self.start = self.convert_reservation_time(start)
        self.end = self.convert_reservation_time(end)
        self.parser = self.create_parser()

    @property
    def reservation_table(self):
        return self.parser.get_element_by_id('rez_rezerwacje_div').getchildren()[0]

    @staticmethod
    def create_parser():
        payload = {
            'log': os.environ['SQUASH_USER'],
            'pwd': os.environ['SQUASH_PASSWORD']
        }

        with session() as c:
            c.post(login_page, data=payload)
            response = c.get(reservation_page)

        msg = (
            f'Response text: {response.text}'
            f'Response status: {response.status_code}'
        )

        logging.debug(msg)

        return html.fromstring(response.content)

    def get_costs(self):
        regex = r'\d{2} - \d{2}|\d{2} \w{2}'
        table_headers = [i.strip() for i in self.reservation_table.getchildren()[0].itertext() if re.match(regex, i)]
        a = {hours: cost for hours, cost in zip(table_headers[0::2], table_headers[1::2])}
        return a

    def get_court(self):
        if self.court_number:
            for i in self.reservation_table.getchildren():
                for a in i:
                    if a.text == str(self.court_number):
                        return a.getparent()
        else:
            return None

    def get_free_reservations(self):
        court = self.get_court()
        free_reservations = court.find_class('rez rez_wolne')
        for i in free_reservations:
            for a in i:
                free_since = self.convert_reservation_time(a.attrib.get('data-godz_od'))
                free_until = self.convert_reservation_time(a.attrib.get('data-godz_do'))
                if free_since >= self.start and free_until <= self.end:
                    yield a.attrib

    @staticmethod
    def convert_reservation_time(res_time):
        # WA for comparing 00:00 in get_free_reservations().
        now = datetime.date.today()
        if res_time == "00:00":
            now = now.replace(day=now.day + 1)
        return datetime.datetime.strptime('{} {}'.format(now, res_time), '%Y-%m-%d %H:%M')

    def choose_discipline(self):
        # TBD
        for i in self.parser.get_element_by_id('rez_obiekt_typ_div'):
            print(i.attrib, i.text)

    def make_reservation(self):
        # TBD
        self.parser.get_element_by_id('rez_rezerwuj_b')

    def show_reservations(self):
        print(list(self.get_free_reservations()))
