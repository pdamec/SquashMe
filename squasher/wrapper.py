import os
import logging
from getpass import getpass
from configparser import ConfigParser
from pprint import pformat
from .squasher import SquashMe

logger = logging.getLogger(__name__)


class SQWrapper:

    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')

    def __init__(self, **kwargs):
        self.args = kwargs
        self.set_config()
        self.sq = SquashMe(**kwargs, config=self.get_config())

    def start_me_please(self):
        free_reservations = self.sq.show_free_reservations()

        if free_reservations:
            logger.info(pformat(free_reservations))
            user_reservations = input('Select hours to reserve (hh:mm-hh:mm or hh:mm): ')

            if self.args['court_number'] is None:
                self.set_court()
            self.reserve(user_reservations)
        else:
            logger.info('No courts available between {}-{} on {}.'.format(self.args['start'], self.args['end'],
                                                                          self.args['day']))

    def set_court(self):
        court = input('Select court (number): ')
        if court:
            self.sq.court_number = int(court)
            logger.info('Getting reservations for court: {}'.format(self.sq.court_number))
        else:
            logger.info('No court provided.')

    def reserve(self, user_reservations):
        if user_reservations:
            user_reservations = list(self.sq.get_user_reservations(user_reservations))
            print(user_reservations)
            reservation_slots = self.sq.create_reservation_payload(user_reservations)
            self.sq.request_reservations(reservation_slots)
        else:
            logger.info('No user reservations provided.')

    def set_config(self):
        if not os.path.isfile(SQWrapper.CONFIG_PATH) or self.args['is_rename']:
            login = input('Provide login to Hasta La Vista: ')
            password = getpass()
            username = input('Provide name and surname (Name Surname) '
                             'that were used to create Hasta La Vista account: ')
            self.create_config(login, password, username)

    @staticmethod
    def create_config(login, password, username):
        username = username.lower().strip().split(' ')

        config = ConfigParser()
        config['USER_INFO'] = dict(login=login, password=password, name=username[0], surname=username[1])
        with open(SQWrapper.CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_config():
        config = ConfigParser()
        config.read(SQWrapper.CONFIG_PATH)

        name = config['USER_INFO']['NAME']
        surname = config['USER_INFO']['SURNAME']
        user_id = '{}{}'.format(surname, name[0]).lower()
        return dict(login=config['USER_INFO']['LOGIN'], password=config['USER_INFO']['PASSWORD'], user_id=user_id)
