import argparse
import logging
from datetime import datetime
from .wrapper import SQWrapper


def create_parser():
    today = datetime.today().strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='Package for sport centre automation.')
    parser.add_argument('--court_number', type=int)
    parser.add_argument('--discipline', type=str, default='squash')
    parser.add_argument('--start', type=str, default="6:00")
    parser.add_argument('--end', type=str, default="23:30")
    parser.add_argument('--day', type=str, default=today)
    parser.add_argument('--rename', type=bool, nargs='?', const=True)
    return parser.parse_args()


def main():
    # TBD: delete.
    logging.basicConfig(level=logging.INFO)

    args = create_parser()

    wrapper = SQWrapper(court_number=args.court_number, discipline=args.discipline, start=args.start, end=args.end,
                        day=args.day, is_rename=args.rename)
    wrapper.start_me_please()
