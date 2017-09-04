#!/usr/bin/env python3
import logging
import os
import persistentdatatools as pdt
import ipaddresstools as ipv4
import module as mod
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = ''
__license__ = ''
__status__ = 'dev'
__version_info__ = (1, 0, 1, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)

mask_conversion = ipv4.mask_conversion


class MultiCast(object):
    """
    Base Multicast Class
    """
    device_type_dict = {
        1: 'IOS',
        2: 'NX-OS',
        3: 'IOS-XR',
    }

    def __init__(self, device_type, rp_ip_addr, acl_or_rmap_name, description=None):
        try:
            self.device_type_dict[device_type]
        except:
            LOGGER.critical('Invalid device type chosen %s in %s', device_type, type(self))
            raise mod.util.BadDeviceType('You have chosen an invalid device type, the valid types are '
                                         '{types}'.format(types=self.device_type_dict))
        self.device_type = device_type
        self.__check_unicast_address(rp_ip_addr)
        self.rp_ip_addr = rp_ip_addr
        acl_or_rmap_name = pdt.remove_spaces_add_hyphen(acl_or_rmap_name)
        self.acl_or_rmap_name = acl_or_rmap_name
        if description:
            description = pdt.remove_extra_spaces(description)
        self.description = description
        self.networks = list()

    def __str__(self):
        return '<MultiCast Object>'

    def add_network(self, mcast_ip_addr):
        """
        Method to add a network to a multicast config
        Args:
            mcast_ip_addr: Multicast ip and mask

        Returns:

        """
        LOGGER.debug('Method add_network in %s', type(self))
        self.__check_mcast_network(mcast_ip_addr)

        mcast_ip_addr_split = mcast_ip_addr.split('/')
        mcast_ip_addr_split[0] = ipv4.whole_subnet_maker(mcast_ip_addr_split[0], mcast_ip_addr_split[1])

        self.networks.append('%s/%s' % (mcast_ip_addr_split[0], mcast_ip_addr_split[1]))

    def __check_unicast_address(self, ip_addr):
        """
        Method to check for a valid unicast IP, and Raise an exception if it is no good
        :param
            *args: IP's to check
        :return:
            The CIDR address or an TypeError exception

        """
        LOGGER.debug('Method __check_unicast_address in %s', type(self))
        if ip_addr:
            good = ipv4.ucast_ip(ip_addr, return_tuple=False)
            if not good:
                LOGGER.critical('Invalid unicast IP address %s in %s', ip_addr, type(self))
                raise mod.util.BadUniCastIP('You have entered a invalid unicast IP address for the RP!!!')

    def __check_mcast_network(self, mcast_ip_addr):
        """
        Method to check for a valid multicast IP network, and Raise an exception if it is no good
        :param
            mcast_ip_addr: IP's to check
        :return:
            The CIDR address or an TypeError exception

        """
        LOGGER.debug('Method __check_mcast_network in %s', type(self))
        if mcast_ip_addr:
            good = ipv4.mcast_ip_mask(mcast_ip_addr, return_tuple=False)
            if not good:
                LOGGER.critical('Invalid multicast IP address and cidr %s in %s', mcast_ip_addr, type(self))
                raise mod.util.BadMultiCastIpNetwork('You have entered a invalid multicast IP network!!!')

    def modify_networks_data(self, list_of_networks=None):
        """
        Method to edit the network list
        Args:
            list_of_networks: As list of networks

        Returns:

        """
        LOGGER.debug('Method modify_networks_data in %s', type(self))
        if list_of_networks:
            if not isinstance(list_of_networks, list):
                LOGGER.critical('Expecting a list but received %s in %s', type(list_of_networks), type(self))
                raise TypeError('Was expecting a list but received {type}'.format(type=type(list_of_networks)))
            for index, network in enumerate(list_of_networks):
                self.__check_mcast_network(network)
                mcast_ip_addr_split = network.split('/')
                mcast_ip_addr_split[0] = ipv4.whole_subnet_maker(mcast_ip_addr_split[0], mcast_ip_addr_split[1])
                list_of_networks[index] = '%s/%s' % (mcast_ip_addr_split[0], mcast_ip_addr_split[1])
            self.networks = list_of_networks

    def get_networks_data(self):
        """
        Method to return the networks config data
        :return:
            Returns a list of CIDR networks

        """
        LOGGER.debug('Method get_networks_data in %s', type(self))
        return self.networks

    def modify_mcast_base_data(self, rp_ip_addr=None, acl_or_rmap_name=None, description=None):
        """
        Method to modify multicast base data
        Args:
            rp_ip_addr: The RP IP Address
            acl_or_rmap_name: The ACL or Route-Map name
            description: A descripton

        Returns:

        """
        LOGGER.debug('Method modify_mcast_base_data in %s', type(self))
        if rp_ip_addr:
            self.__check_unicast_address(rp_ip_addr)
            self.rp_ip_addr = rp_ip_addr
        elif acl_or_rmap_name:
            acl_or_rmap_name = pdt.remove_spaces_add_hyphen(acl_or_rmap_name)
            self.acl_or_rmap_name = acl_or_rmap_name
        elif description:
            description = pdt.remove_extra_spaces(description)
            self.description = description

    def get_mcast_base_data(self):
        """
        Method to return the base RP config data
        :return:
            Returns a dictionary with the following keys
                'rp_ip_addr'
                'acl_or_rmap_name'
                'description'

        """
        LOGGER.debug('Method get_mcast_base_data in %s', type(self))
        return {'rp_ip_addr': self.rp_ip_addr, 'acl_or_rmap_name': self.acl_or_rmap_name,
                'description': self.description}

    def get_mcast_config(self):
        """
        Method to get the configuration for Multi Cast
        :return:
            Returns a list containing the configuration

        """
        LOGGER.debug('Method get_mcast_config in %s', type(self))
        temp_list = list()
        sequence = 10
        if self.device_type == 1:
            temp_list.append("ip pim rp-address %s %s override" % (self.rp_ip_addr, self.acl_or_rmap_name))
            temp_list.append('!')
            temp_list.append('ip access-list standard %s' % (self.acl_or_rmap_name,))
            for network in self.networks:
                network_split = network.split('/')
                temp_list.append('%i permit %s %s' % (sequence, network_split[0],
                                                      mask_conversion[int(network_split[1])]['INVMASK']))
                sequence += 10

        elif self.device_type == 2:
            temp_list.append("ip pim rp-address %s route-map %s" % (self.rp_ip_addr, self.acl_or_rmap_name))
            temp_list.append("!")
            for network in self.networks:
                temp_list.append('route-map %s permit %i' % (self.acl_or_rmap_name, sequence))
                temp_list.append('match ip multicast group %s' % (network,))
                sequence += 10

        elif self.device_type == 3:
            temp_list.append("router pim")
            temp_list.append(" address-family ipv4")
            temp_list.append("  rp-address %s %s override" % (self.rp_ip_addr, self.acl_or_rmap_name))
            temp_list.append('!')
            temp_list.append('ipv4 access-list %s' % (self.acl_or_rmap_name,))
            for network in self.networks:
                network_split = network.split('/')
                temp_list.append('%i permit ipv4 any %s %s' % (sequence, network_split[0],
                                                               mask_conversion[int(network_split[1])]['INVMASK']))
                sequence += 10

        temp_list.append("!")
        return temp_list


class AclToRmHits:
    """
    Class to convert a Mcast ACL to A RM, for just hit lines
    """
    def __init__(self, route_map_name, rp_address, matches_only, file_name, input_dir, output_dir):
        LOGGER.debug('Initializing class {class_type}'.format(class_type=type(self)))
        self.route_map_name = route_map_name
        self.rp_address = rp_address
        self.matches_only = matches_only
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.orig_config = pdt.file_to_list(file_name, self.input_dir)
        self.new_rm_dict = dict()
        self.__convert()

    def __split_acl_matches_only(self):
        """
        Method to split the ACL and check it for matches
        :return:
            None

        """
        LOGGER.debug('Starting method __split_acl_matches_only in class {class_type}'.format(class_type=type(self)))
        new_rm_dict_key = 0
        mcast_ip = None
        mask = None

        for line in self.orig_config:
            line_match = pdt.remove_extra_spaces(line)
            line_split = ' '.join(line_match.split(','))
            line_split = line_split.split()

            if 'matches)' in line_split:
                if ipv4.mcast_ip(line_split[2], return_tuple=False):
                    mcast_ip = line_split[2]

                try:
                    for cidr in mask_conversion:
                        if line_split[5] == mask_conversion[cidr]['INVMASK']:
                            mask = str(cidr)
                            break

                except IndexError as e:
                    LOGGER.info('Method __split_acl_matches_only in class {class_type} '
                                'error {e}'.format(class_type=type(self), e=e))
                    mask = '32'

                self.new_rm_dict[new_rm_dict_key] = '{mcast_ip}/{mask}'.format(mcast_ip=mcast_ip, mask=mask)
                new_rm_dict_key += 1

    def __split_acl(self):
        """
        Method to split the ACL and check it
        :return:
            None

        """
        LOGGER.debug('Starting method __split_acl in class {class_type}'.format(class_type=type(self)))
        new_rm_dict_key = 0
        mcast_ip = None
        mask = None

        for line in self.orig_config:
            line_match = pdt.remove_extra_spaces(line)
            line_split = ' '.join(line_match.split(','))
            line_split = line_split.split()

            if ipv4.mcast_ip(line_split[2], return_tuple=False):

                if ipv4.mcast_ip(line_split[2], return_tuple=False):
                    mcast_ip = line_split[2]

                try:
                    for cidr in mask_conversion:
                        if line_split[5] == mask_conversion[cidr]['INVMASK']:
                            mask = str(cidr)
                            break

                except IndexError as e:
                    LOGGER.info('Method __split_acl_matches_only in class {class_type} '
                                'error {e}'.format(class_type=type(self), e=e))
                    mask = '32'

                self.new_rm_dict[new_rm_dict_key] = '{mcast_ip}/{mask}'.format(mcast_ip=mcast_ip, mask=mask)
                new_rm_dict_key += 1

    def __create_route_map(self):
        """
        Methos to create the route-map and put it in a spreadsheet
        :return:
            None

        """
        LOGGER.debug('Starting method __create_route_map in class {class_type}'.format(class_type=type(self)))
        route_map_obj = MultiCast(2, self.rp_address, self.route_map_name)
        for key in self.new_rm_dict:
            route_map_obj.add_network(self.new_rm_dict[key])

        spreadsheet_file_name = pdt.file_name_increase('mcast_acl_to_rmap.xlsx', self.output_dir)

        excel_obj = mod.scripts.WriteXlsxTabs(os.path.join(self.output_dir, spreadsheet_file_name),
                                              ACL=self.orig_config, ROUTE_MAP=route_map_obj.get_mcast_config())
        excel_obj.write_spreadsheet()

        print('File named {file_name} created in {folder}'.format(file_name=spreadsheet_file_name,
                                                                  folder=self.output_dir))

    def __convert(self):
        """
        Method to order operations
        :return:
            None

        """
        LOGGER.debug('Starting method __convert in class {class_type}'.format(class_type=type(self)))
        if self.matches_only:
            self.__split_acl_matches_only()
        else:
            self.__split_acl()

        self.__create_route_map()
