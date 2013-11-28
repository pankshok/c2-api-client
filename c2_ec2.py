#!/usr/bin/env python
import os
import sys
import urlparse

import boto
import xml.dom.minidom
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from xml.dom.minidom import parseString
from StringIO import StringIO

if not boto.config.has_section("Boto"):
    boto.config.add_section("Boto")

boto.config.set("Boto", "num_retries", "0")

scheme, netloc, path, params, query, fragment = urlparse.urlparse(os.environ['EC2_URL'])
host, port, rest = (netloc + "::").split(":", 2)
conn = EC2Connection(
        is_secure=(scheme == 'https'),
        region=RegionInfo(name="croc", endpoint=host),
        port=int(port) if port else None,
        path=path,
        aws_access_key_id=os.environ['EC2_ACCESS_KEY'],
        aws_secret_access_key=os.environ['EC2_SECRET_KEY']
    )

sys.argv.pop(0)
action = sys.argv.pop(0)
args = dict(zip(sys.argv[::2], sys.argv[1::2]))

resp = conn.make_request(action, args)
print parseString(resp.read()).toprettyxml()
sys.exit(0 if resp.status == 200 else 1)
