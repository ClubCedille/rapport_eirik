"""
This script creates a PDF expense report for ÉTS clubs by copying a template
file and filling the copy's fields. The template is not modified.
"""


from argparse import ArgumentParser
from field_setting import\
	get_yaml_content,\
	parse_yaml_content
from path_arg_checks import\
	check_mandatory_path
from pathlib import Path
from PyPDF2 import PdfFileReader
from pypdf2_util import\
	make_writer_from_reader,\
	RadioBtnGroup,\
	set_need_appearances,\
	update_page_fields


_ADVANCE_FIELD = "Avance"
_CLAIM_FIELD = "Réclamation$"
_AMOUNT_FIELD = "Montant$"
_ccAMOUNT_FIELD = "ccMontant$"
_AMOUNT_TOTAL_FIELD = "TotalMontant"
_ccAMOUNT_TOTAL_FIELD = "TotalccMontant$"

_DFLT_TEMPLATE_PATH = Path("rapport_depenses.pdf")

_PDF_EXTEN_TUPLE = (".pdf",)


def _make_parser():
	parser = ArgumentParser(description=__doc__)

	parser.add_argument("-e", "--editable", action="store_true",
		help="Makes the filled report editable.")

	parser.add_argument("-o", "--output", type=Path, default=None,
		help="Path to the filled PDF report created by this script")

	parser.add_argument("-s", "--setting", type=Path, default=None,
		help="Path to the field setting file. It must be a YAML file.")

	parser.add_argument("-t", "--template", type=Path,
		default=_DFLT_TEMPLATE_PATH,
		help="Path to the report template. It must be a PDF file.")

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
	field_setting_path = args.setting # -s
	template_path = args.template # -t

	check_mandatory_path(
		output_path, "-o/--output", _PDF_EXTEN_TUPLE, must_exist=False)

	check_mandatory_path(
		field_setting_path, "-s/--setting", (".yml",), must_exist=True)

	if template_path != _DFLT_TEMPLATE_PATH:
		check_mandatory_path(
			template_path, "-t/--template", _PDF_EXTEN_TUPLE, must_exist=True)

	template = PdfFileReader(template_path.open(mode="rb"), strict=False)
	writer = make_writer_from_reader(template, args.editable)

	yaml_content = get_yaml_content(field_setting_path)
	field_values = parse_yaml_content(yaml_content)
	_set_automatic_field_vals(field_values)

	radio_btn_group1 = RadioBtnGroup("Group1", "/Choix1", "/Choix2")
	radio_btn_group2 = RadioBtnGroup("Group2", "/Choix1", "/Choix2")
	radio_btn_group4 = RadioBtnGroup("Group4", "/Dépôt", "/Chèque")

	page = writer.getPage(0)
	update_page_fields(page, field_values,
		radio_btn_group1, radio_btn_group2, radio_btn_group4)

	set_need_appearances(writer, True) # To make field values visible
	writer.write(output_path.open(mode="wb"))
