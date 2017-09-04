import logging
import os
import persistentdatatools as pdt
import ipaddresstools as ipv4
import module as mod
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 2, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def get_subnets(ip_address_cidr):
    """
    Function to get all possible subnets in a ip/cidr combo
    :param ip_address_cidr: IP in the following format X.X.X.X/X
    :return: 
        A list of sets, of subnets
    
    """
    LOGGER.debug('Starting Function get_subnets')
    final_list = list()
    ip_net, cidr = ipv4.ip_mask(ip_address_cidr, return_tuple=True)
    test = ipv4.all_subnets_possible(ip_net, cidr)
    for subnet in test:
        subnet_split = subnet.split('/')
        final_list.append((subnet, ipv4.mask_conversion[int(subnet_split[1])]['MASK']))

    return final_list


def get_host_ips(ip_address_cidr):
    """
    Function to get all ip address's in a ip/cidr combo
    :param ip_address_cidr: IP in the following format X.X.X.X/X
    :return: 
        A list of ip address's
    
    """
    LOGGER.debug('Starting Function get_host_ips')
    ip_net, cidr = ipv4.ip_mask(ip_address_cidr, return_tuple=True)
    return ipv4.all_ip_address_in_subnet(ip_net, cidr)


def get_network_aggregator(file_a, lower_constraint, upper_constraint, input_dir, output_dir,):
    """
    Function to create a spreadsheet of possible aggregates
    :param file_a: The file name
    :param lower_constraint: a value between 0  and 32
    :param upper_constraint: a value between 0  and 32
    :param input_dir: The input directory
    :param output_dir: The output directory
    :return: 
        None
    
    """
    LOGGER.debug('Starting Function get_network_aggregator')
    temp_list_good = list()
    temp_list_bad = list()
    temp_possible_set = set()
    final_dict = dict()
    top_n_dict = None

    a_list = pdt.file_to_list(file_a, input_dir)

    for line in a_list:
        line_split = line.split()
        for item in line_split:
            if ipv4.ip_mask(item, return_tuple=False):
                temp_list_good.append(item)

            else:
                temp_list_bad.append(item)

    pdt.list_to_file(temp_list_good, pdt.file_name_increase('good_ip.txt', output_dir), output_dir)
    pdt.list_to_file(temp_list_bad, pdt.file_name_increase('bad_ip.txt', output_dir), output_dir)

    for good_cidr_subnet in temp_list_good:
        good_cidr_subnet_split = good_cidr_subnet.split('/')
        if good_cidr_subnet_split[0] != '0.0.0.0':
            for net in ipv4.all_subnets_shorter_prefix(good_cidr_subnet_split[0], good_cidr_subnet_split[1],
                                                       include_default=False):
                net_split = net.split('/')
                if int(net_split[1]) >= int(lower_constraint) and int(net_split[1]) <= int(upper_constraint):
                    temp_possible_set.add(net)

    for final_net in temp_possible_set:
        final_dict[final_net] = {
            'matched': list(),
            'unmatched': list(),
        }
        for good_cidr_subnet in temp_list_good:
            good_cidr_subnet_split = good_cidr_subnet.split('/')
            if final_net in ipv4.all_subnets_shorter_prefix(good_cidr_subnet_split[0], good_cidr_subnet_split[1],
                                                            include_default=False):
                final_dict[final_net]['matched'].append(good_cidr_subnet)

            else:
                final_dict[final_net]['unmatched'].append(good_cidr_subnet)

    for key in final_dict:
        top_n_dict = get_top_n(top_n_dict, final_dict, key, 10)

    spread_sheet_file_name = pdt.file_name_increase('aggregator.xlsx', output_dir)
    spread_sheet = mod.scripts.WriteXlsxAggregate(os.path.join(output_dir, spread_sheet_file_name), final_dict,
                                                  top_n_dict, len(temp_list_good))
    spread_sheet.write_spreadsheet()


def get_top_n(orig_top_n_dict, orig_dict, key, top_n):
    if not orig_top_n_dict:
        temp_orig_top_n_dict = dict()

    else:
        temp_orig_top_n_dict = orig_top_n_dict.copy()

    if len(temp_orig_top_n_dict) < top_n:
        temp_orig_top_n_dict[key] = orig_dict[key]

    else:
        for orig_top_n_key in temp_orig_top_n_dict:
            if len(temp_orig_top_n_dict[orig_top_n_key]['matched']) < len(orig_dict[key]['matched']):
                orig_top_n_dict.pop(orig_top_n_key)
                orig_top_n_dict[key] = orig_dict[key]

        return orig_top_n_dict

    return temp_orig_top_n_dict
