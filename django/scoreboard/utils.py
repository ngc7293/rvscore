import json

from .models import Time, Car

def add_times_from_json(body):
    """ Parse JSON and insert new times in database """
    new = 0
    data = json.loads(body)
    for mode in data:
        for category in data[mode]:
            for track in data[mode][category]:
                for time in data[mode][category][track]:
                    new += insert_time(mode, category, track, time)
    return new


def insert_time(mode, category, track, time):
    """ Insert a Time row in the database """
    try:
        Time(time=time['time'], profile=time['profile'], car=Car.objects.get(name=time['car']), track=track, mode=mode).save()
        return 1
    except:
        return 0


def get_times_json():
    """ Get JSON of best times """
    modes = ['normal', 'mirror', 'reverse', 'reversemirror']
    categories = ['rookie', 'amateur', 'advanced', 'semi-pro', 'pro']
    tracks = ['botanical gardens', 'rooftops', 'ghost town 1', 'ghost town 2', 'museum 1', 'museum 2', 'supermarket 1', 'supermarket 2', 'toytanic 1', 'toytanic 2', 'toys in the hood 1', 'toys in the hood 2', 'toy world 1', 'toy world 2']

    data = {}
    for mode in modes:
        empty_mode = True
        data[mode] = {}

        for category in categories:
            empty_cat = True
            data[mode][category] = {}

            for track in tracks:
                times = get_times(mode, category, track)
                if times:
                    data[mode][category][track] = times
                    empty_cat = False

            if empty_cat:
                data[mode].pop(category)
            else:
                empty_mode = False

        if empty_mode:
            data.pop(mode)

    return json.dumps(data)


def get_times(mode, category, track):
    """
        Get times according to param 
        Currently this only returns the single best time
    """
    times = []
    for time in Time.objects.filter(track=track, mode=mode, car__category=category).order_by('time')[:1]:
        times.append({
            'time': time.time,
            'profile': time.profile,
            'car': time.car.name
        })
    return times

def get_tracks():
    pass

def get_modes(track):
    pass