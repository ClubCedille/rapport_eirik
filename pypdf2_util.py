from PyPDF2 import PdfFileWriter
from PyPDF2.generic import BooleanObject,\
	IndirectObject, NameObject, TextStringObject


_KEY_ACROFORM = "/AcroForm"
_KEY_ANNOTS = "/Annots"
_KEY_AS = "/AS"
_KEY_KIDS = "/Kids"
_KEY_NEED_APPEARANCES = "/NeedAppearances"
_KEY_PARENT = "/Parent"
_KEY_T = "/T"
_KEY_V = "/V"

_TYPE_FIELD = "/FT"
_TYPE_BUTTON = "/Btn"
_TYPE_TEXT = "/Tx"


class RadioBtnGroup:
	"""
	This class contains the names of the radio buttons that make a radio
	button group in a PDF file. It also contains the name of the group, which
	should be the name of the field that corresponds to the group in the PDF
	file. The buttons' names can be accessed with an index between brackets.
	"""

	def __init__(self, group_name, *btn_names):
		"""
		The constructor needs this group's name followed by the buttons'
		names. At least one button name must be provided.

		Args:
			group_name (str): the name of this radio button group
			*btn_names: the names of the buttons in this group, as strings. At
				least one must be provided.

		Raises:
			ValueError: if no button name is provided
		"""
		if len(btn_names) < 1:
			raise ValueError("At least one button name must be provided.")

		self._name = group_name
		self._btn_names = btn_names

	def __getitem__(self, index):
		return self._btn_names[index]

	def has_index(self, index):
		"""
		Determines whether this group has the given index. If it does not,
		using that number as an index would raise an IndexError.

		Args:
			index (int): an integer that could be an index of this radio
				button group

		Returns:
			bool: True if this group has the given index, False otherwise
		"""
		size = len(self)
		return 0 <= index and index < size\
			or -size <= index and index <= -1

	def __iter__(self):
		self._iter_index = 0
		return self

	def __len__(self):
		return len(self._btn_names)

	@property
	def name(self):
		"""
		The name of this radio button group. It should be the name of the
		field that corresponds to the group in the PDF file.
		"""
		return self._name

	def __next__(self):
		if self._iter_index >= len(self):
			raise StopIteration()

		btn_name = self[self._iter_index]
		self._iter_index += 1
		return btn_name


def get_field_type(pdf_field):
	"""
	Determines the type of the given PDF field: text field (0), radio button
	group (1) or checkbox (2).

	Args:
		pdf_field (dict): a dictionary that represents a field of a PDF file

	Returns:
		int: the type of pdf_field of -1 if no type is determined
	"""
	type_val = pdf_field.get(_TYPE_FIELD)

	if type_val == _TYPE_TEXT:
		# Text field
		return 0

	elif type_val == _TYPE_BUTTON:
		if _KEY_KIDS in pdf_field:
			# Radio button group
			return 1

		else:
			# Checkbox
			return 2

	else:
		return -1


def _make_radio_btn_group_dict(radio_btn_groups):
	"""
	Creates a dictionary that associates each given radio button group with
	its name. The name is a property of class RadioBtnGroup.

	Args:
		radio_btn_groups: a list, set or tuple that contains instances of
			RadioBtnGroup

	Returns:
		dict: Its keys are the groups' names; its values are the groups.
	"""
	btn_groups = dict()

	for group in radio_btn_groups:
		btn_groups[group.name] = group

	return btn_groups


def make_writer_from_reader(pdf_reader, editable):
	"""
	Creates a PdfFileWriter instance from the content of a PdfFileReader
	instance. Depending on parameter editable, it will be possible to modify
	the fields of the file produced by the returned writer.

	Args:
		pdf_reader (PdfFileReader): an instance of PdfFileReader
		editable (bool): If True, the fields in the file created by the
			returned writer can be modified.

	Returns:
		PdfFileWriter: an instance that contains the pages of pdf_reader
	"""
	pdf_writer = PdfFileWriter()

	if editable:
		for page in pdf_reader.pages:
			pdf_writer.addPage(page)

	else:
		pdf_writer.cloneDocumentFromReader(pdf_reader)

	return pdf_writer


def set_need_appearances(pdf_writer, bool_val):
	"""
	Sets property _root_object["/AcroForm"]["/NeedAppearances"] of the given
	PdfFileWriter instance to a Boolean value. Setting it to True can be
	necessary to make visible the values in the fields of the file produced by
	pdf_writer.

	Args:
		bool_val (bool): the Boolean value to which /NeedAppearances will be
			set
	"""
	# https://stackoverflow.com/questions/47288578/pdf-form-filled-with-pypdf2-does-not-show-in-print
	catalog = pdf_writer._root_object

	# Get the AcroForm tree and add /NeedAppearances attribute
	if _KEY_ACROFORM not in catalog:
		pdf_writer._root_object.update({NameObject(_KEY_ACROFORM):
			IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})

	need_appearances = NameObject(_KEY_NEED_APPEARANCES)
	pdf_writer._root_object[_KEY_ACROFORM][need_appearances]\
		= BooleanObject(bool_val)


def update_page_fields(page, fields, *radio_btn_groups):
	"""
	Sets the fields in the given PdfFileWriter page to the values contained in
	argument fields. Every key in fields must be the name of a field in page.
	Text fields can be set to any object, which will be converted to a string.
	Checkboxes must be set to a string that represents their checked or
	unchecked state. For a radio button group, the value must be the index of
	the selected button. The index must correspond to a button name contained
	in the RadioBtnGroup instance in argument radio_btn_groups that bears the
	name of the group.

	Args:
		page (PyPDF2.pdf.PageObject): a page from a PdfFileWriter instance
		fields (dict): Its keys are field names; its values are the data to
			put in the fields.
		*radio_btn_groups: RadioBtnGroup instances that represent the radio
			button groups in page

	Raises:
		IndexError: if argument fields sets a radio button group to an
			incorrect index
	"""
	# This function is based on PdfFileWriter.updatePageFormFieldValues and an answer to this question:
	# https://stackoverflow.com/questions/35538851/how-to-check-uncheck-checkboxes-in-a-pdf-with-python-preferably-pypdf2
	if len(radio_btn_groups) > 0:
		radio_buttons = True
		btn_group_dict = _make_radio_btn_group_dict(radio_btn_groups)

	else:
		radio_buttons = False

	# Names of the set radio button groups
	radio_btn_grp_names = list()

	page_annots = page[_KEY_ANNOTS]

	for writer_annot in page_annots:
		writer_annot = writer_annot.getObject()
		annot_name = writer_annot.get(_KEY_T)
		field_type = get_field_type(writer_annot)

		# Set text fields and checkboxes
		if annot_name in fields:
			field_value = fields[annot_name]

			if field_type == 0: # Text field
				writer_annot.update({
					NameObject(_KEY_V): TextStringObject(field_value)
				})

			elif field_type == 2: # Checkbox
				writer_annot.update({
					NameObject(_KEY_AS): NameObject(field_value),
					NameObject(_KEY_V): NameObject(field_value)
				})

		# Set radio buttons
		elif radio_buttons and annot_name is None:
			annot_parent = writer_annot.get(_KEY_PARENT).getObject()

			if annot_parent is not None:
				annot_parent_name = annot_parent.get(_KEY_T).getObject()

				if annot_parent_name in fields\
						and annot_parent_name not in radio_btn_grp_names\
						and get_field_type(annot_parent) == 1:
					button_index = fields[annot_parent_name]
					button_group = btn_group_dict.get(annot_parent_name)

					if button_group is not None:
						if not button_group.has_index(button_index):
							raise IndexError(annot_parent_name
								+ " does not have index "
								+ str(button_index) + ".")

						button_name = button_group[button_index]

						annot_parent[NameObject(_KEY_KIDS)].getObject()\
							[button_index].getObject()[NameObject(_KEY_AS)]\
							= NameObject(button_name)

						annot_parent[NameObject(_KEY_V)]\
							= NameObject(button_name)

						radio_btn_grp_names.append(annot_parent_name)
