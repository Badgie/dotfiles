from urllib import request
from urllib.error import URLError

for x in range(0, 200):
    try:
        request.urlretrieve(f'https://www.dmi.dk/fileadmin/assets/img/{x}.svg', f'./svg/{x}.svg')
    except URLError:
        continue
