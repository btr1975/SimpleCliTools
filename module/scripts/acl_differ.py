import logging
import persistentdatatools as pdt
import ipaddresstools as ipv4
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 1, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class AccessListInformation:
    """
    Class to pull a part and Standard ACL for diffing, and converting to a Prefix-List
    """

    def __init__(self, access_list_original):
        LOGGER.debug('Initializing Class {class_type}'.format(class_type=type(self)))
        if isinstance(access_list_original, list):
            self.access_list_original = access_list_original
        else:
            LOGGER.critical('Expected a list but received a {item_type}'.format(item_type=type(access_list_original)))
            raise TypeError('Expected a list but received a {item_type}'.format(item_type=type(access_list_original)))

        self.access_list_permit_deny_dict = {'permit': list(),
                                             'deny': list()}
        self.access_list_permit_statement_matcher = list()
        self.access_list_deny_statement_matcher = list()
        self.access_list_parts_list = list()
        self.comparison = None
        self.acl_name = None
        self._compile_access_list()

    def _create_acl_permit_deny_dict(self):
        """
        Method to create a permit or deny dictionary

        :return:
            None

        """
        LOGGER.debug('Starting Method _create_acl_permit_deny_dict in Class '
                     '{class_type}'.format(class_type=type(self)))

        for index, line in enumerate(self.access_list_original):
            line = ' '.join(line.split())
            line_split = line.split()
            self.access_list_parts_list.append(line_split)
            if len(line_split) == 2:
                if line_split[0] == 'permit':
                    self.access_list_permit_deny_dict['permit'].append((index, line_split[1]))

                elif line_split[0] == 'deny':
                    self.access_list_permit_deny_dict['deny'].append((index, line_split[1]))

            elif len(line_split) == 3:
                if line_split[0] == 'permit':
                    self.access_list_permit_deny_dict['permit'].append((index, ' '.join(line_split[1:])))

                elif line_split[0] == 'deny':
                    self.access_list_permit_deny_dict['deny'].append((index, ' '.join(line_split[1:])))

            else:
                LOGGER.warning('Line {index}, did not match a need length {line}'.format(index=index, line=line_split))
                self.acl_name = line_split[3]

    def _create_match_lists(self):
        """
        Method to create a list from the tuples in orig_list

        :return:
            None

        """
        LOGGER.debug('Starting Method _create_match_lists in Class {class_type}'.format(class_type=type(self)))

        for orig_tuple in self.access_list_permit_deny_dict['permit']:
            self.access_list_permit_statement_matcher.append(orig_tuple[1])

        for orig_tuple in self.access_list_permit_deny_dict['deny']:
            self.access_list_deny_statement_matcher.append(orig_tuple[1])

    def _compile_access_list(self):
        """
        Method to compile the prefix-list data

        :return:
            None

        """
        LOGGER.debug('Starting Method _compile_access_list in Class {class_type}'.format(class_type=type(self)))
        self._create_acl_permit_deny_dict()
        self._create_match_lists()

    def compare_access_list(self, acl_object, input_file_name):
        """
        Method to compare another ACL-list object
        :param acl_object: The comparison object
        :param input_file_name: The source file name
        :return:
            A list of differences

        """
        LOGGER.debug('Starting Method compare_access_list in Class {class_type}'.format(class_type=type(self)))
        if not isinstance(acl_object, AccessListInformation):
            LOGGER.critical('Method compare_access_list in Class {class_type}, expected a <AccessListInformation> '
                            'object but received a {item_type}'.format(class_type=self, item_type=acl_object))
            raise TypeError('expected a <AccessListInformation> object but received a '
                            '{item_type}'.format(item_type=acl_object))

        if not self.comparison:
            self.comparison = list()

        else:
            LOGGER.critical('Tried to run a comparison, when one has already been run!')
            raise FileExistsError('A comparison is already being stored')

        comparison_permit_list = acl_object.get_access_list_permit_statement_matcher()
        comparison_deny_list = acl_object.get_access_list_deny_statement_matcher()

        for key in self.access_list_permit_deny_dict:
            for line in self.access_list_permit_deny_dict[key]:
                if key == 'permit':
                    if line[1] not in comparison_permit_list:
                        self.comparison.append(
                            '{permit_deny} {ip_addr} not in ACL {acl_name} in file '
                            '{input_file_name}'.format(permit_deny=key,
                                                       ip_addr=line[1],
                                                       acl_name=self.acl_name,
                                                       input_file_name=input_file_name))
                        self.comparison.append(self.access_list_original[line[0]])

                elif key == 'deny':
                    if line[1] not in comparison_deny_list:
                        self.comparison.append(
                            '{permit_deny} {ip_addr} not in ACL {acl_name} in file '
                            '{input_file_name}'.format(permit_deny=key,
                                                       ip_addr=line[1],
                                                       acl_name=self.acl_name,
                                                       input_file_name=input_file_name))
                        self.comparison.append(self.access_list_original[line[0]])

        return self.comparison

    def convert_to_prefix_list(self, new_prefix_list_name=None):
        """
        Method to convert a standard ACL to a Prefix-List for filtering
        Args:
            new_prefix_list_name: If you want to change the name of the Prefix-List

        Returns:
            A List of the Prefix-List

        """
        LOGGER.debug('Starting Method convert_to_prefix_list in Class '
                     '{class_type}'.format(class_type=type(self)))

        pl_temp = list()
        if not new_prefix_list_name:
            new_prefix_list_name = self.acl_name

        for line in self.access_list_original:
            line = ' '.join(line.split())
            line_split = line.split()
            if len(line_split) == 2:
                ip = line_split[1]
                split_ip = ip.split('.')
                if split_ip[0] == '0':
                    cidr = '0'
                    pl_temp.append(
                        'ip prefix-list {pl_name} {p_or_d} {ip_addr}/{cidr}'.format(p_or_d=line_split[0],
                                                                                    pl_name=new_prefix_list_name,
                                                                                    ip_addr=ip, cidr=cidr))

                elif split_ip[1] == '0':
                    cidr = '8'
                    pl_temp.append(
                        'ip prefix-list {pl_name} {p_or_d} {ip_addr}/{cidr}'.format(p_or_d=line_split[0],
                                                                                    pl_name=new_prefix_list_name,
                                                                                    ip_addr=ip, cidr=cidr))

                elif split_ip[2] == '0':
                    cidr = '16'
                    pl_temp.append(
                        'ip prefix-list {pl_name} {p_or_d} {ip_addr}/{cidr}'.format(p_or_d=line_split[0],
                                                                                    pl_name=new_prefix_list_name,
                                                                                    ip_addr=ip, cidr=cidr))

                elif split_ip[3] == '0':
                    cidr = '24'
                    pl_temp.append(
                        'ip prefix-list {pl_name} {p_or_d} {ip_addr}/{cidr}'.format(p_or_d=line_split[0],
                                                                                    pl_name=new_prefix_list_name,
                                                                                    ip_addr=ip, cidr=cidr))

                else:
                    cidr = '32'
                    pl_temp.append('ip prefix-list {pl_name} {p_or_d} {ip_addr}/'
                                   '{cidr}'.format(p_or_d=line_split[0], pl_name=new_prefix_list_name,
                                                   ip_addr=ip, cidr=cidr))

            elif len(line_split) == 3:
                ip, invmask = line_split[1:]
                for mask in ipv4.mask_conversion:
                    if invmask == ipv4.mask_conversion[mask]['INVMASK']:
                        pl_temp.append('ip prefix-list {pl_name} {p_or_d} {ip_addr}/'
                                       '{cidr} le 32'.format(p_or_d=line_split[0], pl_name=new_prefix_list_name,
                                                             ip_addr=ip, cidr=ipv4.mask_conversion[mask]['CIDR']))

        return pl_temp

    def get_access_list_permit_deny_dict(self):
        """
        Method access_list_permit_deny_dict getter
        :return:
            A dictionary

        """
        return self.access_list_permit_deny_dict

    def get_access_list_original(self):
        """
        Method access_list_original getter
        :return:
            A List

        """
        return self.access_list_original

    def get_access_list_permit_statement_matcher(self):
        """
        Method access_list_permit_statement_matcher getter
        :return:
            A List

        """
        return self.access_list_permit_statement_matcher

    def get_access_list_deny_statement_matcher(self):
        """
        Method access_list_deny_statement_matcher getter
        :return:
            A List

        """
        return self.access_list_deny_statement_matcher

    def get_access_list_parts_list(self):
        """
        Method access_list_parts_list getter
        :return:
            A List

        """
        return self.access_list_parts_list


def acl_diff(file_a, file_b, output_file, input_dir, output_dir):
    """
    The ACL Diffing Function
    :param file_a: The name of file a
    :param file_b: The name of file b
    :param output_file: The name of the output file
    :param input_dir: The name of the input directory
    :param output_dir: The name of the output directory
    :return:
        None

    """
    LOGGER.debug('Starting Function acl_diff')

    a_list = pdt.file_to_list(file_a, input_dir)
    b_list = pdt.file_to_list(file_b, input_dir)

    acl_obj_a = AccessListInformation(a_list)
    acl_obj_b = AccessListInformation(b_list)

    output_list = acl_obj_a.compare_access_list(acl_obj_b, file_b)
    output_list += acl_obj_b.compare_access_list(acl_obj_a, file_a)

    output_file = pdt.file_name_increase(output_file, output_dir)
    print('File named {file_name} created in {folder}'.format(file_name=pdt.list_to_file(output_list,
                                                                                         output_file,
                                                                                         output_dir),
                                                              folder=output_dir))


def acl_to_prefix_list_converter(file_a, output_file, input_dir, output_dir):
    """
    The ACL Diffing Function
    :param file_a: The name of file a
    :param output_file: The name of the output file
    :param input_dir: The name of the input directory
    :param output_dir: The name of the output directory
    :return:
        None

    """
    LOGGER.debug('Starting Function acl_to_prefix_list_converter')

    a_list = pdt.file_to_list(file_a, input_dir)

    acl_obj_a = AccessListInformation(a_list)

    output_list = acl_obj_a.convert_to_prefix_list()

    output_file = pdt.file_name_increase(output_file, output_dir)
    print('File named {file_name} created in {folder}'.format(file_name=pdt.list_to_file(output_list,
                                                                                         output_file,
                                                                                         output_dir),
                                                              folder=output_dir))
