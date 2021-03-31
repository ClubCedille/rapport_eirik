from field_setting_parser import get_yaml_content, parse_yaml_content
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, set_need_appearances
from sys import argv, exit


if __name__ == "__main__":

	template_path = Path(argv[1])
	field_setting_path = Path(argv[2])
	output_path = Path(argv[3])

	report_template = PdfFileReader(template_path.open(mode="rb"))
	report_writer = make_writer_from_reader(report_template, False)

	yaml_content = get_yaml_content(field_setting_path)
	field_values = parse_yaml_content(yaml_content)

	page = report_writer.getPage(0)
	report_writer.updatePageFormFieldValues(page, field_values)

	set_need_appearances(report_writer, True) # To make field values visible
	report_writer.write(output_path.open(mode="wb"))
