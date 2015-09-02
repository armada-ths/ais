import requests
import json

def make_placement():
    tables = open('/home/jw/projects/armada/ais/lib/gasque_tables.json', 'r').read()
    persons = open('/home/jw/projects/armada/ais/lib/gasque_attendances.json', 'r').read()

    api_url = 'http://bordsplacering.armada.nu:9292/do_placement'
    payload = {'tables':tables, 'persons':persons}
    data=requests.post(api_url, data=payload)

    json_data = json.loads(data.text)

    output = open('/home/jw/projects/armada/ais/lib/placement.json', 'w')
    output.write('[\n')
    for person in json_data['persons']:
        output.write("{\"id\":\"%s\",\"table_id\":\"%s\",\"seat\":\"%s\"},\n"%(person['id'],person['placement']['table_id'],person['placement']['seat']))

    output.seek(-2, 2)
    output.write('\n]')
