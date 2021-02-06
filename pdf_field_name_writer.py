from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, set_need_appearances
from sys import argv, exit

# This script copies a PDF file and writes the name of the copy's fields in them.
# argv[1]: path to the input PDF file
# argv[2]: (optional) path to the output PDF file

PDF_EXTENSION = ".pdf"
TEXT_FIELD_TYPE = "/Tx"

def check_path_existence(path):
	if not path.exists():
		print("ERROR! " + str(path) + " does not exist.")
		exit()


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
	print("ERROR! Need the input file as the first argument.")
	exit()

check_path_existence(input_path)

if not input_path.suffix == PDF_EXTENSION: # False if not a file
	print("ERROR! The input file must have the extension " + PDF_EXTENSION + ".")
	exit()

# Output path checks
try:
	output_path = Path(argv[2])
except IndexError:
	output_path = Path("field_names.pdf")

if not output_path.suffix == PDF_EXTENSION: # False if not a file
	print("ERROR! The output file must have the extension " + PDF_EXTENSION + ".")
	exit()

# Actual work
reader = PdfFileReader(input_path.open(mode="rb"))
writer = make_writer_from_reader(reader, False)

field_list = make_field_name_list(reader)
# By AXDOOMER on branch fieldsname_location
field_update = dict(zip(field_list, field_list))

page = reader.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible
writer.write(output_path.open(mode="wb"))
