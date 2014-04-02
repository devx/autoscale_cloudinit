#!/usr/bin/env python
import sys, base64

if len(sys.argv) < 2:
    print """Usage: %s FILE_TO_DECODE

              MFILE_TO_DECODE - The fle in b64 format, that you wan to decode

          """%sys.argv[0]
    sys.exit(0)

#base64.encode(open(sys.argv[1], 'rb'), open(sys.argv[2], 'wb'))
print base64.b64decode(open(sys.argv[1], 'rb').read())
