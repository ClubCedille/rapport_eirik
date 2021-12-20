"""
This script copies a PDF file and writes the name of the copy's text fields
in them. The original file is not modified.

Args:
	1: the path to the input PDF file
	2: (optional) the path to the output PDF file
"""


from path_arg_checks import check_io_path_pair
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import\
	make_writer_from_reader,\
	set_need_appearances
from sys import argv


_EXTENSION_PDF = ".pdf"

_TYPE_TEXT_FIELD = "/Tx"


def make_field_name_list(pdf_reader):
	pdf_fields = pdf_reader.getFields()
	if pdf_fields is None:
		return None

	name_list = list()
	for name, field in pdf_fields.items():
		if field.fieldType == _TYPE_TEXT_FIELD:
			name_list.append(name)

	return name_list

try:
	input_path = Path(argv[1])
except IndexError:
	input_path = None

try:
	output_path = Path(argv[2])
except IndexError:
	output_path = None

output_path = check_io_path_pair(
	input_path, "Input file", _EXTENSION_PDF,
	output_path, "Output file", _EXTENSION_PDF,
	"_field_names")

reader = PdfFileReader(input_path.open(mode="rb"))
writer = make_writer_from_reader(reader, False)

field_list = make_field_name_list(reader)
field_update = dict(zip(field_list, field_list))

page = reader.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible
writer.write(output_path.open(mode="wb"))
