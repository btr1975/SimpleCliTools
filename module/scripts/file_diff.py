import logging
import module as mod
import os
import re
import persistentdatatools as pdt
import ipaddresstools as ipv4
import difflibhelper as diffhelper
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 3, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def file_diff(file_a, file_b, input_dir, output_dir, one_off_cidr_cef):
    """
    Function to do a plain file diff, and output a Excel Spreadsheet
    :param file_a: A file
    :param file_b: A File
    :param input_dir: The input directory
    :param output_dir: The output directory
    :param one_off_cidr_cef: Created cause of issue with ASR 9K OS Upgrades
    :return:
        None

    """
    LOGGER.debug('Starting Function file_diff')

    a_list = pdt.file_to_list(file_a, input_dir)
    b_list = pdt.file_to_list(file_b, input_dir)

    if one_off_cidr_cef:
        b_list = one_off_next_hop(b_list)

    diff_data_set = diffhelper.get_a_data_set_diff(a_list, b_list)

    spreadsheet_file_name = pdt.file_name_increase('file_diff.xlsx', output_dir)

    excel_obj = mod.scripts.WriteXlsxDiff(os.path.join(output_dir, spreadsheet_file_name),
                                          diffhelper.list_with_line_numbers(a_list),
                                          diffhelper.list_with_line_numbers(b_list), diff_data_set)
    excel_obj.write_spreadsheet()

    print('File named {file_name} created in {folder}'.format(file_name=spreadsheet_file_name, folder=output_dir))


def multi_file_diff(input_dir_1, input_dir_2, output_dir, one_off_cidr_cef, vba_data_dir):
    """
    Function to do a 2 folder diff, and output a Excel Spreadsheet, the files must be named the same
    in both directories.
    :param input_dir_1: A Directory
    :param input_dir_2: A Directory
    :param output_dir: The output directory
    :param one_off_cidr_cef: Created cause of issue with ASR 9K OS Upgrades
    :param vba_data_dir: The location of the vba directory
    :return:
        None

    """
    LOGGER.debug('Starting Function multi_file_diff')

    diff_data_dict = dict()

    file_names_dir_1 = pdt.list_files_in_directory(input_dir_1)
    file_names_dir_2 = pdt.list_files_in_directory(input_dir_2)

    for file_name_1 in file_names_dir_1:
        a_list = None
        b_list = None
        if file_name_1 not in file_names_dir_2:
            a_list = pdt.file_to_list(file_name_1, input_dir_1)
            b_list = list()

        elif file_name_1 in file_names_dir_2:
            a_list = pdt.file_to_list(file_name_1, input_dir_1)
            b_list = pdt.file_to_list(file_name_1, input_dir_2)
            if one_off_cidr_cef:
                if 'CEF' in file_name_1:
                    b_list = one_off_next_hop(b_list)

        file_name_1_split = file_name_1.split('.')
        diff_data_dict[file_name_1_split[0].upper()] = diffhelper.get_a_data_set_diff(a_list, b_list)

    spreadsheet_file_name = pdt.file_name_increase('folder_diff.xlsm', output_dir)

    excel_obj = mod.scripts.WriteXlsxMultiTabDiff(os.path.join(output_dir, spreadsheet_file_name), diff_data_dict,
                                                  vba_data_dir)
    excel_obj.write_spreadsheet()

    print('File named {file_name} created in {folder}'.format(file_name=spreadsheet_file_name, folder=output_dir))


def one_off_next_hop(orig_list):
    """
    Function to correct a CEF table that changed from nh X.X.X.X to X.X.X.X/32
    :param orig_list: Original list
    :return:
        A corrected CEF table list

    """
    fixed_list = list()
    for line in orig_list:
        line_split = re.split(r'(\s+)', line)
        if len(line_split) == 7:
            if ipv4.ucast_ip_mask(line_split[2], return_tuple=False):
                ip_addr_split = line_split[2].split('/')
                line_split[2] = '{ip_addr}   '.format(ip_addr=ip_addr_split[0])
        fixed_list.append(''.join(line_split))

    return fixed_list
