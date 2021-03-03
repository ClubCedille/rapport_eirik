# This script copies a PDF file and writes the name of the copy's fields in them.
# argv[1]: path to the input PDF file
# argv[2]: (optional) path to the output PDF file


from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, set_need_appearances
from sys import argv, exit


PDF_EXTENSION = ".pdf"
PDF_EXTENSION_AS_LIST = [PDF_EXTENSION]
TEXT_FIELD_TYPE = "/Tx"


def check_path_existence(path):
	if not path.exists():
		print("ERROR! " + str(path) + " does not exist.")
		exit()


def _make_default_output_file_name(input_path):
	return _make_default_output_file_stem(input_path) + PDF_EXTENSION


def _make_default_output_file_stem(input_path):
	return input_path.stem + "_field_names"


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
try:
	input_path = Path(argv[1])
except IndexError:
	print("ERROR! The path to a " + _INPUT_EXTENSION
		+ " file must be provided as the first argument.")
	exit()

check_path_existence(input_path)

if input_path.suffixes != PDF_EXTENSION_AS_LIST: # False if not a file
	print("ERROR! The first argument must be the path to a "
		+ PDF_EXTENSION + " file.")
	exit()

# Output path checks
try:
	output_path = Path(argv[2])

	if output_path.is_dir():
		output_path = output_path/_make_default_output_file_name(input_path)

	elif output_path.suffixes != PDF_EXTENSION_AS_LIST:
		output_path = output_path.with_suffix(PDF_EXTENSION)

except IndexError:
	output_path = input_path.with_name(
		_make_default_output_file_name(input_path))

# Actual work
reader = PdfFileReader(input_path.open(mode="rb"))
writer = make_writer_from_reader(reader, False)

field_list = make_field_name_list(reader)
field_update = dict(zip(field_list, field_list))

page = reader.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible
writer.write(output_path.open(mode="wb"))
