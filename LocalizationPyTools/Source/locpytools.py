# author: Katarzyna 'K8' Sosnowska
# e-mail: sosnowska.kk@gmail.com
# 
# date of last update: 2022-08-21
# 
# # About: 
# This program is an entry point for using tools dedicated to a particular pipeline used 
# with Unreal Engine built-in Localization system.
# 
# Here, you have access to two following tools:
# 
# XLSX Analyser:
#  > command: xlsxan
#  > description: Reads all XLSX files found in input directory and generates
#                 a dictionary with all translations for each found native text.
#                 All input arguments are read from config file (`xlsxan` prefix).
# 
# List Missing Texts:
#  > command: lmt
#  > description: Searches texts with missing translations in input CSV files.
#                 All missing translations are written into generated XLSX file.
#                 Each text ID is combined from file name and real text ID.
#                 All input arguments are read from config file (`lmt` prefix).
# 
# PO Updater:
#  > command: pou
#  > description: Updates all PO files found in input directory subdirectories 
#                 with translations loaded from selected XLSX files.
#                 All input arguments are read from config file (`pou` prefix).
# 
# .

from configtools import LocToolsConfig
from configtools import generate_new_config, generate_config_if_needed
from xlsxanalyser import analyse_xlsx_translations
from listmissingtexts import list_missing_texts
from listchangedtexts import list_changed_native_texts
from poupdater import po_updater

# program commands and arguments:
HELP_SHORT = "-h"
HELP_FULL = "help"
QUIT_OPTION = "quit"
MAKE_CONFIG = "mkconfig"
XLSXAN_TOOL = "xlsxan"
LMT_TOOL = "lmt"
LCT_TOOL = "lct"
POU_TOOL = "pou"

# program messages:
WELCOME_MESSAGE = '''
[Localization Tools UE] is ON
Start using it or pass {} or {} for more info.
'''.format(HELP_SHORT, HELP_FULL)
QUIT_MESSAGE = '''[Localization Tools UE] program ended.'''
UNRECOGNISED_COMMAND_MESSAGE = "Unrecognized command. Pass {} or {} to see the program manual.".format(HELP_SHORT, HELP_FULL)
MANUAL_MESSAGE = '''Localization Tools UE - available options:
-h, help    Prints this help

quit        Quits the Localization Tools UE program

mkconfig    Generates a config file for other tools.
            (note that config file is being automatically generated 
            at the start of [Localization Tools UE] program.

xlsxan      Reads all XLSX files found in input directory and generates
            a dictionary with all translations for each found native text.
            All input arguments are read from a config file (`xlsxan` prefix).

lmt         Searches texts with missing translations in input CSV files.
            All missing translations are written into a generated XLSX file.
            Each text ID is combined from file name and real text ID.
            All input arguments are read from config file (`lmt` prefix).

lct         Searches texts with outdated translations in input PO file
            for native culture.
            All found texts are written into a generated XLSX file.
            All input arguments are read from a config file (`lct` prefix).

pou         Updates all PO files found in input directory subdirectories 
            with translations loaded from selected XLSX files.
            All input arguments are read from config file (`pou` prefix).\n
'''

CONFIG_FILE_PATH = "./config"

def run_xlsxan_program():
    config_data = LocToolsConfig()
    config_data.load_config_data()
    xlsxan_settings = config_data.get_xlsxan_settings()
    column_headers_map, translations_dict = analyse_xlsx_translations(xlsxan_settings[0], xlsxan_settings[1], True)
    pass

def run_lmt_program():
    config_data = LocToolsConfig()
    config_data.load_config_data()
    xlsxan_settings = config_data.get_xlsxan_settings()
    ltm_settings = config_data.get_lmt_settings()
    list_missing_texts(ltm_settings[0], xlsxan_settings[0], ltm_settings[1], ltm_settings[2])
    pass

def run_lct_program():
    config_data = LocToolsConfig()
    config_data.load_config_data()
    lct_settings = config_data.get_lct_settings()
    list_changed_native_texts(lct_settings[0], lct_settings[1])
    pass

def run_pou_program():
    config_data = LocToolsConfig()
    config_data.load_config_data()
    pou_settings = config_data.get_pou_settings()
    xlsxan_settings = config_data.get_xlsxan_settings()
    po_updater(pou_settings[0], pou_settings[1], xlsxan_settings[0], xlsxan_settings[1])
    pass

#===============================================================================================

if __name__== "__main__":
    generate_config_if_needed()
    print(WELCOME_MESSAGE)
    while True:
        args = input('> ').split(' ')
        if len(args) == 0:
            continue
        selectedTool = args[0]
        # print help message:
        if selectedTool in [HELP_SHORT, HELP_FULL]:
            print(MANUAL_MESSAGE)
            continue
        # quit the program:
        elif selectedTool == QUIT_OPTION:
            break
        # selectedTool is 'mkconfig':
        elif selectedTool == MAKE_CONFIG:
            generate_new_config()
        # selectedTool is 'xlsxan':
        elif selectedTool == XLSXAN_TOOL:
            run_xlsxan_program()
        # selectedTool is 'lmt':
        elif selectedTool == LMT_TOOL:
            run_lmt_program()
        # selectedTool is 'lmt':
        elif selectedTool == LCT_TOOL:
            run_lct_program()
        # selectedTool is 'pou':
        elif selectedTool == POU_TOOL:
            run_pou_program()
        # unrecognised command message:
        else:
            print(UNRECOGNISED_COMMAND_MESSAGE)
            continue
    print(QUIT_MESSAGE)