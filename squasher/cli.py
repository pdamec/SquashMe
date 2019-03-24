import argparse
import logging
from pprint import pprint
from datetime import datetime
from .squasher import SquashMe


def create_parser():
    today = datetime.today().strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='Package for sport centre automation.')
    parser.add_argument('--court_number', type=int)
    parser.add_argument('--discipline', type=str, default='squash')
    parser.add_argument('--start', type=str, default="6:00")
    parser.add_argument('--end', type=str, default="23:30")
    parser.add_argument('--day', type=str, default=today)
    return parser.parse_args()


def main():
    # TBD: delete.
    logging.basicConfig(level=logging.INFO)

    args = create_parser()

    sq = SquashMe(args.court_number, args.discipline, args.start, args.end, args.day)
    free_reservations = sq.show_free_reservations()

    if free_reservations:
        pprint(free_reservations)
        user_reservations = input('Select hours to reserve (hh:mm-hh:mm or hh:mm): ')
        if user_reservations:
            sq.book_courts(reservations=user_reservations)
        else:
            logging.info('No user reservations provided.')
    else:
        logging.info('No courts available between {}-{} on {}.'.format(args.start, args.end, args.day))
