#!/usr/bin/env python3

import requests
import xmltodict
import argparse

banner = """
BAFILES
========
Bucket Access Files
 
"""

def get_infos(resp, url, method):
	global BUCKET
	xml = xmltodict.parse(resp.text)
	BUCKET = xml['ListBucketResult']['Name']
	contents = xml['ListBucketResult']['Contents']
	print(f"Bucket name: \033[1;33m{BUCKET}\033[0;0m")
	print(f"Total files found: {str(len(contents))}")
	print("[i] Accessible files:")

	for content in contents:
		if method == "aws":
			get_files_aws(content['Key'])
		if method == "domain":
			get_files_domain(url, content['Key'])

def get_files_domain(url, key):
	r = requests.get(url+key)
	if r.status_code == 200:
		print(f"{url+key} [\033[1;33m{str(len(r.text))}\033[0;0m]")
	
def get_files_aws(key):
	r = requests.get(f"https://{BUCKET}.s3.amazonaws.com/"+key)
	if r.status_code == 200:
		print(f"https://{BUCKET}.s3.amazonaws.com/{key} [\033[1;33m{str(len(r.text))}\033[0;0m]")
	
def get_s3(url):
	req = requests.get(url, stream=True)
	return req

def main(url, method):
	get_infos(get_s3(url), url, method)

if __name__ == '__main__':
	BUCKET = ""
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument("-u", "--url", help="URL with bucket list", required=True)
	parser.add_argument("-m", "--method", help="Method to test files: (domain, aws)", required=True)
	args = parser.parse_args()
	
	url = args.url
	method = args.method
	print(banner)
	main(url, method)