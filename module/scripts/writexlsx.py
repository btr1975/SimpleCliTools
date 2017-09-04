#!/usr/bin/env python3
import logging
from xlsxwriter import Workbook
import os
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = ''
__license__ = ''
__status__ = 'dev'
__version_info__ = (1, 0, 5, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class WriteXlsxDiff(Workbook):
    """
    Class to Write the Diff Spreadsheet
    """
    def __init__(self, file_name, pre_cleaned, post_cleaned, diff_data):
        LOGGER.debug('Initializing class {class_obj}'.format(class_obj=type(self)))
        super().__init__(filename=file_name)
        self.file_name = file_name
        self.pre_cleaned = pre_cleaned
        self.post_cleaned = post_cleaned
        self.diff_data = diff_data

    def __changed_cell_format(self):
        """
        Method to change the format of a changed cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __changed_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#ffcccc'})
        return cellformat

    def __regular_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __regular_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1})
        return cellformat

    def __sheet_create(self, sheet_name):
        """
        Method to create a sheet
        :param sheet_name: The name of the sheet
        :return:
            A sheet object

        """
        LOGGER.debug('Starting method __sheet_create in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.add_worksheet(sheet_name)
        sheet_obj.hide_gridlines(2)
        return sheet_obj

    def __write_diff_data(self):
        """
        Method to write the diff sheet
        :return:
            None

        """
        LOGGER.debug('Starting method __write_diff_data in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.__sheet_create('DIFF')
        row = 0

        for line in self.diff_data:
            if line[0] == 'changed':
                sheet_obj.write(row, 0, line[0], self.__changed_cell_format())
                sheet_obj.write(row, 1, line[1], self.__changed_cell_format())
                sheet_obj.write(row, 2, line[2], self.__changed_cell_format())
                sheet_obj.write(row, 3, line[3], self.__changed_cell_format())
                sheet_obj.write(row, 4, line[4], self.__changed_cell_format())
                sheet_obj.write(row, 5, line[5], self.__changed_cell_format())
            else:
                sheet_obj.write(row, 0, line[0], self.__regular_cell_format())
                sheet_obj.write(row, 1, line[1], self.__regular_cell_format())
                sheet_obj.write(row, 2, line[2], self.__regular_cell_format())
                sheet_obj.write(row, 3, line[3], self.__regular_cell_format())
                sheet_obj.write(row, 4, line[4], self.__regular_cell_format())
                sheet_obj.write(row, 5, line[5], self.__regular_cell_format())

            row += 1

        sheet_obj.autofilter('A1:F{last_row}'.format(last_row=row+1))

    def __write_original_data(self):
        """
        Method to write the pre and post sheet
        :return:
            None

        """
        LOGGER.debug('Starting method __write_original_data in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj_pre = self.__sheet_create('PRE')

        row = 0
        for line in self.pre_cleaned:
            sheet_obj_pre.write(row, 0, line, self.__regular_cell_format())
            row += 1

        sheet_obj_post = self.__sheet_create('POST')

        row = 0
        for line in self.post_cleaned:
            sheet_obj_post.write(row, 0, line, self.__regular_cell_format())
            row += 1

    def write_spreadsheet(self):
        """
        Method to call the spreadsheet writer
        :return:
            None

        """
        LOGGER.debug('Starting method write_spreadsheet in class {class_obj}'.format(class_obj=type(self)))
        self.__write_original_data()
        self.__write_diff_data()


class WriteXlsxTabs(Workbook):
    """
    Class to Write the Spreadsheet
    """
    def __init__(self, file_name, **kwargs):
        LOGGER.debug('Initializing class {class_obj}'.format(class_obj=type(self)))
        super().__init__(filename=file_name)
        self.file_name = file_name
        self.tab_data = kwargs

    def __regular_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __regular_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1})
        return cellformat

    def __sheet_create(self, sheet_name):
        """
        Method to create a sheet
        :param sheet_name: The name of the sheet
        :return:
            A sheet object

        """
        LOGGER.debug('Starting method __sheet_create in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.add_worksheet(sheet_name)
        sheet_obj.hide_gridlines(2)
        return sheet_obj

    def __write_data(self):
        """
        Method to write the sheet
        :return:
            None

        """
        LOGGER.debug('Starting method __write_data in class {class_obj}'.format(class_obj=type(self)))
        for data_list_name in self.tab_data:
            sheet_obj_pre = self.__sheet_create(data_list_name)
            row = 0
            for line in self.tab_data[data_list_name]:
                sheet_obj_pre.write(row, 0, line, self.__regular_cell_format())
                row += 1

    def write_spreadsheet(self):
        """
        Method to call the spreadsheet writer
        :return:
            None

        """
        LOGGER.debug('Starting method write_spreadsheet in class {class_obj}'.format(class_obj=type(self)))
        self.__write_data()


class WriteXlsxMultiTabDiff(Workbook):
    """
    Class to Write the Diff Spreadsheet
    """
    def __init__(self, file_name, diff_data_dict, vba_dir=None):
        LOGGER.debug('Initializing class {class_obj}'.format(class_obj=type(self)))
        super().__init__(filename=file_name)
        self.file_name = file_name
        self.diff_data_dict = diff_data_dict
        if vba_dir:
            self.set_vba_name('ThisWorkBook')
            self.add_vba_project(os.path.join(vba_dir, 'vbaProjectTabSort.bin'))

    def __changed_cell_format(self):
        """
        Method to change the format of a changed cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __changed_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#ffcccc'})
        return cellformat

    def __regular_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __regular_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1})
        return cellformat

    def __sheet_create(self, sheet_name):
        """
        Method to create a sheet
        :param sheet_name: The name of the sheet
        :return:
            A sheet object

        """
        LOGGER.debug('Starting method __sheet_create in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.add_worksheet(sheet_name)
        sheet_obj.hide_gridlines(2)
        return sheet_obj

    def __write_diff_data(self, diff_data, tab_name):
        """
        Method to write the diff sheet
        :return:
            None

        """
        LOGGER.debug('Starting method __write_diff_data in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.__sheet_create(tab_name)
        row = 0

        for line in diff_data:
            if line[0] == 'changed':
                sheet_obj.write(row, 0, line[0], self.__changed_cell_format())
                sheet_obj.write(row, 1, line[1], self.__changed_cell_format())
                sheet_obj.write(row, 2, line[2], self.__changed_cell_format())
                sheet_obj.write(row, 3, line[3], self.__changed_cell_format())
                sheet_obj.write(row, 4, line[4], self.__changed_cell_format())
                sheet_obj.write(row, 5, line[5], self.__changed_cell_format())
            else:
                sheet_obj.write(row, 0, line[0], self.__regular_cell_format())
                sheet_obj.write(row, 1, line[1], self.__regular_cell_format())
                sheet_obj.write(row, 2, line[2], self.__regular_cell_format())
                sheet_obj.write(row, 3, line[3], self.__regular_cell_format())
                sheet_obj.write(row, 4, line[4], self.__regular_cell_format())
                sheet_obj.write(row, 5, line[5], self.__regular_cell_format())

            row += 1

        sheet_obj.autofilter('A1:F{last_row}'.format(last_row=row+1))

    def write_spreadsheet(self):
        """
        Method to call the spreadsheet writer
        :return:
            None

        """
        LOGGER.debug('Starting method write_spreadsheet in class {class_obj}'.format(class_obj=type(self)))
        for tab_name in self.diff_data_dict:
            self.__write_diff_data(self.diff_data_dict[tab_name], tab_name)


class WriteXlsxAggregate(Workbook):
    """
    Class to Write the Spreadsheet for Subnet Aggregator
    """
    def __init__(self, file_name, agg_dict, top_n_dict, total_possible):
        LOGGER.debug('Initializing class {class_obj}'.format(class_obj=type(self)))
        super().__init__(filename=file_name)
        self.file_name = file_name
        self.agg_dict = agg_dict
        self.total_possible = str(total_possible)
        self.top_n_dict = top_n_dict

    def __regular_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __regular_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'left': 1,
            'right': 1})
        return cellformat

    def __all_matched_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __all_matched_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'left': 1,
            'right': 1,
            'fg_color': '#ccff99'})
        return cellformat

    def __unmatched_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __unmatched_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'left': 1,
            'right': 1,
            'fg_color': '#ffcccc'})
        return cellformat

    def __header_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        LOGGER.debug('Starting method __header_cell_format in class {class_obj}'.format(class_obj=type(self)))
        cellformat = self.add_format({
            'border': 1,
            'bold': True,
            'underline': True})
        return cellformat

    def __sheet_create(self, sheet_name):
        """
        Method to create a sheet
        :param sheet_name: The name of the sheet
        :return:
            A sheet object

        """
        LOGGER.debug('Starting method __sheet_create in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj = self.add_worksheet(sheet_name)
        sheet_obj.hide_gridlines(2)
        return sheet_obj

    def __write_data(self):
        """
        Method to write the sheet
        :return:
            None

        """
        LOGGER.debug('Starting method __write_data in class {class_obj}'.format(class_obj=type(self)))
        sheet_obj_pre = self.__sheet_create('AGGS')
        col = 0
        max_row = 0
        for data_list_name in self.agg_dict:
            row = 0
            sheet_obj_pre.write(row, col, data_list_name, self.__header_cell_format())
            row += 1
            if len(self.agg_dict[data_list_name].get('matched')) == int(self.total_possible):
                for line in self.agg_dict[data_list_name].get('matched'):
                    sheet_obj_pre.write(row, col, line, self.__all_matched_cell_format())
                    row += 1
                    if row > max_row:
                        max_row = row + 5

            else:
                for line in self.agg_dict[data_list_name].get('matched'):
                    sheet_obj_pre.write(row, col, line, self.__regular_cell_format())
                    row += 1
                    if row > max_row:
                        max_row = row + 5

            for line in self.agg_dict[data_list_name].get('unmatched'):
                sheet_obj_pre.write(row, col, line, self.__unmatched_cell_format())
                row += 1
                if row > max_row:
                    max_row = row + 5

            sheet_obj_pre.write(row, col, 'Aggregated: {total_possible}'.format(total_possible=len(self.agg_dict[data_list_name].get('matched'))), self.__regular_cell_format())
            col += 1

        sheet_obj_pre.write(max_row + 2, 0, 'Total Possible: {total_possible}'.format(total_possible=self.total_possible), self.__regular_cell_format())

        # Test

        sheet_obj_top_n = self.__sheet_create('TOP')
        col = 0
        max_row = 0
        for data_list_name in self.top_n_dict:
            row = 0
            sheet_obj_top_n.write(row, col, data_list_name, self.__header_cell_format())
            row += 1
            if len(self.top_n_dict[data_list_name].get('matched')) == int(self.total_possible):
                for line in self.top_n_dict[data_list_name].get('matched'):
                    sheet_obj_top_n.write(row, col, line, self.__all_matched_cell_format())
                    row += 1
                    if row > max_row:
                        max_row = row + 5

            else:
                for line in self.top_n_dict[data_list_name].get('matched'):
                    sheet_obj_top_n.write(row, col, line, self.__regular_cell_format())
                    row += 1
                    if row > max_row:
                        max_row = row + 5

            for line in self.top_n_dict[data_list_name].get('unmatched'):
                sheet_obj_top_n.write(row, col, line, self.__unmatched_cell_format())
                row += 1
                if row > max_row:
                    max_row = row + 5

            sheet_obj_top_n.write(row, col, 'Aggregated: {total_possible}'.format(total_possible=len(self.top_n_dict[data_list_name].get('matched'))), self.__regular_cell_format())
            col += 1

        sheet_obj_top_n.write(max_row + 2, 0, 'Total Possible: {total_possible}'.format(total_possible=self.total_possible), self.__regular_cell_format())

    def write_spreadsheet(self):
        """
        Method to call the spreadsheet writer
        :return:
            None

        """
        LOGGER.debug('Starting method write_spreadsheet in class {class_obj}'.format(class_obj=type(self)))
        self.__write_data()