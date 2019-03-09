import argparse
from .squasher import SquashMe


def create_parser():
    parser = argparse.ArgumentParser(description='Lib for automation.')
    parser.add_argument('--court_number', type=int, help='an integer for the accumulator')
    parser.add_argument('--discipline', type=str)
    parser.add_argument('--start', type=str, default="6:00")
    parser.add_argument('--end', type=str, default="23:30")
    return parser.parse_args()


def main():
    args = create_parser()
    sq = SquashMe(args.court_number, args.discipline, args.start, args.end)
    sq.show_reservations()
