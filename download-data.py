import requests, json, time, os


files = {
	'pollingStations.json'	: 'https://belarus2020.org/pollingStations.json',
	'whitelist.json'		: 'https://belarus2020.org/data/results/whitelist.json',
	'total.json'			: 'https://belarus2020.org/data/results/total.json',
	'unassigned.json'		: 'https://belarus2020.org/data/results/byStation/unassigned.json',
	'stats.json'			: 'https://d3kxokrdpc64vo.cloudfront.net/stats.json',
}
# for file_name, url in files.items():
# 	response = requests.get(url)
# 	with open(f'data/{file_name}', 'w', encoding='utf-8') as f:
# 		json.dump(response.json(), f, ensure_ascii=False, indent=4)


# gather station codes
stations_code = set()
with open(f'data/pollingStations.json', 'r', encoding='utf-8') as f:
	stations = json.load(f)
with open(f'data/whitelist.json', 'r', encoding='utf-8') as f:
	whitelist= json.load(f)

for station in stations:
	stations_code.add(station['code'])
stations_code.update(whitelist['forgery'])
stations_code.update(whitelist['truth'])
# fix a bug in the data
stations_code.remove('проспект Мира, дома 15, 21, 25, 25а, 256, 25в, 25г, 27, 27а, 276, 29; улица Левая Дубравенка от проспекта Мира до Клубного Оврага; 4-й Октябрьский переулок; улица Бурденко, дома 10, 12.')


target = {
	'byStation'	: 'https://belarus2020.org/data/results/byStation/{}.json',
	'photos'   	: 'https://belarus2020.org/data/results/photos/{}.json',
	'Quarantine': 'https://api.golos2020.org/Quarantine/{}',
}
for code in stations_code:
	# time.sleep(5)  # avoid throttling
	for group, url_pattern in target.items():
		if (os.path.exists(f'data/{group}/{code}.json')):
			continue
		url = url_pattern.format(code)
		print(url)
		response = requests.get(url)
		try:
			with open(f'data/{group}/{code}.json', 'w', encoding='utf-8') as f:
				json.dump(response.json(), f, ensure_ascii=False, indent=4)
		except:
			print('Error')

# download photos
