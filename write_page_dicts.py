from dict_util import write_dict_in_stream
from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv


try:
	input_path = Path(argv[1])
except IndexError:
	print("The path to a PDF file must be provided as an argument.")
	exit()

try:
	output_path = Path(argv[2])
except IndexError:
	output_path = input_path.parents[0]/(input_path.stem + ".txt")

reader = PdfFileReader(input_path.open("rb"))
pages = reader.pages

with output_path.open("w") as output_stream:
	output_stream.write("Content of " + str(input_path) + "\n")

	for i in range(len(pages)):
		output_stream.write("\nPage " + str(i) + "\n")
		write_dict_in_stream(pages[i], output_stream, after_line="\n")
		#output_stream.write("\n")
