#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import ssl
import boto
import argparse
import datetime

from xml.dom.minidom import parseString


# dirty monkeypatching (https://www.python.org/dev/peps/pep-0476/)
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	ssl._create_default_https_context = _create_unverified_https_context


def _response_prettyprint(string):
	return parseString(string).toprettyxml(encoding="utf-8")


def _configure_boto():
	"""Configure boto runtime for CROC Cloud"""

	if not boto.config.has_section("Boto"):
		boto.config.add_section("Boto")
	boto.config.set("Boto", "is_secure", "True")
	boto.config.set("Boto", "num_retries", "0")
	boto.config.set("Boto", "https_validate_certificates", "False")
	boto.config.set("Boto", "validate_certs", "False")
	if not boto.config.has_section("Credentials"):
		boto.config.add_section("Credentials")
	boto.config.set("Credentials", "aws_access_key_id", os.environ["EC2_ACCESS_KEY"])
	boto.config.set("Credentials", "aws_secret_access_key", os.environ["EC2_SECRET_KEY"])


def make_request(action, args):
        connection = boto.connect_ec2_endpoint(os.environ["EC2_URL"])
        print("Start: {0}".format(datetime.datetime.now()))
        try:
                response = connection.make_request(action, args)
                response = response.read()
        except Exception as e:
                response = e
        return response


def parse_args():
	"""Parse incoming action and arguments as a dictionary
	for support AWS EC2 API requests format."""

	parser = argparse.ArgumentParser(prog="c2-ec2")
	parser.add_argument("action", help="The action that you want to perform.")
	parser.add_argument("parameters", nargs="*", help="Any parameters for the action. \
		Parameters specified by parameter key and parameter value separated by space.")
	args = parser.parse_args()

	action = args.action
	params = args.parameters
	parameters = dict(zip(params[::2], params[1::2]))

	return action, parameters


def main():
	"""Main function."""
	_configure_boto()
	action, args = parse_args()
	response = make_request(action, args)

	if sys.platform == "win32":
		import msvcrt
		msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
		lines = "\r\n".join(map(str, _response_prettyprint(response).splitlines()))
		os.write(sys.stdout.fileno(), bytes(lines))
		os.write(sys.stdout.fileno(), "\r\n")
	else:
		print(_response_prettyprint(response))

	return True


if __name__ == "__main__":
	sys.exit(0 if main() else 1)
