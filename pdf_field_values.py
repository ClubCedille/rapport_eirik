from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit

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

try:
	field_values = reader.getFormTextFields()
except TypeError:
	print("File " + str(input_path) + " does not have fields.")
	exit()

field_str = str()
for field, value in field_values.items():
	field_str += str(field) + ": " + str(value) + "\n"

output_path.write_text(field_str)
