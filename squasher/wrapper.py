import os
import logging
from configparser import ConfigParser
from pprint import pprint
from .squasher import SquashMe

logger = logging.getLogger(__name__)


class SQWrapper:

    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')

    def __init__(self, **kwargs):
        self.args = kwargs
        self.sq = SquashMe(**kwargs)

    def start_me_please(self):
        self.set_config()
        free_reservations = self.sq.show_free_reservations()

        if free_reservations:
            pprint(free_reservations)
            user_reservations = input('Select hours to reserve (hh:mm-hh:mm or hh:mm): ')
            self.check_court()
            self.check_user_reservations(user_reservations)
        else:
            logger.info('No courts available between {}-{} on {}.'.format(self.args['start'], self.args['end'],
                                                                          self.args['day']))

    def check_court(self):
        if self.args['court_number'] is None:
            court = input('Select court (number): ')
            self.sq.court_number = court
        logger.info('Checking reservations for court: {}'.format(self.sq.court_number))

    def check_user_reservations(self, user_reservations):
        if user_reservations:
            self.sq.book_courts(reservations=user_reservations)
        else:
            logger.info('No user reservations provided.')

    def set_config(self):
        if not os.path.isfile(SQWrapper.CONFIG_PATH) or self.args['is_rename']:
            user_name = input('Provide name and surname (Name Surname) '
                              'that were used to create Hasta La Vista account: ')
            self.create_config(user_name)
        self.sq.USER_ID = self.get_user_id()

    @staticmethod
    def create_config(user_name):
        user_name = user_name.lower().strip().split(' ')

        config = ConfigParser()
        config['USER_INFO'] = dict(name=user_name[0], surname=user_name[1])
        with open(SQWrapper.CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_user_id():
        config = ConfigParser()
        config.read(SQWrapper.CONFIG_PATH)
        name = config['USER_INFO']['NAME']
        surname = config['USER_INFO']['SURNAME']
        return '{}{}'.format(surname, name[0]).lower()

