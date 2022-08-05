# author: Katarzyna 'K8' Sosnowska
# e-mail: sosnowska.kk@gmail.com
# 
# date of last update: 2022-08-05
# 
# # About: 
# This file contains helper class for managing reading and writing 
# config files with settings used in locpytools program.
# 
# .

import os
from datetime import datetime

# config file variables:
XLSXAN_TRANSLATIONS_DIR = "xlsxan_translations_dir"
XLSXAN_MAX_COLUMNS = "xlsxan_max_columns"
LMT_SOURCE_CSV_DIR = "lmt_source_csv_dir"
LMT_XLSX_OUTPUT_DIR = "lmt_xlsx_output_dir"
LMT_SEPARATOR = "lmt_separator"
POU_PO_SOURCE_DIR = "pou_po_source_dir"

DEFAULT_ID_PREFIX = ','
STR_NONE = "none"
CONFIG_FILE_NAME = "config"

'''
This class encapsulates all settings used in Loc Tools UE program.
'''
class LocToolsConfig:
    # xlsxan (xlsx-analyser) settings:
    xlsxan_translations_dir = STR_NONE
    xlsxan_max_columns = 5
    # lmt (list-missing-texst) settings:
    lmt_source_csv_dir = STR_NONE
    lmt_xlsx_output_dir = STR_NONE
    lmt_separator = STR_NONE
    # pou (po-updater) settings:
    pou_po_source_dir = STR_NONE

    '''
    Writes down current state of all variables into a file with given path <config_file_path>.
    '''
    def write_config_to_file(self):
        with open(CONFIG_FILE_NAME, "w") as config_file:
            config_file.write("### This is a LocalizationPyTools config file\n")
            config_file.write("# This config file was generated {0}\n".format(datetime.now()))
            # generate xlsxan (xlsx-analyser) variables:
            config_file.write("\n## XLSXAN (xlsx-analyser) tool setting:\n")
            config_file.write("# {0} - a path to a directory with XLSX files with texts translations.\n".format(XLSXAN_TRANSLATIONS_DIR))
            config_file.write("{0}=none\n".format(XLSXAN_TRANSLATIONS_DIR))
            config_file.write("# {0} - limit of columns, that will be inspected in XLSX file\n".format(XLSXAN_MAX_COLUMNS))
            config_file.write("{0}=5\n".format(XLSXAN_MAX_COLUMNS))
            # lmt (list-missing-texst) variables:
            config_file.write("\n## LMT (list-missing-texts) tool settings:\n")
            config_file.write("# {0} - a path to a directory with all csv source files, which contain all native texts.\n".format(LMT_SOURCE_CSV_DIR))
            config_file.write("{0}=none\n".format(LMT_SOURCE_CSV_DIR))
            config_file.write("# {0} - a path to a directory, where the output XLSX file with list of missing translations will be generated.\n".format(LMT_XLSX_OUTPUT_DIR))
            config_file.write("{0}=none\n".format(LMT_XLSX_OUTPUT_DIR))
            config_file.write("# {0} - a single character or a phrase used for separating cells with data in CSV files (eg. a comma ',').\n".format(LMT_SEPARATOR))
            config_file.write("{0}=,\n".format(LMT_SEPARATOR))
            # generate pou (po-updater) variables:
            config_file.write("\n## POU (po-updater) tool settings:\n")
            config_file.write("# {0} - a path to a directory with PO files, that whill be updated during POU tool job.\n".format(POU_PO_SOURCE_DIR))
            config_file.write("{0}=none\n".format(POU_PO_SOURCE_DIR))
        pass

    '''
    Updates variables state with data from a `config` file inside the current directory.
    '''
    def load_config_data(self):
        if not os.path.exists(CONFIG_FILE_NAME):
            print("[configtools] Couldn't load data from file path: {0}!".format(CONFIG_FILE_NAME))
            return
        with open(CONFIG_FILE_NAME, "r") as config_file:
            for line in config_file:
                words = line.split('=')
                if len(words) <= 1:
                    continue
                # parsing xlsx-analyser variables:
                elif words[0] == XLSXAN_TRANSLATIONS_DIR:
                    self.xlsxan_translations_dir = words[1].rstrip('\r\n')
                elif words[0] == XLSXAN_MAX_COLUMNS:
                    self.xlsxan_max_columns = int(words[1].rstrip('\r\n'))
                    # parsing list-missing-texts variables:
                elif words[0] == LMT_SOURCE_CSV_DIR:
                    self.lmt_source_csv_dir = words[1].rstrip('\r\n')
                elif words[0] == LMT_XLSX_OUTPUT_DIR:
                    self.lmt_xlsx_output_dir = words[1].rstrip('\r\n')
                elif words[0] == LMT_SEPARATOR:
                    self.lmt_separator = words[1].rstrip('\r\n')
                # parsing po_updater variables:
                elif words[0] == POU_PO_SOURCE_DIR:
                    self.pou_po_source_dir = words[1].rstrip('\r\n')
        pass

    '''
    This methods returns a tuple with all settings needed for 'xlsxan' tool.
    returns: (xlsx_translations_dir, xlsxan_max_columns)
    '''
    def get_xlsxan_settings(self):
        return self.xlsxan_translations_dir, self.xlsxan_max_columns
    
    '''
    This methods returns a tuple with all settings needed for 'lmt' tool.
    returns: (lmt_source_csv_dir, lmt_xlsx_output_dir, lmt_separator)
    '''
    def get_lmt_settings(self):
        return self.lmt_source_csv_dir, self.lmt_xlsx_output_dir, self.lmt_separator
    
    '''
    This methods returns a tuple with all settings needed for 'pou' tool.
    returns: (pou_po_source_dir)
    '''
    def get_po_updater_settings(self):
        return self.pou_po_source_dir

'''
Generates new config file if can't find any in specified './config' location.
'''
def generate_new_config():
    config_data = LocToolsConfig()
    config_data.write_config_to_file()
    print("[configtools] generated config file.")
    pass

#===============================================================================================

if __name__== "__main__":
    generate_new_config()
    pass