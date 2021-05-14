from argparse import ArgumentParser
from arg_processing import make_parser, process_arguments, StructureType
from pathlib import Path
from pdf_obj_struct import write_pdf_obj_struct
from PyPDF2 import PdfFileReader


def _write_page_objs_in_stream(pdf_path, pages, w_stream, depth_limit):
	w_stream.write("Objects in the pages of " + str(pdf_path) + "\n")

	for i in range(len(pages)):
		page = pages[i]
		w_stream.write("\n\nPAGE " + str(i) + "\n")
		write_pdf_obj_struct(page, w_stream, True, depth_limit>0, depth_limit)


if __name__ == "__main__":
	try:
		struct_type = StructureType.PAGE
		parser = make_parser(struct_type)
		args = parser.parse_args()
		input_path, depth_limit, output_path\
			= process_arguments(args, struct_type)

	except ValueError as ve:
		print(ve)
		exit()

	reader = PdfFileReader(input_path.open(mode="rb"), strict=False)
	pages = reader.pages

	if output_path is None:
		from sys import stdout
		_write_page_objs_in_stream(input_path, pages, stdout, depth_limit)

	else:
		with output_path.open(mode="w", encoding="utf8") as output_stream:
			_write_page_objs_in_stream(input_path, pages,
				output_stream, depth_limit)
