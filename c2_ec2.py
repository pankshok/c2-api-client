#!/usr/bin/env python

import os
import sys
import boto
import argparse
import datetime

from multiprocessing import Process, Queue
from xml.dom.minidom import parseString


def _response_prettyprint(string):
	return parseString(string).toprettyxml()


def _configure_boto():
	"""Configure boto runtime for CROC Cloud"""

	if not boto.config.has_section("Boto"):
		boto.config.add_section("Boto")
	boto.config.set("Boto", "is_secure", "True")
	boto.config.set("Boto", "num_retries", "0")
	boto.config.set("Boto", "https_validate_certificates", "False")
	if not boto.config.has_section("Credentials"):
		boto.config.add_section("Credentials")
	boto.config.set("Credentials", "aws_access_key_id", os.environ["EC2_ACCESS_KEY"])
	boto.config.set("Credentials", "aws_secret_access_key", os.environ["EC2_SECRET_KEY"])


def make_parallel(action, args, threads, azs, field):
	"""Make parallel requests to CROC Cloud."""

	process_pool = []
	results_queue = Queue()

	connection = boto.connect_ec2_endpoint(os.environ["EC2_URL"])

	def request_maker(queue, args):
		print "Start: {0}".format(datetime.datetime.now())
		try:
			response = connection.make_request(action, args)
			response = response.read()
		except Exception as e:
			response = e

		queue.put((response,))

	try:
		if azs:
			process_pool = [ Process(target=request_maker, args=(results_queue, dict(args, **{field: az})),)
				for i in xrange(0, threads) for az in azs ]
		else:
			process_pool = [ Process(target=request_maker, args=(results_queue, args,))
				for i in xrange(0, threads) ]
		map(lambda p: p.start(), process_pool)
	finally:
		map(lambda p: p.join(), process_pool)

	return [ results_queue.get()[0] for p in process_pool ]


def parse_args():
	"""Parse incoming action and arguments as a dictionary
	for support AWS EC2 API requests format."""

	parser = argparse.ArgumentParser(prog="c2-ec2")
	parser.add_argument("-t", "--threads", metavar="threads", default=1,
		help="Number of threads to perform request.")
	parser.add_argument("--azs", metavar="AZ,[AZ,[...]]",
		help="Comma-separated list of AZs.")
	parser.add_argument("--az-field", default="AvailabilityZone",
		help="EC2 AZ request field. Default: 'AvailabilityZone'")
	parser.add_argument("action", help="The action that you want to perform.")
	parser.add_argument("parameters", nargs="*", help="Any parameters for the action. \
		Parameters specified by parameter key and parameter value separated by space.")
	args = parser.parse_args()

	azs = args.azs.split(",") if args.azs else None
	az_field = args.az_field
	threads = int(args.threads)
	action = args.action
	params = args.parameters
	parameters = dict(zip(params[::2], params[1::2]))

	return action, parameters, threads, azs, az_field


def main():
	"""Main function."""

	_configure_boto()
	action, args, threads, azs, az_field = parse_args()

	responses = make_parallel(action, args, threads, azs, az_field)
	for resp in responses:
		print _response_prettyprint(resp)

	return True


if __name__ == "__main__":
	sys.exit(os.EX_OK if main() else os.EX_SOFTWARE)
