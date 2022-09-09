#!/usr/bin/env python3

import requests
import xmltodict
import argparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
	print("[\033[1;33mi\033[0;0m] Accessible files:")

	for content in contents:
		if method == "aws":
			get_files_aws(content['Key'])
		if method == "domain":
			get_files_domain(url, content['Key'])

def get_info_bucket():
	r = requests.get(f'https://{BUCKET}.s3.amazonaws.com/', verify=False)
	return r

def get_files_domain(url, key):
	r = requests.get(url+key)
	if r.status_code == 200:
		print(f"{url+key} [\033[1;33m{str(len(r.text))}\033[0;0m]")
	
def get_files_aws(key):
	r = requests.get(f"https://{BUCKET}.s3.amazonaws.com/"+key, verify=False)
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
	parser.add_argument("-u", "--url", help="URL with bucket list")
	parser.add_argument("-m", "--method", help="Method to test files: (domain, aws)", required=True)
	parser.add_argument("-b", "--bucket", help="Bucket name")
	args = parser.parse_args()
	
	
	method = args.method
	
	print(banner)
	
	if args.url:
		main(url, method)
	else:
		BUCKET = args.bucket
		get_infos(get_info_bucket(),"None", method)
