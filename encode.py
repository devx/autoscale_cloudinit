#!/usr/bin/env python
import sys, base64

if len(sys.argv) < 2:
    print """Usage: %s FILE_TO_ENCODE

              MFILE_TO_ENCODE - The fle you wan to encode in Base64

          """%sys.argv[0]
    sys.exit(0)

#base64.encode(open(sys.argv[1], 'rb'), open(sys.argv[2], 'wb'))
print base64.b64encode(open(sys.argv[1], 'rb').read())
