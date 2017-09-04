import logging
import persistentdatatools as pdt
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


class PrefixListInformation:
    """
    Class to pull apart, and compare a Prefix-List
    """

    def __init__(self, prefix_list_original):
        LOGGER.debug('Initializing Class {class_type}'.format(class_type=type(self)))
        if isinstance(prefix_list_original, list):
            self.prefix_list_original = prefix_list_original
        else:
            LOGGER.critical('Expected a list but received a {item_type}'.format(item_type=type(prefix_list_original)))
            raise TypeError('Expected a list but received a {item_type}'.format(item_type=type(prefix_list_original)))

        self.prefix_list_permit_deny_dict = {'permit': list(),
                                             'deny': list()}
        self.prefix_list_permit_statement_matcher = list()
        self.prefix_list_deny_statement_matcher = list()
        self.prefix_list_parts_list = list()
        self.comparison = None
        self._compile_prefix_list()

    def _create_prefix_list_permit_deny_dict(self):
        """
        Method to create a permit or deny dictionary

        :return:
            None

        """
        LOGGER.debug('Starting Method _create_prefix_list_permit_deny_dict in Class '
                     '{class_type}'.format(class_type=type(self)))

        for index, line in enumerate(self.prefix_list_original):
            line_split = line.split()
            self.prefix_list_parts_list.append(line_split)
            if len(line_split) == 9:
                if line_split[5] == 'permit':
                    self.prefix_list_permit_deny_dict['permit'].append((index, ' '.join(line_split[6:9])))

                elif line_split[5] == 'deny':
                    self.prefix_list_permit_deny_dict['deny'].append((index, ' '.join(line_split[6:9])))

            elif len(line_split) == 7:
                if line_split[5] == 'permit':
                    self.prefix_list_permit_deny_dict['permit'].append((index, line_split[6]))

                elif line_split[5] == 'deny':
                    self.prefix_list_permit_deny_dict['deny'].append((index, line_split[6]))

            else:
                LOGGER.warning('Line {index}, did not match a need length {line}'.format(index=index, line=line_split))

    def _create_match_lists(self):
        """
        Method to create a list from the tuples in orig_list

        :return:
            None

        """
        LOGGER.debug('Starting Method _create_match_lists in Class {class_type}'.format(class_type=type(self)))

        for orig_tuple in self.prefix_list_permit_deny_dict['permit']:
            self.prefix_list_permit_statement_matcher.append(orig_tuple[1])

        for orig_tuple in self.prefix_list_permit_deny_dict['deny']:
            self.prefix_list_deny_statement_matcher.append(orig_tuple[1])

    def _compile_prefix_list(self):
        """
        Method to compile the prefix-list data

        :return:
            None

        """
        LOGGER.debug('Starting Method _compile_prefix_list in Class {class_type}'.format(class_type=type(self)))
        self._create_prefix_list_permit_deny_dict()
        self._create_match_lists()

    def compare_prefix_list(self, pl_object, input_file_name):
        """
        Method to compare another prefix-list object
        :param pl_object: The comparison object
        :param input_file_name: The source file name
        :return:
            A list of differences

        """
        LOGGER.debug('Starting Method compare_prefix_list in Class {class_type}'.format(class_type=type(self)))
        if not isinstance(pl_object, PrefixListInformation):
            LOGGER.critical('Method compare_prefix_list in Class {class_type}, expected a <PrefixListInformation> '
                            'object but received a {item_type}'.format(class_type=self, item_type=pl_object))
            raise TypeError('expected a <PrefixListInformation> object but received a '
                            '{item_type}'.format(item_type=pl_object))

        if not self.comparison:
            self.comparison = list()

        else:
            LOGGER.critical('Tried to run a comparison, when one has already been run!')
            raise FileExistsError('A comparison is already being stored')

        comparison_permit_list = pl_object.get_prefix_list_permit_statement_matcher()
        comparison_deny_list = pl_object.get_prefix_list_deny_statement_matcher()

        for key in self.prefix_list_permit_deny_dict:
            for line in self.prefix_list_permit_deny_dict[key]:
                if key == 'permit':
                    if line[1] not in comparison_permit_list:
                        self.comparison.append(
                            '{permit_deny} {ip_addr} not in prefix-list {pl_name} in file '
                            '{input_file_name}'.format(permit_deny=key,
                                                       ip_addr=line[1],
                                                       pl_name=self.prefix_list_parts_list[line[0]][2],
                                                       input_file_name=input_file_name))
                        self.comparison.append(self.prefix_list_original[line[0]])

                elif key == 'deny':
                    if line[1] not in comparison_deny_list:
                        self.comparison.append(
                            '{permit_deny} {ip_addr} not in prefix-list {pl_name} in file '
                            '{input_file_name}'.format(permit_deny=key,
                                                       ip_addr=line[1],
                                                       pl_name=self.prefix_list_parts_list[line[0]][2],
                                                       input_file_name=input_file_name))
                        self.comparison.append(self.prefix_list_original[line[0]])

        return self.comparison

    def get_prefix_list_permit_deny_dict(self):
        """
        Method prefix_list_permit_deny_dict getter
        :return:
            A dictionary

        """
        return self.prefix_list_permit_deny_dict

    def get_prefix_list_original(self):
        """
        Method get_prefix_list_original getter
        :return:
            A List

        """
        return self.prefix_list_original

    def get_prefix_list_permit_statement_matcher(self):
        """
        Method get_prefix_list_permit_statement_matcher getter
        :return:
            A List

        """
        return self.prefix_list_permit_statement_matcher

    def get_prefix_list_deny_statement_matcher(self):
        """
        Method get_prefix_list_deny_statement_matcher getter
        :return:
            A List

        """
        return self.prefix_list_deny_statement_matcher

    def get_prefix_list_parts_list(self):
        """
        Method get_prefix_list_parts_list getter
        :return:
            A List

        """
        return self.prefix_list_parts_list


def prefix_list_diff(file_a, file_b, output_file, input_dir, output_dir):
    """
    The main running function
    :param file_a: The name of file a
    :param file_b: The name of file b
    :param output_file: The name of the output file
    :param input_dir: The name of the input directory
    :param output_dir: The name of the output directory
    :return:
        None

    """
    LOGGER.debug('Starting Function main')

    a_list = pdt.file_to_list(file_a, input_dir)
    b_list = pdt.file_to_list(file_b, input_dir)

    pl_obj_a = PrefixListInformation(a_list)
    pl_obj_b = PrefixListInformation(b_list)

    output_list = pl_obj_a.compare_prefix_list(pl_obj_b, file_b)

    output_list += pl_obj_b.compare_prefix_list(pl_obj_a, file_a)

    output_file = pdt.file_name_increase(output_file, output_dir)
    print('File named {file_name} created in {folder}'.format(file_name=pdt.list_to_file(output_list,
                                                                                         output_file,
                                                                                         output_dir),
                                                              folder=output_dir))
