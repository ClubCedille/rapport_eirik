"""
This script copies a PDF file and writes the name of the copy's text fields
in them. The original file is not modified.

Args:
	1: path to the input PDF file
	2: (optional) path to the output PDF file
"""

from jazal import\
	MissingPathArgWarner,\
	make_altered_name,\
	make_altered_path
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import\
	make_writer_from_reader,\
	set_need_appearances
from sys import argv, exit


DFLT_OUTPUT_TERMINATION = "_field_names"
ERROR_INTRO = "ERROR! "
PDF_EXTENSION = ".pdf"
TEXT_FIELD_TYPE = "/Tx"


def make_field_name_list(pdf_reader):
	pdf_fields = pdf_reader.getFields()
	if pdf_fields is None:
		return None

	name_list = list()
	for name, field in pdf_fields.items():
		if field.fieldType == TEXT_FIELD_TYPE:
			name_list.append(name)

	return name_list


# Input path checks
missing_input_warner = MissingPathArgWarner("Input file", (PDF_EXTENSION,))
try:
	input_path = Path(argv[1])
	input_path_checker =\
		missing_input_warner.make_reactive_path_checker(input_path)
	input_path_checker.check_path_exists()
	input_path_checker.check_extension_correct()

except IndexError:
	print(ERROR_INTRO + missing_input_warner.make_missing_arg_msg())
	exit()

except Exception as e:
	print(ERROR_INTRO + str(e))
	exit()

# Output path checks
missing_output_warner = MissingPathArgWarner("Output file", (PDF_EXTENSION,))
try:
	output_path = Path(argv[2])

	output_path_checker =\
		missing_output_warner.make_reactive_path_checker(output_path)

	if output_path_checker.path_is_dir():
		output_path = output_path/make_altered_name(
				input_path, after_stem=DFLT_OUTPUT_TERMINATION,
				extension=output_path_checker.extension_to_str())
	else:
		output_path_checker.check_extension_correct()

except IndexError:
	output_path = make_altered_path(
		input_path,
		after_stem=DFLT_OUTPUT_TERMINATION,
		extension=missing_output_warner.extension_to_str())

except Exception as e:
	print(ERROR_INTRO + str(e))
	exit()

# Real work
reader = PdfFileReader(input_path.open(mode="rb"))
writer = make_writer_from_reader(reader, False)

field_list = make_field_name_list(reader)
field_update = dict(zip(field_list, field_list))

page = reader.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible
writer.write(output_path.open(mode="wb"))
