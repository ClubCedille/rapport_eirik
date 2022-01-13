"""
This script creates a PDF expense report for ÉTS clubs by copying a template
file and filling the copy's fields. The template is not modified.
"""


from argparse import ArgumentParser
from pathlib import Path
from sys import exit

from field_setting_parser import\
	get_yaml_content,\
	parse_yaml_content
from path_arg_checks import check_ungenerable_path
from PyPDF2 import PdfFileReader
from pypdf2_util import\
	make_writer_from_reader,\
	pdf_field_name_val_dict,\
	RadioBtnGroup,\
	set_need_appearances,\
	update_page_fields


_ADVANCE_FIELD = "Avance"
_CLAIM_FIELD = "Réclamation$"
_AMOUNT_FIELD = "Montant$"
_ccAMOUNT_FIELD = "ccMontant$"
_AMOUNT_TOTAL_FIELD = "TotalMontant"
_ccAMOUNT_TOTAL_FIELD = "TotalccMontant$"

_DFLT_TEMPLATE_PATH = Path(__file__).parents[0]/"rapport_depenses.pdf"

_EXTENSION_PDF = ".pdf"
_EXTENSION_YML = ".yml"

_NAME_CHOICE1 = "/Choix1"
_NAME_CHOICE2 = "/Choix2"

_NAME_GROUP1 = "Group1"
_NAME_GROUP2 = "Group2"
_NAME_GROUP4 = "Group4"


def _get_fields_from_pdf(pdf_data_path, radio_btn_group1, radio_btn_group2):
	pdf_data_source =\
		PdfFileReader(pdf_data_path.open(mode="rb"), strict=False)
	field_values = pdf_field_name_val_dict(pdf_data_source.getFields(), True)

	try:
		group1_index = radio_btn_group1.index(field_values.get(_NAME_GROUP1))
		field_values[_NAME_GROUP1] = group1_index
	except ValueError:
		pass

	try:
		group2_index = radio_btn_group2.index(field_values.get(_NAME_GROUP2))
		field_values[_NAME_GROUP2] = group2_index
	except ValueError:
		pass

	group4_index = _index_from_btn_group4(field_values.get(_NAME_GROUP4))
	if group4_index >= 0:
		field_values[_NAME_GROUP4] = group4_index

	return field_values


def _index_from_btn_group4(selected_btn):
	if selected_btn == "/D#E9p#F4t":
		return 0

	elif selected_btn == "/Ch#E8que":
		return 1

	else:
		return -1


def _make_parser():
	parser = ArgumentParser(description=__doc__)

	parser.add_argument("-e", "--editable", action="store_true",
		help="Makes the filled report editable.")

	parser.add_argument("-o", "--output", type=Path, default=None,
		help="Path to the filled PDF report created by this script")

	parser.add_argument("-p", "--pdf_data", type=Path, default=None,
		help="Path to the .pdf field setting file.")

	parser.add_argument("-t", "--template", type=Path,
		default=_DFLT_TEMPLATE_PATH,
		help="Path to the report template. It must be a PDF file.")

	parser.add_argument("-y", "--yml_data", type=Path, default=None,
		help="Path to the .yml field setting file.")

	return parser


def _set_automatic_field_vals(field_dict):
	_set_total_montant(field_dict, False)
	_set_reclamation(field_dict)
	_set_total_montant(field_dict, True)


def _set_reclamation(field_dict):
	reclamation = field_dict.get(_AMOUNT_TOTAL_FIELD, 0)\
		- field_dict.get(_ADVANCE_FIELD, 0)
	field_dict[_CLAIM_FIELD] = reclamation


def _set_total_montant(field_dict, cc):
	total_montant = 0

	if cc:
		loop_limit = 6
		amount_field = _ccAMOUNT_FIELD
		total_amount_field = _ccAMOUNT_TOTAL_FIELD

	else:
		loop_limit = 9
		amount_field = _AMOUNT_FIELD
		total_amount_field = _AMOUNT_TOTAL_FIELD

	for i in range(1, loop_limit):
		amount = field_dict.get(amount_field + str(i), 0)
		total_montant += amount

	if total_montant > 0:
		field_dict[total_amount_field] = total_montant


if __name__ == "__main__":
	parser = _make_parser()
	args = parser.parse_args()
	output_path = args.output # -o
	pdf_data_path = args.pdf_data # -p
	template_path = args.template # -t
	yml_data_path = args.yml_data # -y

	check_ungenerable_path(
		output_path, "-o/--output", _EXTENSION_PDF, must_exist=False)

	if pdf_data_path is not None:
		check_ungenerable_path(
			pdf_data_path, "-p/--pdf_data", _EXTENSION_PDF, must_exist=True)

	if template_path == _DFLT_TEMPLATE_PATH:
		if not template_path.exists():
			print("ERROR! Default report template "
				+ str(template_path) + " not found.")
			exit(1)
	else:
		check_ungenerable_path(
			template_path, "-t/--template", _EXTENSION_PDF, must_exist=True)

	check_ungenerable_path(
		yml_data_path, "-y/--yml_data", _EXTENSION_YML, must_exist=True)

	template = PdfFileReader(template_path.open(mode="rb"), strict=False)
	writer = make_writer_from_reader(template, args.editable)

	radio_btn_group1 = RadioBtnGroup(
		_NAME_GROUP1, _NAME_CHOICE1, _NAME_CHOICE2)
	radio_btn_group2 = RadioBtnGroup(
		_NAME_GROUP2, _NAME_CHOICE1, _NAME_CHOICE2)
	radio_btn_group4 = RadioBtnGroup(
		_NAME_GROUP4, "/Dépôt", "/Chèque")

	if pdf_data_path is None:
		field_values = dict()
	else:
		field_values = _get_fields_from_pdf(
			pdf_data_path, radio_btn_group1, radio_btn_group2)

	yaml_content = get_yaml_content(yml_data_path)
	yml_data = parse_yaml_content(yaml_content)
	_set_automatic_field_vals(yml_data)

	field_values.update(yml_data)

	page = writer.getPage(0)
	update_page_fields(page, field_values,
		radio_btn_group1, radio_btn_group2, radio_btn_group4)

	set_need_appearances(writer, True) # To make field values visible
	writer.write(output_path.open(mode="wb"))
