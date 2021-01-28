from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit

# This script writes the name and value of a PDF file's fields in a .txt file.
# argv[1]: path to the input PDF file
# argv[2]: (optional) path to the output .txt file

INPUT_EXTENSION = ".pdf"
OUTPUT_EXTENSION = ".txt"

def check_path_existence(path):
	if not path.exists():
		print("ERROR! " + str(path) + " does not exist.")
		exit()

# Input path checks
try:
	input_path = Path(argv[1])
except IndexError:
	print("ERROR! Need the input file as the first argument.")
	exit()

check_path_existence(input_path)

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

pdf_fields = reader.getFields()
if pdf_fields is None:
	print("File " + str(input_path) + " does not have fields.")
	exit()

field_str = str()
for mapping_name, field in pdf_fields.items():
	field_str += str(mapping_name) + " (" + str(field.fieldType) + "): " + str(field.value) + "\n"

output_path.write_text(field_str)
