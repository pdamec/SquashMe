# SquashMe

Tired of constantly trying to find free court for your beloved squash? 
Maybe some badminton game? Fear not. Squash-Me is a package for 
automating <i>Hasta La Vista</i> - one of the biggest sport centres in Wroclaw.

With it, you can constantly fetch and reserve free courts at desired time.

## Installation
Either:
- Install directly from repository
```
pip install git+ssh://{USER}@github.com:pdamec/squash-me.git
```

- Clone repository and install with setuptools
```
Git clone {USER}@github.com:pdamec/squash-me.git
python setup.py install
```

## Usage
### Command Line

```
sq-me --court_number 4 --discipline squash --start 17:30 --end 19:00 --day 2019-03-28
```

Where:
- court_number: desired court. If not provided, SquashMe searches at all courts.
- discipline: supports squash, badminton and table_tennis. Default is squash.
- start: from what time look for available courts. Default set for 06:00 AM.
- end: until what time look for available courts. Default set for 12 AM.
- day: on what day free courts should be checked. Default is day of program execution.

IMPORTANT NOTE: start, end arguments support 24-hour format.
 
For more info, execute:

```
sq-me --help
```

