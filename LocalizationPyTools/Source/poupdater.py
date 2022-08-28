# author: Katarzyna 'K8' Sosnowska
# e-mail: sosnowska.kk@gmail.com
# 
# date of last update: 2022-08-06
# 
# # About: 
# This file contains methods for updating PO files with translations data read from given XLSX files.
# 
# # Base assumptions for this pipeline are as follows:
# - all string tables used in UE project are created from data loaded from CSV files
# - all localization data have been exported from UE built-in Localization system to a bunch of PO files
# - translation company provided a set of XLSX files with texts translations
# - texts IDs in XLSX files are composed with CSV file name and text key used in UE separated by the '+' sign:
#   eg.: 'ST_SomeFile.csv+Some_Text_ID'
# 
# # How POU program works?
# 
# First, it analyses all XLSX files with translations and register all translations in a dedicated dictionary.
# For this step, the xlsxanalyser tool is used.
# 
# After that, it goes through all input PO files (those are set of texts for all cultures used in UE project) 
# found inside subdirectories of input directory and read their content. For each text ID (msgctxt) that has 
# existing translations in generated translations dictionary its assigned translation text (msgstr) 
# is replaced by updated translation from generated translations dictionary.
#
# .

import os
from configtools import LocToolsConfig
from xlsxanalyser import analyse_xlsx_translations

MSGCTXT = "msgctxt "    # text ID
MSGSTR = "msgstr "      # translation text
PO_FILE_EXT = ".po"

'''
Overrides PO file texts with provided translations dictionary.
'''
def update_po_file(input_file_path, culture_code, translations_dict, text_id_separator):
    updated_lines = []
    debug_translations_count = 0
    debug_errors_count = 0
    debug_texts_count = 0
    # go line by line and update it with translation when applicable:
    with open(input_file_path, "r", encoding="utf8") as input_file:
        text_id = ""
        for line in input_file:
            if line.startswith(MSGCTXT):
                full_text_id = line[len(MSGCTXT) + 1:-2]
                text_id_parts = full_text_id.split(text_id_separator)
                if len(text_id_parts) < 2:
                    pass
                text_id = text_id_parts[1]
                debug_texts_count += 1
                if text_id not in translations_dict:
                    debug_errors_count += 1
                    pass
                updated_lines.append(line)
            elif line.startswith(MSGSTR):
                # translation was found in some XLSX file, use it:
                if text_id in translations_dict and culture_code in translations_dict[text_id]:
                    text_source = translations_dict[text_id][culture_code]
                    updated_lines.append("{0}\"{1}\"\n".format(MSGSTR, text_source))
                    debug_translations_count += 1
                # translation was not found in any XLSX file, reset MSGSTR:
                else:
                    updated_lines.append("{0}\"\"\n".format(MSGSTR))
                    debug_errors_count += 1
            else:
                updated_lines.append(line)
        pass
    # save updated file:
    with open(input_file_path, "w", encoding="utf8") as result_file:
        result_file.writelines(updated_lines)
    # log summary:
    print("\t> updated \"{0}\" file [{1} texts | {2} updated translations | {3} missing texts]".format(input_file_path, debug_texts_count, debug_translations_count, debug_errors_count))
    pass

'''
Searches all subdirectories inside input_dir_path for PO files and updates them with translations.
'''
def po_updater(input_dir_path, text_id_separator, translations_input_dir, max_column):
    if not os.path.exists(input_dir_path):
        print("\t> error: directory {0} doesn't exist!".format(input_dir_path))
        return
    # load translations data:
    column_headers_map, translations_dict = analyse_xlsx_translations(translations_input_dir, max_column, False)
    print("> generated {0} texts in translationsDict".format(len(translations_dict)))
    # update all PO files found in input dir:
    for loc_dir in os.scandir(input_dir_path):
        if not loc_dir.is_dir():
            continue
        print("> checking \'{0}\' directory".format(loc_dir.name))
        for file in os.scandir(loc_dir.path):
            if not file.is_file() or not file.name.endswith(PO_FILE_EXT):
                continue
            update_po_file(file.path, loc_dir.name, translations_dict, text_id_separator)
    pass

#===============================================================================================

if __name__== "__main__":
    config_data = LocToolsConfig()
    config_data.load_config_data()
    pou_settings = config_data.get_pou_settings()
    xlsxan_settings = config_data.get_xlsxan_settings()
    po_updater(pou_settings[0], pou_settings[1], xlsxan_settings[0], xlsxan_settings[1])
