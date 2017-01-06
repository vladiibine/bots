import argparse
from collections import defaultdict
import base64

import requests
import uncurl

from vwh_importable_data import POST_RESP_BODY_2, POST_RESP_HEADERS_2, OPTIONS_RESP_BODY_2, \
	POST_RESP_BODY_1, OPTIONS_RESP_HEADERS_2, POST_RESP_HEADERS_1, OPTIONS_RESP_BODY_1, \
	OPTIONS_RESP_HEADERS_1, POST_REQ_2, OPTIONS_REQ_2, POST_REQ_1, OPTIONS_REQ_1, GAME_URL


def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--credentials-file', '-c',
		help='Path to a file containing base64.b64encode("Username:password")')
	parser.add_argument(
		'--login-url', '-l',
		help='Login url of the service which needs to authenticate me',
		default='https://armorgames.com/login')
	parser.add_argument(
		'--game-url', '-g',
		help='URL of the game to be played. Would require to be authenticated by the login service')

	return parser


def extract_credentials_from_file(credentials_file):
	"""
	:param credentials_file:
	:return: the username string and the hex encoded password
	"""
	try:
		with open(credentials_file, 'rb') as thefile:
			content = thefile.read()
			credentials_string = base64.b64decode(content)
			user, pwd = credentials_string.split(b':', 1)
			return user, pwd.hex()
	except (TypeError, IOError) as err:
		raise Exception(
			"Something's wrong with the credentials file: {}:"
			"\n{}".format(credentials_file, str(err)))


def cli_main_old():
	parser = get_parser()
	args = parser.parse_args()

	user, encoded_password = extract_credentials_from_file(args.credentials_file)

	session = requests.Session()
	response = session.post(
		args.login_url, data={'username': user, 'password': bytes.fromhex(encoded_password)})

	game_url = GAME_URL

	# when i log in and get the site below, what will be the src of the iframe?
	# armorgames.com/forge-of-gods-game/17842

	response2 = session.get('https://armorgames.com/forge-of-gods-game/17842')
	start_of_auth_token = response2.text.index('auth_token=')
	string_from_auth_token = response2.text[start_of_auth_token + 11]
	pass


# todo
# 1. Compare 2 request sets from get_league
class GetLeagueRequest(object):
	def __init__(self, options_request_str, post_request_str):
		"""Holds data regarding the `get_league` requests made. Strips out newline characters

		:param str options_request_str: the curl string for the OPTIONS http request
		:param str post_request_str: the curl string for the second http request, a POST
		"""
		self.options_request = uncurl.parse(options_request_str.replace('\n', ''))
		self.post_request = uncurl.parse(post_request_str.replace('\n', ''))


class GetLeagueResponse(object):
	def __init__(self, options_headers, options_body, post_headers, post_body):
		"""Holds data regarding the responses to the `get_league` requests.
		Copy paste the headers and the

		:param str options_headers: the string copy-pasted from google chrome, from the HEADERS section
		:param str options_body:
		:param str post_headers:
		:param str post_body:
		"""

		self.options_headers = defaultdict(lambda: [])
		

def cli_main():
	options_req_1 = OPTIONS_REQ_1
	
	post_req_1 = POST_REQ_1
	
	options_req_2 = OPTIONS_REQ_2

	post_req_2 = POST_REQ_2

	get_league_request_1 = GetLeagueRequest(options_req_1, post_req_1)
	get_league_request_2 = GetLeagueRequest(options_req_2, post_req_2)

	options_resp_headers_1 = OPTIONS_RESP_HEADERS_1
	options_resp_body_1 = OPTIONS_RESP_BODY_1

	post_resp_headers_1 = POST_RESP_HEADERS_1

	post_resp_body_1 = POST_RESP_BODY_1

	options_resp_headers_2 = OPTIONS_RESP_HEADERS_2

	options_resp_body_2 = OPTIONS_RESP_BODY_2

	post_resp_headers_2 = POST_RESP_HEADERS_2
	post_resp_body_2 = POST_RESP_BODY_2

	get_league_response_1 = GetLeagueResponse(
		options_resp_headers_1, options_resp_body_1, post_resp_headers_1, post_resp_body_1)

	get_league_response_2 = GetLeagueResponse(
		options_resp_headers_2, options_resp_body_2, post_resp_headers_2, post_resp_body_2)

if __name__ == '__main__':
	cli_main()

