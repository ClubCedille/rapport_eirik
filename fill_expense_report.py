from argparse import ArgumentParser
from field_setting import get_yaml_content, parse_yaml_content
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, RadioBtnGroup,\
	set_need_appearances, update_page_fields


parser = ArgumentParser(description=
	"This script creates a PDF expense report for ÉTS clubs by copying a\
	template file and filling the copy's fields. The template is not\
	modified.")

parser.add_argument("-e", "--editable", action="store_true",
	help="Makes the filled report editable.")

parser.add_argument("-o", "--output", type=Path, required=True,
	help="Path to the filled PDF report created by this script")

parser.add_argument("-s", "--setting", type=Path, required=True,
	help="Path to the field setting file. It must be a YAML file.")

parser.add_argument("-t", "--template", type=Path,
	default=Path("rapport_depenses.pdf"),
	help="Path to the report template. It must be a PDF file.")

args = parser.parse_args()


if __name__ == "__main__":
	template_path = args.template
	field_setting_path = args.setting
	output_path = args.output

	template = PdfFileReader(template_path.open(mode="rb"), strict=False)
	writer = make_writer_from_reader(template, args.editable)

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
