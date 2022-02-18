import lib.arg_parser as arg_parser
from lib.auth import Auth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
GERRIT_MAGIC_JSON_PREFIX = ")]}'\n"

def _decode_response(response):
    if response.startswith(GERRIT_MAGIC_JSON_PREFIX):
        index = len(GERRIT_MAGIC_JSON_PREFIX)
        content = response[index:]
    try:
        return json.loads(content)
    except ValueError:
        raise

def get_all_contributors(args, auth):
    contributors = []
    query_all = "changes/?q=branch:%s status:merged" % args.branch
    content = requests.get("%s/a/%s" %(args.gerritUrl, query_all), auth=auth, verify=False).text
    all_commits = _decode_response(content)
    for commits in all_commits:
        contributors.append(commits['owner']['_account_id'])
        contributors.append(commits['submitter']['_account_id'])
    return set(contributors)

def fetch_account(ids, args, auth):
    accounts = []
    for user in ids:
        query = "accounts/%s/detail" % (user)
        content = requests.get("%s/a/%s" %(args.gerritUrl, query), auth=auth, verify=False).text
        get_accounts = _decode_response(content)
        accounts.append(get_accounts['email'])
    print(accounts)
    return accounts

def main():
    try:
        args = arg_parser.parse_args()
        auth = Auth(args.user, args.apikey)
        auth_token = Auth.get_auth(auth)
        if "fetch_contributors" in args.Operation:
            all_contributors_ids = get_all_contributors(args, auth_token)
            all_contributors_mails = fetch_account(all_contributors_ids, args, auth_token)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
