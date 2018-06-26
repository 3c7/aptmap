#!/usr/bin/env python3
import json
import io
import os


if __name__ == '__main__':
    os.remove('src/utils/actors.ts')
    with io.open('resources/misp-galaxy/clusters/threat-actor.json', 'r') as handle:
        data = json.loads(handle.read())
        with io.open('src/utils/actors.ts', 'w') as output:
            output.write('let actors = ')
            output.write(json.dumps(data, indent=4))
            output.write(';\n\nexport default actors;')
    if os.path.isfile('src/utils/actors.ts'):
        print('New threat actor file was written.')
