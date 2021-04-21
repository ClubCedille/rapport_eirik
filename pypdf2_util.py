from PyPDF2 import PdfFileWriter
from PyPDF2.generic import BooleanObject,\
	IndirectObject, NameObject, TextStringObject


_FIELD_TYPE = "/FT"

_KIDS_KEY = "/Kids"

_BUTTON_TYPE = "/Btn"
_TEXT_TYPE = "/Tx"


class RadioBtnGroup:

	def __init__(self, group_name, *btn_names):
		if len(btn_names) < 1:
			raise ValueError("At least one button name must be provided.")

		self._name = group_name
		self._btn_names = btn_names

	def __getitem__(self, index):
		return self._btn_names[index]

	def has_index(self, index):
		return 0 <= index and index < self._size\
			or -self._size <= index and index <= -1

	def __iter__(self):
		self._iter_index = 0
		return self

	def __len__(self):
		return len(self._btn_names)

	@property
	def name(self):
		return self._name

	def __next__(self):
		if self._iter_index >= len(self):
			raise StopIteration()

		group = self[self._iter_index]
		self._iter_index += 1
		return group


def get_field_type(pdf_field):
	type_val = pdf_field.get(_FIELD_TYPE)

	if type_val == _TEXT_TYPE:
		# Text field
		return 0

	elif type_val == _BUTTON_TYPE:
		if _KIDS_KEY in pdf_field:
			# Radio button group
			return 1

		else:
			# Checkbox
			return 2

	else:
		return -1


def _make_radio_btn_group_dict(radio_btn_groups):
	btn_groups = dict()

	for group in radio_btn_groups:
		btn_groups[group.name] = group

	return btn_groups


def make_writer_from_reader(pdf_reader, editable):
	pdf_writer = PdfFileWriter()

	if editable:
		for page in pdf_reader.pages:
			pdf_writer.addPage(page)

	else:
		pdf_writer.cloneDocumentFromReader(pdf_reader)

	return pdf_writer


def set_need_appearances(pdf_writer, bool_val):
	# https://stackoverflow.com/questions/47288578/pdf-form-filled-with-pypdf2-does-not-show-in-print
	catalog = pdf_writer._root_object

	# Get the AcroForm tree and add /NeedAppearances attribute
	if "/AcroForm" not in catalog:
		pdf_writer._root_object.update({NameObject("/AcroForm"):
			IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})

	need_appearances = NameObject("/NeedAppearances")
	pdf_writer._root_object["/AcroForm"][need_appearances]\
		= BooleanObject(bool_val)


def update_page_fields(page, fields, *radio_btn_groups):
	# This function is based on PdfFileWriter.updatePageFormFieldValues and an answer to this question:
	# https://stackoverflow.com/questions/35538851/how-to-check-uncheck-checkboxes-in-a-pdf-with-python-preferably-pypdf2
	if len(radio_btn_groups) > 0:
		radio_buttons = True
		btn_group_dict = _make_radio_btn_group_dict(radio_btn_groups)

	else:
		radio_buttons = False

	# Names of the set radio button groups
	radio_btn_grp_names = list()

	page_annots = page["/Annots"]

	for j in range(0, len(page_annots)):
		writer_annot = page_annots[j].getObject()
		annot_name = writer_annot.get("/T")

		field_type = get_field_type(writer_annot)

		for field in fields:
			# Set text fields and checkboxes
			if annot_name == field:
				if field_type == 0: # Text field
					writer_annot.update({
                        NameObject("/V"): TextStringObject(fields[field])
                    })

				elif field_type == 2: # Checkbox
					writer_annot.update({
						NameObject("/V"): NameObject(fields[field]),
						NameObject("/AS"): NameObject(fields[field])
					})

			# Set radio buttons
			elif radio_buttons and annot_name is None:
				annot_parent = writer_annot.get("/Parent").getObject()

				if annot_parent is not None:
					annot_parent_name = annot_parent.get("/T").getObject()

					if annot_parent_name == field\
							and annot_parent_name not in radio_btn_grp_names\
							and get_field_type(annot_parent) == 1:
						button_index = fields[field]
						button_group = btn_group_dict.get(field)

						if button_group is not None:
							button_name = button_group[button_index]

							annot_parent[NameObject("/Kids")].getObject()\
								[button_index].getObject()[NameObject("/AS")]\
								= NameObject(button_name)

							annot_parent[NameObject("/V")]\
								= NameObject(button_name)

							radio_btn_grp_names.append(annot_parent_name)
