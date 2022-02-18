import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--user',
                        help="Authenicated User for Gerrit Server",
                        default=None, required=True)
    common_parser.add_argument('--apikey',
                        help="API key of user to be used for authentication",
                        default=None, required=True)
    common_parser.add_argument('--gerritUrl',
                        help="Gerrit Server URL")

    common_parser_filter = argparse.ArgumentParser(add_help=False)
    common_parser_filter.add_argument('--project', help='Enter the Project name')
    common_parser_filter.add_argument('--branch',
                               help='Enter the Project name (Default is master)',
                               default="master")

    subparsers = parser.add_subparsers(dest="Operation")
    subparsers.add_parser('fetch_contributors', parents=[common_parser, common_parser_filter],
                          help='Fetches the contributor list from Gerrit')

    args = parser.parse_args()
    return args
