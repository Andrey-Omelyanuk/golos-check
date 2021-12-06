import requests, json, time, os


# get data from file of download from url and save it to file
def get_data(file_name, url):
    data = None
    if not os.path.exists(file_name):
        print(f"Download {url}")
        response = requests.get(url)
        with open(file_name, 'w', encoding='utf-8') as f:
            try:
                data = response.json()
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"Saved in {file_name}")
            except Exception as e:
                print(f"Empty data")
                data = {} 
    else:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(file_name, "Empty data")
            data = {} 
    return data


# download base data
pollingStations = get_data('data/pollingStations.json'  , 'https://belarus2020.org/pollingStations.json')
whitelist       = get_data('data/whitelist.json'        , 'https://belarus2020.org/data/results/whitelist.json')
total           = get_data('data/total.json'            , 'https://belarus2020.org/data/results/total.json')
unassigned      = get_data('data/unassigned.json'       , 'https://belarus2020.org/data/results/byStation/unassigned.json')
stats           = get_data('data/stats.json'            , 'https://d3kxokrdpc64vo.cloudfront.net/stats.json')

# gather station codes
stations_code = set()
for station in pollingStations: 
    stations_code.add(station['code'])
stations_code.update(whitelist['forgery'])
stations_code.update(whitelist['truth'])
# fix a bug in the data
stations_code.remove('проспект Мира, дома 15, 21, 25, 25а, 256, 25в, 25г, 27, 27а, 276, 29; улица Левая Дубравенка от проспекта Мира до Клубного Оврага; 4-й Октябрьский переулок; улица Бурденко, дома 10, 12.')


# download details of stations
stations = {} 
for code in stations_code:
    by_station = get_data(f'data/byStation/{code}.json', f'https://belarus2020.org/data/results/byStation/{code}.json')
    x = {
        'photos'    : get_data(f'data/photos/{code}.json'       , f'https://belarus2020.org/data/results/photos/{code}.json'),
        'quarantine': get_data(f'data/Quarantine/{code}.json'   , f'https://api.golos2020.org/Quarantine/{code}'),
    }
    stations[code] = {**by_station, **x}

for station in pollingStations:
    code = station['code']
    if code in stations_code:
        stations[code] = {**stations[code], **station}


# TODO: download photos


# gather everything in one file /work/data.json 
with open('work/data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'stations'  : stations,
        'whitelist' : whitelist,
        'total'     : total,
        'unassigned': unassigned,
        'stats'     : stats
    }, f, ensure_ascii=False, indent=4)
