# LocalizationPyTools



## What is LocPyTools and why to use it

Imagine you set up all localizable texts in your Unreal project and now you want to send them over to the localization company for translation process. However, the localization company of your choice doesn't want to work with PO files provided by Unreal; they want XLSX files instead.

Here comes the __LocPyTools__ - this python program provides a set of tools that automatize generating a XLSX file with missing translations and rewrites Unreal PO files with translations read from existing XLSX documments.

## Basic assumptions

Before using LocPyTools you need to learn about some basic assumptions takes during developing this program:

- all string tables used in UE project are created from data loaded from CSV files
- all localization data have been exported from UE built-in Localization system to a bunch of PO files
- the translation company of your choice uses only with XLSX files for texts translation
- texts IDs in XLSX files are composed with CSV file name and text key used in UE separated by the '+' sign:
  eg.: 'ST_SomeFile.csv+Some_Text_ID'



## Installation and usage

__LocPyTools__ was developed and tested with Python 3.10. All source scripts can be found in *LocalizationPyTools* directory on this repository.

You can either run `locpytools.py` script from *LocalizationPyTool/Source* directory on your own or use provided executable file available in *LocalizationPyTools/dist* directory.

The *UETestProject* directory contains an example project created in Unreal Engine, while the *XlsxTranslations* directory holds some translations for texts found in this project. Feel free to play with it and learn how to use the __LocPyTools__ program.

## Support
In case of any questions you can contact me at sosnowska.kk@gmail.com.

## License
This project is licensed under the MIT License. [Learn more](https://choosealicense.com/licenses/mit/)




# LocPyTools Manual

Following paragraphs contain descriptions of all commands available in __LocPyTools__ program.

## The `-h, -help` commands

It prints a short manual for the program.

## The `quit` command

It quits the program.

## The `mkconfig` command

It generates the `.config` file used by other tools. Note that this file is automatically generated at the start of the program if none `.config` file has been found.

## The `xlsxan` command

It runs the analyser tool for all XLSX files found in input directory. The result of this analysis is a dictionary with all translations for each found native text. All input arguments are read from config file (`xlsxan` prefix).

### Usage

1. Run __locpytools__ program. Make sure that the `.config` file exists - if not, you can generate one using the `mkconfig` command.
1. Make sure the `.config` file has proper data for arguments with prefix `xlsxan`.
1. Run `xlsxan` command in __locpytools__ program.

## The `lmt` command

It runs the `listmissingtexts` tool, which generates a new XLSX file with all missing translations.

First, it analyses all XLSX files with translations and register all translations in a dedicated dictionary. For this step, the `xlsxan` tool is used.

After that, the program goes through all input CSV files (those files are used to create string tables used in UE project) and read their content. Each text ID from CSV file that is not in generated translations dictionary is written down into output XLSX file. As a result, the output XLSX file will contain all texts that are missing their translations.

### Usage

1. Run __locpytools__ program. Make sure that the `.config` file exists - if not, you can generate one using the `mkconfig` command.
1. Make sure the `.config` file has proper data for arguments with prefixes `xlsxan` and `lmt`.
1. Run `lmt` command in __locpytools__ program.
1. New `MissingTexts_XYZ.xlsx` file should be generated inside the path provided for `lmt_xlsx_output_dir` argument. The XYZ in the file name will be replaced with a date and time of the file creation.

## The `lct` command

It runs the `listchangedtexts` tool, which generates a new XLSX file with all source texts, that have been changed and may have outdated translations. Generally, this program helps to find all source texts, whose new meaning is completely different from the previous version, which invalidate their existing translations.

This simple program analyses data from the input PO file with native culture. It compares the content of the `msgstr` and the `msgid` parts of the localized text data. If `msgstr` text is different than the text assigned to `msgid`, it means that the source text in `msgid` has changed, and the existing translation stored in `msgstr` property may be outdated.

### Usage

1. Open your project in Unreal editor, go to the `Localization Dashboard` window and use *Gather texts* option to update localized texts archives in your project.
1. Run __locpytools__ program. Make sure that the `.config` file exists - if not, you can generate one using the `mkconfig` command.
1. Make sure the `.config` file has proper data for arguments with `lct` prefix.
1. Run `lct` command in __locpytools__ program.
1. New `ChangedTexts_XYZ.xlsx` file should be generated inside the path provided for `lct_xlsx_output_dir` argument. The XYZ in the file name will be replaced with a date and time of the file creation.

## The `pou` command

It runs the `poupdater` tool, that updates existing PO files with provided texts translations found in XLSX files.

First, it analyses all XLSX files with translations and register all translations in a dedicated dictionary. For this step, the `xlsxan` tool is used.

After that, it goes through all input PO files (those are set of texts for all cultures used in UE project) found inside subdirectories of input directory and read their content. For each text ID `msgctxt` that has existing translations in generated translations dictionary its assigned translation text `msgstr` is replaced by updated translation from generated translations dictionary.

### Usage

1. Open your project in Unreal editor and go to the `Localization Dashboard` window. Use the *Export texts* option available under `Cultures` tab to generate a PO file for all cultures (you can also export texts to PO for each culture separatedly).
1. Run __locpytools__ program. Make sure that the `.config` file exists - if not, you can generate one using the `mkconfig` command.
1. Make sure the `.config` file has proper data for arguments with prefixes `xlsxan` and `pou`.
1. Run `pou` command in __locpytools__ program.
1. At this point, all PO files inside the directory path provided for `pou_po_source_dir` have been updated with the existing translations loaded from XLSX files.
1. Go back to the `Localization Dashboard` in the Unreal editor and use the *Import texts* option available under `Cultures` tab to load new translations for all cultures from updated PO files (you can also import texts from PO for each culture separatedly).