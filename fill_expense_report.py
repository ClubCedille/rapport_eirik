"""
This script creates a PDF file by copying a template file and filling the
copy's fields. The template is not modified.

Args:
	1: the path to the template. It must be a PDF file.
	2: the path to a YAML file that defines the information to put in the
		fields
	3: the path to the PDF file created by this script
"""


from field_setting import get_yaml_content, parse_yaml_content
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, RadioBtnGroup,\
	set_need_appearances, update_page_fields
from sys import argv


if __name__ == "__main__":

	template_path = Path(argv[1])
	field_setting_path = Path(argv[2])
	output_path = Path(argv[3])

	template = PdfFileReader(template_path.open(mode="rb"), strict=False)
	writer = make_writer_from_reader(template, False)

	yaml_content = get_yaml_content(field_setting_path)
	field_values = parse_yaml_content(yaml_content)

	radio_btn_group1 = RadioBtnGroup("Group1", "/Choix1", "/Choix2")
	radio_btn_group2 = RadioBtnGroup("Group2", "/Choix1", "/Choix2")
	radio_btn_group4 = RadioBtnGroup("Group4", "/Dépôt", "/Chèque")

	page = writer.getPage(0)
	update_page_fields(page, field_values,
		radio_btn_group1, radio_btn_group2, radio_btn_group4)

	set_need_appearances(writer, True) # To make field values visible
	writer.write(output_path.open(mode="wb"))
