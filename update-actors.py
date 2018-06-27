#!/usr/bin/env python3
"""
Creates a new utils/actors.ts from the misp-galaxy threat actor cluster.
"""
import json
import io
import os


if __name__ == '__main__':
    try:
        os.remove('src/utils/actors.ts')
    except FileNotFoundError:
        pass
    with io.open('resources/misp-galaxy/clusters/threat-actor.json', 'r') as handle:
        data = json.loads(handle.read())
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
