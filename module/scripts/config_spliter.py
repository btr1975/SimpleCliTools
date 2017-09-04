#!/usr/bin/env python3
import logging
import re
import os
import persistentdatatools as pdt
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


class ConfigSplitter:
    """
    Method to split a Cisco config
    """
    def __init__(self, file_name, input_dir, output_dir, output_text_files=False):
        LOGGER.debug('Initializing class {class_obj}'.format(class_obj=type(self)))
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.orig_config = pdt.file_to_list(file_name, self.input_dir)
        self.output_text_files = output_text_files
        self.hostname = None
        self.standard_acls = dict()
        self.extended_acls = dict()
        self.nxos_acls = dict()
        self.iosxr_acls = dict()
        self.prefix_lists = dict()
        self.route_maps = dict()
        self.standard_community_lists = dict()
        self.interfaces = list()
        self.__get_hostname()
        self.__split_config()

    def __get_hostname(self):
        LOGGER.debug('Starting method __get_hostname in class {class_obj}'.format(class_obj=type(self)))
        hostname_regex = re.compile(r'^hostname', re.IGNORECASE)
        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if hostname_regex.match(match_line):
                hostname_split = match_line.split()
                self.hostname = hostname_split[1]

    def __split_standard_acls(self):
        LOGGER.debug('Starting method __split_standard_acls in class {class_obj}'.format(class_obj=type(self)))
        standard_acl_regex = re.compile(r'^ip access-list standard', re.IGNORECASE)
        permit_regex = re.compile(r'^permit')
        deny_regex = re.compile(r'^deny')
        bang_regex = re.compile(r'^!$')
        acl_name = None
        acl_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if standard_acl_regex.match(match_line):
                acl_line_split = match_line.split()
                acl_name = acl_line_split[3]
                if acl_found:
                    if not self.standard_acls.get(acl_name):
                        self.standard_acls.update({acl_name: list()})
                    self.standard_acls[acl_name].append(line)
                else:
                    self.standard_acls.update({acl_name: list()})
                    acl_found = True
                    self.standard_acls[acl_name].append(line)

            elif bang_regex.match(match_line):
                acl_found = False

            elif permit_regex.match(match_line) and acl_found:
                self.standard_acls[acl_name].append(line)

            elif deny_regex.match(match_line) and acl_found:
                self.standard_acls[acl_name].append(line)

    def __split_extended_acls(self):
        LOGGER.debug('Starting method __split_extended_acls in class {class_obj}'.format(class_obj=type(self)))
        extended_acl_regex = re.compile(r'^ip access-list extended', re.IGNORECASE)
        permit_regex = re.compile(r'^permit')
        deny_regex = re.compile(r'^deny')
        bang_regex = re.compile(r'^!$')
        acl_name = None
        acl_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if extended_acl_regex.match(match_line):
                acl_line_split = match_line.split()
                acl_name = acl_line_split[3]
                if acl_found:
                    if not self.extended_acls.get(acl_name):
                        self.extended_acls.update({acl_name: list()})
                    self.extended_acls[acl_name].append(line)
                else:
                    acl_found = True
                    self.extended_acls.update({acl_name: list()})
                    self.extended_acls[acl_name].append(line)

            elif bang_regex.match(match_line):
                acl_found = False

            elif permit_regex.match(match_line) and acl_found:
                self.extended_acls[acl_name].append(line)

            elif deny_regex.match(match_line) and acl_found:
                self.extended_acls[acl_name].append(line)

    def __split_nxos_acls(self):
        LOGGER.debug('Starting method __split_nxos_acls in class {class_obj}'.format(class_obj=type(self)))
        acl_regex = re.compile(r'^ip access-list', re.IGNORECASE)
        permit_regex = re.compile(r'^[0-9]+ permit')
        deny_regex = re.compile(r'^[0-9]+ deny')
        bang_regex = re.compile(r'^!$')
        acl_name = None
        acl_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if acl_regex.match(match_line):
                acl_line_split = match_line.split()
                acl_name = acl_line_split[2]
                if acl_found:
                    if not self.nxos_acls.get(acl_name):
                        self.nxos_acls.update({acl_name: list()})
                    self.nxos_acls[acl_name].append(line)
                else:
                    acl_found = True
                    self.nxos_acls.update({acl_name: list()})
                    self.nxos_acls[acl_name].append(line)

            elif bang_regex.match(match_line):
                acl_found = False

            elif permit_regex.match(match_line) and acl_found:
                self.nxos_acls[acl_name].append(line)

            elif deny_regex.match(match_line) and acl_found:
                self.nxos_acls[acl_name].append(line)

    def __split_iosxr_acls(self):
        LOGGER.debug('Starting method __split_iosxr_acls in class {class_obj}'.format(class_obj=type(self)))
        acl_regex = re.compile(r'^ipv4 access-list', re.IGNORECASE)
        permit_regex = re.compile(r'^[0-9]+ permit')
        deny_regex = re.compile(r'^[0-9]+ deny')
        remark_regex = re.compile(r'^[0-9]+ remark')
        bang_regex = re.compile(r'^!$')
        acl_name = None
        acl_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if acl_regex.match(match_line):
                acl_line_split = match_line.split()
                acl_name = acl_line_split[2]
                if acl_found:
                    if not self.iosxr_acls.get(acl_name):
                        self.iosxr_acls.update({acl_name: list()})
                    self.iosxr_acls[acl_name].append(line)
                else:
                    acl_found = True
                    self.iosxr_acls.update({acl_name: list()})
                    self.iosxr_acls[acl_name].append(line)

            elif bang_regex.match(match_line):
                acl_found = False

            elif permit_regex.match(match_line) and acl_found:
                self.iosxr_acls[acl_name].append(line)

            elif deny_regex.match(match_line) and acl_found:
                self.iosxr_acls[acl_name].append(line)

            elif remark_regex.match(match_line) and acl_found:
                self.iosxr_acls[acl_name].append(line)

    def __split_interfaces(self):
        LOGGER.debug('Starting method __split_interfaces in class {class_obj}'.format(class_obj=type(self)))
        interface_regex = re.compile(r'^interface', re.IGNORECASE)
        bang_regex = re.compile(r'^!', re.IGNORECASE)
        interface_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if interface_regex.match(match_line):
                interface_found = True
                self.interfaces.append('!')
                self.interfaces.append(line)

            elif bang_regex.match(match_line):
                interface_found = False

            elif interface_found:
                self.interfaces.append(line)

    def __split_prefix_lists(self):
        LOGGER.debug('Starting method __split_prefix_lists in class {class_obj}'.format(class_obj=type(self)))
        prefix_list_regex = re.compile(r'^ip prefix-list', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        prefix_list_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if prefix_list_regex.match(match_line):
                prefix_list_line_split = match_line.split()
                prefix_list_name = prefix_list_line_split[2]
                if prefix_list_found:
                    if not self.prefix_lists.get(prefix_list_name):
                        self.prefix_lists.update({prefix_list_name: list()})
                    self.prefix_lists[prefix_list_name].append(line)
                else:
                    prefix_list_found = True
                    self.prefix_lists.update({prefix_list_name: list()})
                    self.prefix_lists[prefix_list_name].append(line)

            elif bang_regex.match(match_line):
                prefix_list_found = False

    def __split_prefix_sets(self):
        LOGGER.debug('Starting method __split_prefix_sets in class {class_obj}'.format(class_obj=type(self)))
        prefix_set_begin_regex = re.compile(r'^prefix-set', re.IGNORECASE)
        prefix_set_end_regex = re.compile(r'^end-set', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        prefix_set_found = False
        prefix_list_name = None

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if prefix_set_begin_regex.match(match_line):
                prefix_list_line_split = match_line.split()
                prefix_list_name = prefix_list_line_split[1]
                if prefix_set_found:
                    if not self.prefix_lists.get(prefix_list_name):
                        self.prefix_lists.update({prefix_list_name: list()})
                    self.prefix_lists[prefix_list_name].append(line)
                else:
                    prefix_set_found = True
                    self.prefix_lists.update({prefix_list_name: list()})
                    self.prefix_lists[prefix_list_name].append(line)

            elif bang_regex.match(match_line):
                prefix_set_found = False

            elif prefix_set_end_regex.match(match_line) and prefix_set_found:
                self.prefix_lists[prefix_list_name].append(line)
                prefix_set_found = False

            elif prefix_set_found:
                self.prefix_lists[prefix_list_name].append(line)

    def __split_route_maps(self):
        LOGGER.debug('Starting method __split_route_maps in class {class_obj}'.format(class_obj=type(self)))
        route_map_regex = re.compile(r'^route-map ([A-Z]|_|[0-9]|-)+ (permit|deny)', re.IGNORECASE)
        description_regex = re.compile(r'^description', re.IGNORECASE)
        match_regex = re.compile(r'^match', re.IGNORECASE)
        set_regex = re.compile(r'^set', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        route_map_name = None
        route_map_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if route_map_regex.match(match_line):
                route_map_line_split = match_line.split()
                route_map_name = route_map_line_split[1]
                if route_map_found:
                    if not self.route_maps.get(route_map_name):
                        self.route_maps.update({route_map_name: list()})
                    self.route_maps[route_map_name].append(line)
                else:
                    route_map_found = True
                    if not self.route_maps.get(route_map_name):
                        self.route_maps.update({route_map_name: list()})
                    self.route_maps[route_map_name].append(line)

            elif bang_regex.match(match_line):
                route_map_found = False

            elif description_regex.match(match_line) and route_map_found:
                self.route_maps[route_map_name].append(line)

            elif match_regex.match(match_line) and route_map_found:
                self.route_maps[route_map_name].append(line)

            elif set_regex.match(match_line) and route_map_found:
                self.route_maps[route_map_name].append(line)

    def __split_route_policies(self):
        LOGGER.debug('Starting method __split_route_policies in class {class_obj}'.format(class_obj=type(self)))
        route_policy_begin_regex = re.compile(r'^route-policy', re.IGNORECASE)
        route_policy_end_regex = re.compile(r'^end-policy', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        route_policy_found = False
        route_policy_name = None

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if route_policy_begin_regex.match(match_line):
                route_policy_line_split = match_line.split()
                route_policy_name = route_policy_line_split[1]
                if route_policy_found:
                    if not self.route_maps.get(route_policy_name):
                        self.route_maps.update({route_policy_name: list()})
                    self.route_maps[route_policy_name].append(line)
                else:
                    route_policy_found = True
                    self.route_maps.update({route_policy_name: list()})
                    self.route_maps[route_policy_name].append(line)

            elif bang_regex.match(match_line):
                route_policy_found = False

            elif route_policy_end_regex.match(match_line) and route_policy_found:
                self.route_maps[route_policy_name].append(line)
                route_policy_found = False

            elif route_policy_found:
                self.route_maps[route_policy_name].append(line)

    def __split_standard_community_lists(self):
        LOGGER.debug('Starting method __split_standard_community_lists in class '
                     '{class_obj}'.format(class_obj=type(self)))
        standard_community_list_regex = re.compile(r'^ip community-list standard', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        community_list_found = False

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if standard_community_list_regex.match(match_line):
                community_list_line_split = match_line.split()
                community_name = community_list_line_split[3]
                if community_list_found:
                    if not self.standard_community_lists.get(community_name):
                        self.standard_community_lists.update({community_name: list()})
                    self.standard_community_lists[community_name].append(line)
                else:
                    community_list_found = True
                    self.standard_community_lists.update({community_name: list()})
                    self.standard_community_lists[community_name].append(line)

            elif bang_regex.match(match_line):
                community_list_found = False

    def __split_community_sets(self):
        LOGGER.debug('Starting method __split_community_sets in class {class_obj}'.format(class_obj=type(self)))
        community_set_begin_regex = re.compile(r'^community-set', re.IGNORECASE)
        community_set_end_regex = re.compile(r'^end-set', re.IGNORECASE)
        bang_regex = re.compile(r'^!$')
        community_set_found = False
        community_set_name = None

        for line in self.orig_config:
            match_line = pdt.remove_extra_spaces(line)
            if community_set_begin_regex.match(match_line):
                community_set_line_split = match_line.split()
                community_set_name = community_set_line_split[1]
                if community_set_found:
                    if not self.standard_community_lists.get(community_set_name):
                        self.standard_community_lists.update({community_set_name: list()})
                    self.standard_community_lists[community_set_name].append(line)
                else:
                    community_set_found = True
                    self.standard_community_lists.update({community_set_name: list()})
                    self.standard_community_lists[community_set_name].append(line)

            elif bang_regex.match(match_line):
                community_set_found = False

            elif community_set_end_regex.match(match_line) and community_set_found:
                self.standard_community_lists[community_set_name].append(line)
                community_set_found = False

            elif community_set_found:
                self.standard_community_lists[community_set_name].append(line)

    def __output_text_files(self):
        LOGGER.debug('Starting method __output_text_files in class {class_obj}'.format(class_obj=type(self)))
        self.__split_standard_acls()
        for key in self.standard_acls:
            pdt.list_to_file(self.standard_acls[key], 'STANDARD-ACL-{name}.txt'.format(name=key),
                             os.path.join(self.output_dir, self.hostname))

        self.__split_extended_acls()
        for key in self.extended_acls:
            pdt.list_to_file(self.extended_acls[key], 'EXTENDED-ACL-{name}.txt'.format(name=key),
                             os.path.join(self.output_dir, self.hostname))

        if not self.standard_acls and not self.extended_acls:
            self.__split_nxos_acls()
            for key in self.nxos_acls:
                pdt.list_to_file(self.nxos_acls[key], 'ACL-{name}.txt'.format(name=key),
                                 os.path.join(self.output_dir, self.hostname))

            if not self.nxos_acls:
                self.__split_iosxr_acls()
                for key in self.iosxr_acls:
                    pdt.list_to_file(self.iosxr_acls[key], 'ACL-{name}.txt'.format(name=key),
                                     os.path.join(self.output_dir, self.hostname))

        self.__split_interfaces()
        if self.interfaces:
            pdt.list_to_file(self.interfaces, 'INTERFACES.txt', os.path.join(self.output_dir, self.hostname))

        self.__split_prefix_lists()
        for key in self.prefix_lists:
            pdt.list_to_file(self.prefix_lists[key], 'PREFIX-LIST-{name}.txt'.format(name=key),
                             os.path.join(self.output_dir, self.hostname))

        if not self.prefix_lists:
            self.__split_prefix_sets()
            for key in self.prefix_lists:
                pdt.list_to_file(self.prefix_lists[key], 'PREFIX-SET-{name}.txt'.format(name=key),
                                 os.path.join(self.output_dir, self.hostname))

        self.__split_route_maps()
        for key in self.route_maps:
            pdt.list_to_file(self.route_maps[key], 'ROUTE-MAP-{name}.txt'.format(name=key),
                             os.path.join(self.output_dir, self.hostname))

        if not self.route_maps:
            self.__split_route_policies()
            for key in self.route_maps:
                pdt.list_to_file(self.route_maps[key], 'ROUTE-POLICY-{name}.txt'.format(name=key),
                                 os.path.join(self.output_dir, self.hostname))

        self.__split_standard_community_lists()
        for key in self.standard_community_lists:
            pdt.list_to_file(self.standard_community_lists[key], 'STANDARD-CL-{name}.txt'.format(name=key),
                             os.path.join(self.output_dir, self.hostname))

        if not self.standard_community_lists:
            self.__split_community_sets()
            for key in self.standard_community_lists:
                pdt.list_to_file(self.standard_community_lists[key], 'CS-{name}.txt'.format(name=key),
                                 os.path.join(self.output_dir, self.hostname))

    def __output_spreadsheet(self, host_name):
        LOGGER.debug('Starting method __output_spreadsheet in class {class_obj}'.format(class_obj=type(self)))
        temp_list = list()
        tabs_dict = dict()

        self.__split_standard_acls()
        if self.standard_acls:
            for key in self.standard_acls:
                temp_list.append('!')
                for line in self.standard_acls[key]:
                    temp_list.append(line)

            tabs_dict.update({'STANDARD_ACLS': temp_list.copy()})
            temp_list.clear()

        self.__split_extended_acls()
        if self.extended_acls:
            for key in self.extended_acls:
                temp_list.append('!')
                for line in self.extended_acls[key]:
                    temp_list.append(line)

            tabs_dict.update({'EXTENDED_ACLS': temp_list.copy()})
            temp_list.clear()

        if not self.standard_acls and not self.extended_acls:
            self.__split_nxos_acls()
            if self.nxos_acls:
                for key in self.nxos_acls:
                    temp_list.append('!')
                    for line in self.nxos_acls[key]:
                        temp_list.append(line)

                tabs_dict.update({'NXOS_ACLS': temp_list.copy()})
                temp_list.clear()

            if not self.nxos_acls:
                self.__split_iosxr_acls()
                if self.iosxr_acls:
                    for key in self.iosxr_acls:
                        temp_list.append('!')
                        for line in self.iosxr_acls[key]:
                            temp_list.append(line)

                    tabs_dict.update({'IOSXR_ACLS': temp_list.copy()})
                    temp_list.clear()

        self.__split_interfaces()
        if self.interfaces:
            tabs_dict.update({'INTERFACES': self.interfaces})

        self.__split_prefix_lists()
        if self.prefix_lists:
            for key in self.prefix_lists:
                temp_list.append('!')
                for line in self.prefix_lists[key]:
                    temp_list.append(line)

            tabs_dict.update({'PREFIX_LISTS': temp_list.copy()})
            temp_list.clear()

        if not self.prefix_lists:
            self.__split_prefix_sets()
            if self.prefix_lists:
                for key in self.prefix_lists:
                    temp_list.append('!')
                    for line in self.prefix_lists[key]:
                        temp_list.append(line)

                tabs_dict.update({'PREFIX_SETS': temp_list.copy()})
                temp_list.clear()

        self.__split_route_maps()
        if self.route_maps:
            for key in self.route_maps:
                temp_list.append('!')
                for line in self.route_maps[key]:
                    temp_list.append(line)

            tabs_dict.update({'ROUTE_MAPS': temp_list.copy()})
            temp_list.clear()

        if not self.route_maps:
            self.__split_route_policies()
            if self.route_maps:
                for key in self.route_maps:
                    temp_list.append('!')
                    for line in self.route_maps[key]:
                        temp_list.append(line)

                tabs_dict.update({'ROUTE_POLICIES': temp_list.copy()})
                temp_list.clear()

        self.__split_standard_community_lists()
        if self.standard_community_lists:
            for key in self.standard_community_lists:
                temp_list.append('!')
                for line in self.standard_community_lists[key]:
                    temp_list.append(line)

            tabs_dict.update({'STANDARD_COMMUNITY_LISTS': temp_list.copy()})
            temp_list.clear()

        if not self.standard_community_lists:
            self.__split_community_sets()
            if self.standard_community_lists:
                for key in self.standard_community_lists:
                    temp_list.append('!')
                    for line in self.standard_community_lists[key]:
                        temp_list.append(line)

                tabs_dict.update({'COMMUNITY_SETS': temp_list.copy()})
                temp_list.clear()

        spreadsheet_obj = mod.scripts.WriteXlsxTabs(os.path.join(self.output_dir, host_name,
                                                                 '{host_name}.xlsx'.format(host_name=host_name)),
                                                    **tabs_dict)
        spreadsheet_obj.write_spreadsheet()

    def __split_config(self):
        LOGGER.debug('Starting method __split_config in class {class_obj}'.format(class_obj=type(self)))
        if self.hostname:
            pdt.verify_directory(self.hostname, self.output_dir, directory_create=True)
        else:
            self.hostname = 'NONE'
            pdt.verify_directory('NONE', self.output_dir, directory_create=True)

        if self.output_text_files:
            self.__output_text_files()

        else:
            self.__output_spreadsheet(self.hostname)
