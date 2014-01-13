#!/usr/bin/env python

import argparse
import boto
import sys
import os
from xml.dom.minidom import parseString

def _response_prettyprint(string):
	return parseString(string).toprettyxml()

def configure_boto():
	""" Configure boto runtime for CROC Cloud"""
	
	if not boto.config.has_section("Boto"):
		boto.config.add_section("Boto")
	boto.config.set("Boto", "is_secure", "True")
	boto.config.set("Boto", "num_retries", "0")
	boto.config.set("Boto", "https_validate_certificates", "True")
	if not boto.config.has_section("Credentials"):
		boto.config.add_section("Credentials")
	boto.config.set("Credentials", "aws_access_key_id", os.environ["EC2_ACCESS_KEY"])
	boto.config.set("Credentials", "aws_secret_access_key", os.environ["EC2_SECRET_KEY"])


def parse_args():
	""" Parse incoming action and arguments as a dictionary for support AWS EC2 API requests format """
	
	parser = argparse.ArgumentParser(prog='c2-ec2')
	parser.add_argument('action', help='The action that you want to perform.')
	parser.add_argument('parameters', nargs='*', help='Any parameters for the action. Parameters specified by parameter key and parameter value separated by space.')
	args = parser.parse_args()
	
	action = args.action
	params = args.parameters
	parameters = dict(zip(params[::2], params[1::2]))

	return action, parameters

def main():
	"""Main function"""
	
	configure_boto()
	action, args = parse_args()
	response = None
	try:
		connection = boto.connect_ec2_endpoint(os.environ["EC2_URL"])
		response = connection.make_request(action, args)	
	except Exception as e:
		print e
		return False
	
	print _response_prettyprint(response.read())
	return True

if __name__ == "__main__":
	sys.exit(os.EX_OK if main() else os.EX_SOFTWARE)
