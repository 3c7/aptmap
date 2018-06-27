#!/usr/bin/env python3
"""
Creates a new utils/actors.ts from the misp-galaxy threat actor cluster.
"""
import json
import io
import os
try:
    import iso3166
except:
    print('You need to have the iso3166 module installed:\npip install -r requirements.txt')


if __name__ == '__main__':
    try:
        os.remove('src/utils/actors.ts')
    except FileNotFoundError:
        pass
    with io.open('resources/misp-galaxy/clusters/threat-actor.json', 'r') as handle:
        data = json.loads(handle.read())

        # Convert country code
        print('Converting country codes...')
        for actor in data['values']:
            if actor['meta'].get('country', None):
                actor['meta']['country'] = iso3166.countries.get(actor['meta']['country'])[2]

        if not os.path.isdir('src/utils'):
            os.mkdir('src/utils')
        with io.open('src/utils/actors.ts', 'w') as output:
            output.write('let actors = ')
            output.write(json.dumps(data, indent=4))
            output.write(';\n\nexport default actors;')
    if os.path.isfile('src/utils/actors.ts'):
        print('New threat actor file was written.')
    else:
        print('Could not update threat actors.')
        exit(1)
