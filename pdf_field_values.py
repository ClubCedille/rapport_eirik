from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit

# This script writes the name and value of a PDF file's fields in a .txt file.
# argv[1]: path to the input PDF file
# argv[2]: (optional) path to the output .txt file

class FieldRecord:
	def __init__(self, name, val_type, value):
		self.name = name if type(name) is str else str(name)
		self.val_type = val_type
		self.value = value

	def __str__(self):
		return self.name + " (" + str(self.val_type) + "): " + str(self.value)


def get_pdf_field_list(pdf_reader):
	pdf_fields = pdf_reader.getFields()
	if pdf_fields is None:
		return None

	field_list = list()
	for mapping_name, field in pdf_fields.items():
		field_list.append(FieldRecord(mapping_name, field.fieldType, field.value))

	return field_list


if __name__ == "__main__":
	INPUT_EXTENSION = ".pdf"
	OUTPUT_EXTENSION = ".txt"

	# Input path checks
	try:
		input_path = Path(argv[1])
	except IndexError:
		print("ERROR! Need the input file as the first argument.")
		exit()

	if not input_path.exists():
		print("ERROR! " + str(input_path) + " does not exist.")
		exit()

	if not input_path.suffix == INPUT_EXTENSION: # False if not a file
		print("ERROR! The input file must have the extension " + INPUT_EXTENSION + ".")
		exit()

	# Output path checks
	try:
		output_path = Path(argv[2])
	except IndexError:
		output_path = Path("field_values.txt")

	if not output_path.suffix == OUTPUT_EXTENSION: # False if not a file
		print("ERROR! The output file must have the extension " + OUTPUT_EXTENSION + ".")
		exit()

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"))
	field_list = get_pdf_field_list(reader)
	field_str = str()

	for field in field_list:
		field_str += str(field) + "\n"

	header = "Fields in file " + str(input_path) + "\n\n"
	output_path.write_text(header + field_str)
