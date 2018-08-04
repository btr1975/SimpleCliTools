import logging
import os
import sys
from argparse import ArgumentParser
import persistentdatatools as pdt
import ipaddresstools as ipv4
import module as mod
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'dev'
__version_info__ = (1, 0, 13, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

BASE_DIR = None
DATA_DIR = None
INPUT_DIR = None
OUTPUT_DIR = None
LOGGING_DIR = None
LOGGER = logging.getLogger(__name__)
LOGGING_LEVEL = None

if __name__ == '__main__':
    if __status__ == 'prod':
        BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    elif __status__ == 'dev':
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    INPUT_DIR = os.path.join(BASE_DIR, 'Input')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'Output')
    LOGGING_DIR = os.path.join(BASE_DIR, 'Logs')
    DATA_DIR = os.path.join(BASE_DIR, 'Data')
    LOGGING_LEVEL = logging.WARNING
    pdt.verify_directory('Input', BASE_DIR, directory_create=True)
    pdt.verify_directory('Output', BASE_DIR, directory_create=True)
    pdt.verify_directory('Logs', BASE_DIR, directory_create=True)
    pdt.verify_directory('Data', BASE_DIR, directory_create=True)
    existing_input_files = pdt.list_files_in_directory(INPUT_DIR)
    logging.basicConfig(format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
                        filename=os.path.join(LOGGING_DIR, 'logs.txt'))
    logging.getLogger().setLevel(LOGGING_LEVEL)
    LOGGER.warning('Logging started!!')

    arg_parser = ArgumentParser(description='Simple Command Line Tools')
    arg_parser.add_argument('-f', '--folder', help='Put output file in a folder, name of the folder')
    arg_parser.add_argument('-v', '--version', action='version', version=__version__)
    subparsers = arg_parser.add_subparsers(title='subcommands', description='Valid subcommands', help='CLI Help')

    arg_parser_pl = subparsers.add_parser('pldiff', help='Prefix-List Differ')
    arg_parser_pl.set_defaults(which_sub='pldiff')
    arg_parser_pl.add_argument('filename_a', help='The "A" Side file name you saved the Prefix-List to')
    arg_parser_pl.add_argument('filename_b', help='The "B" Side file name you saved the Prefix-List to')
    arg_parser_pl.add_argument('output_filename', help='The name of the file you want to send output to')

    arg_parser_acl = subparsers.add_parser('acldiff', help='ACL Differ')
    arg_parser_acl.set_defaults(which_sub='acldiff')
    arg_parser_acl.add_argument('filename_a', help='The "A" Side file name you saved the ACL to')
    arg_parser_acl.add_argument('filename_b', help='The "B" Side file name you saved the ACL to')
    arg_parser_acl.add_argument('output_filename', help='The name of the file you want to send output to')

    arg_parser_acl_pl_convert = subparsers.add_parser('acltopl', help='Convert ACL to Prefix-List')
    arg_parser_acl_pl_convert.set_defaults(which_sub='acltopl')
    arg_parser_acl_pl_convert.add_argument('filename_a', help='The file name you saved the ACL to')
    arg_parser_acl_pl_convert.add_argument('output_filename', help='The name of the file you want to send output to')

    arg_parser_file_diff = subparsers.add_parser('filediff', help='Line Differ')
    arg_parser_file_diff.set_defaults(which_sub='filediff')
    arg_parser_file_diff.add_argument('filename_a', help='The "A" Side file name you saved')
    arg_parser_file_diff.add_argument('filename_b', help='The "B" Side file name you saved')
    arg_parser_file_diff.add_argument('-f', '--format', help='Formats are html, and xlsx', required=True)
    arg_parser_file_diff.add_argument('-o', '--oneoff', help='Used in case A CEF table changes to a CIDR '
                                                             'notation next hop , make the CDIR notation file File B',
                                      action='store_true')

    arg_parser_file_diff = subparsers.add_parser('folderdiff', help='Diffs Files in 2 Folders')
    arg_parser_file_diff.set_defaults(which_sub='folderdiff')
    arg_parser_file_diff.add_argument('folder_a', help='Folder "A"')
    arg_parser_file_diff.add_argument('folder_b', help='Folder "B"')
    arg_parser_file_diff.add_argument('-o', '--oneoff', help='Used in case A CEF table changes to a CIDR '
                                                             'notation next hop, make the CDIR notation file Folder B',
                                      action='store_true')

    arg_parser_config_split = subparsers.add_parser('configsplit', help='Config Splitter')
    arg_parser_config_split.set_defaults(which_sub='configsplit')
    arg_parser_config_split.add_argument('filename_a', help='The file name of the show run')
    arg_parser_config_split.add_argument('-t', '--text', help='Output text files, default is to output to Excel',
                                         action='store_true')

    arg_parser_convert_mcast_acl = subparsers.add_parser('convertmcastacltorm',
                                                         help='Convert Mcast ACL to Route-Map from a show '
                                                              'command, not the config')
    arg_parser_convert_mcast_acl.set_defaults(which_sub='convertmcastacltorm')
    arg_parser_convert_mcast_acl.add_argument('-m', '--matches', help='Look for matches only', action='store_true')
    arg_parser_convert_mcast_acl.add_argument('filename_a', help='The file name os the show info')
    arg_parser_convert_mcast_acl.add_argument('new_rm_name', help='The name of the Route-Map to create')
    arg_parser_convert_mcast_acl.add_argument('rp_address', help='The RP address for the mcast config')

    arg_parser_ipaddresstools = subparsers.add_parser('ipaddresstools', help="Convert IP Addres's to several formats")
    arg_parser_ipaddresstools.set_defaults(which_sub='ipaddresstools')
    arg_parser_ipaddresstools.add_argument('-s', '--subnets', help='Display all available subnets', action='store_true')
    arg_parser_ipaddresstools.add_argument('-a', '--all_hosts', help='Display all available host ip',
                                           action='store_true')
    arg_parser_ipaddresstools.add_argument('ip_address_cidr', help='The IP address in the following format X.X.X.X/X')

    arg_parser_ip_agg = subparsers.add_parser('aggregate', help='Aggregate a list of subnets')
    arg_parser_ip_agg.set_defaults(which_sub='aggregate', lower='0', upper='32')
    arg_parser_ip_agg.add_argument('filename_a', help='The file name of the list of subnets.')
    arg_parser_ip_agg.add_argument('-l', '--lower', help='Lower CIDR constraint')
    arg_parser_ip_agg.add_argument('-u', '--upper', help='Upper CIDR constraint')

    args = arg_parser.parse_args()

    try:

        check_subs_two_files = ('pldiff', 'acldiff', 'filediff')
        check_subs_one_file = ('acltopl', 'configsplit', 'convertmcastacltorm', 'aggregate')

        if args.which_sub in check_subs_two_files:
            if args.filename_a not in existing_input_files or args.filename_b not in existing_input_files:
                LOGGER.error('Entered bad file names {filename_a} {filename_b} '
                             '{existing}'.format(filename_a=args.filename_a,
                                                 filename_b=args.filename_b,
                                                 existing=existing_input_files))
                print('Existing file names')
                for file_name in existing_input_files:
                    print(file_name)
                sys.exit('Please check the names of your input files.  One, or both do not exist!')

        elif args.which_sub in check_subs_one_file:
            if args.filename_a not in existing_input_files:
                LOGGER.error('Entered bad file name {filename_a} {existing}'.format(filename_a=args.filename_a,
                                                                                    existing=existing_input_files))
                print('Existing file names')
                for file_name in existing_input_files:
                    print(file_name)
                sys.exit('Please check the names of your input file.  It does not exist!')

        if args.folder:
            pdt.verify_directory(args.folder, OUTPUT_DIR, directory_create=True)
            OUTPUT_DIR = os.path.join(OUTPUT_DIR, args.folder)

        if args.which_sub == 'pldiff':
            mod.scripts.pl_diff.prefix_list_diff(args.filename_a, args.filename_b, args.output_filename, INPUT_DIR,
                                                 OUTPUT_DIR)

        elif args.which_sub == 'acltopl':
            mod.scripts.acl_diff.acl_to_prefix_list_converter(args.filename_a, args.output_filename, INPUT_DIR,
                                                              OUTPUT_DIR)

        elif args.which_sub == 'acldiff':
            mod.scripts.acl_diff.acl_diff(args.filename_a, args.filename_b, args.output_filename, INPUT_DIR, OUTPUT_DIR)

        elif args.which_sub == 'filediff':
            formats = ('html', 'xlsx')
            if args.format not in formats:
                LOGGER.critical('Format entered {}'.format(args.format))
                arg_parser.print_help()
                raise ValueError('The options for file format are html, and xlsx!!')

            else:
                mod.scripts.file_diff(args.filename_a, args.filename_b, INPUT_DIR, OUTPUT_DIR, args.oneoff, args.format)

        elif args.which_sub == 'folderdiff':
            if not pdt.verify_directory(args.folder_a, INPUT_DIR, directory_create=False) or not \
                    pdt.verify_directory(args.folder_b, INPUT_DIR, directory_create=False):
                LOGGER.critical('One, or all of the input folders do not exist')
                arg_parser.print_help()
                raise ValueError('One, or all of the input folders do not exist, please verify!!')

            else:
                mod.scripts.multi_file_diff(os.path.join(INPUT_DIR, args.folder_a),
                                            os.path.join(INPUT_DIR, args.folder_b), OUTPUT_DIR, args.oneoff, DATA_DIR)

        elif args.which_sub == 'configsplit':
            mod.scripts.ConfigSplitter(args.filename_a, INPUT_DIR, OUTPUT_DIR, args.text)

        elif args.which_sub == 'convertmcastacltorm':
            if ipv4.ucast_ip(args.rp_address, return_tuple=False):
                mod.scripts.AclToRmHits(args.new_rm_name, args.rp_address, args.matches,
                                        args.filename_a, INPUT_DIR, OUTPUT_DIR)

            else:
                LOGGER.critical('Invalid RP address {e}'.format(e=args.rp_address))
                arg_parser.print_help()
                raise ValueError('Invalid RP address {e}'.format(e=args.rp_address))

        elif args.which_sub == 'ipaddresstools':
            if ipv4.ip_mask(args.ip_address_cidr, return_tuple=False):

                if args.subnets:
                    for subnet in mod.scripts.get_subnets(args.ip_address_cidr):
                        print('{subnet} or {mask}'.format(subnet=subnet[0], mask=subnet[1]))

                elif args.all_hosts:
                    for ip_address in mod.scripts.get_host_ips(args.ip_address_cidr):
                        print(ip_address)

            else:
                LOGGER.critical('Invalid IP address {e}'.format(e=args.ip_address_cidr))
                arg_parser.print_help()
                raise ValueError('Invalid IP address {e}'.format(e=args.ip_address_cidr))

        elif args.which_sub == 'aggregate':
            mod.scripts.get_network_aggregator(args.filename_a, args.lower, args.upper, INPUT_DIR, OUTPUT_DIR)

    except AttributeError as e:
        LOGGER.critical(e)
        arg_parser.print_help()
