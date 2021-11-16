"""
This module uses library Jazal to check path arguments provided to other
modules of this repository.
"""


from jazal import\
	MissingPathArgWarner,\
	make_altered_name,\
	make_altered_path

from sys import exit


_ERROR_INTRO = "ERROR! "


def check_io_path_pair(input_path, input_path_name, input_path_exten,
		output_path, output_path_name, output_path_exten, dflt_output_termin):
	"""
	Performs verifications for a pair of path arguments provided to a script.
	The first one, the input path, points to a file from which the script
	extracts data. It is verified by function check_mandatory_path with
	must_exist set to True. The second path argument, the output path, is
	optional. It points to a file in which the script writes a result. It is
	verified by function check_optional_path. Argument input_path serves as the
	base for the default output path value.

	This function performs the following calls.

	check_mandatory_path(input_path, input_path_name, input_path_exten, True)

	check_optional_path(output_path, output_path_name,
		output_path_exten, input_path, dflt_output_termin)

	Read those functions' documentation to get the full information about the
	expected arguments.

	Args:
		input_path (pathlib.Path): the input path
		input_path_name (str): the input path argument's name
		input_path_exten (str): the extension that the input path is supposed
			to have
		output_path (pathlib.Path): the output path
		output_path_name (str): the output path argument's name
		output_path_exten (str): the extension that the output path is supposed
			to have
		dflt_output_termin (str): a string appended to input_path's file name
			to make a default output file name if necessary

	Returns:
		pathlib.Path: the output path, since it can be modified

	Raises:
		ValueError: if dflt_output_termin is None while output_path is None or
			points to a directory
	"""
	check_mandatory_path(input_path, input_path_name, input_path_exten, True)

	try:
		dflt_output_path = check_optional_path(
			output_path, output_path_name, output_path_exten,
			input_path, dflt_output_termin)

	except ValueError:
		raise ValueError(
			"If output_path is None or points to a directory, dflt_output_termin cannot be None.")

	return dflt_output_path


def check_mandatory_path(path_obj, path_arg_name, path_exten, must_exist):
	"""
	Performs verifications with library Jazal on a path argument that must be
	provided to a script. An error message is printed in the console and the
	script is interrupted if the path is omitted, if it points to an inexistent
	file while must_exist is True or if it has an incorrect extension.

	Args:
		path_obj (pathlib.Path): the path argument being checked. Set this
			parameter to None to indicate that the path was not provided.
		path_arg_name (str): the name of the path argument
		path_exten (str): the extension that path_obj is supposed to have. It
			must start with a '.'.
		must_exist (bool): If it is set to True, the existence of the file to
			which the path argument points is verified.
	"""
	missing_path_warner = MissingPathArgWarner(path_arg_name, path_exten)

	if path_obj is None:
		print(_ERROR_INTRO + missing_path_warner.make_missing_arg_msg())
		exit(1)

	try:
		path_checker =\
			missing_path_warner.make_reactive_path_checker(path_obj)

		if must_exist:
			path_checker.check_path_exists()

		path_checker.check_extension_correct()

	except Exception as e:
		print(_ERROR_INTRO + str(e))
		exit(1)


def check_optional_path(
		path_obj, path_arg_name, path_exten, base_path, termination):
	"""
	Performs verifications with library Jazal on a path argument that is
	optionally provided to a script. If it is omitted, a default value is
	generated from base_path and termination. If the path points to a
	directory, a default name is generated from base_path's file name and
	termination. If the path has an incorrect extension, an error message is
	printed in the console and the script is interrupted. If path_obj is not
	None and points to a file rather than a directory, base_path and
	termination are not required and can be None.

	Args:
		path_obj (pathlib.Path): the path argument being checked. Set this
			parameter to None to indicate that the path was not provided.
		path_arg_name (str): the name of the path argument
		path_exten (str): the extension that path_obj is supposed to have. It
			must start with a '.'.
		base_path (pathlib.Path): this path can serve as a base to generate a
			default value for the checked path.
		termination (str): a string appended to base_path's file name to make a
			default output file name if necessary

	Returns:
		pathlib.Path: the checked path, since it can be modified

	Raises:
		ValueError: if base_path or termination is None while path_obj is None
			or points to a directory
	"""
	path_provided = path_obj is not None
	path_is_dir = path_obj.is_dir() if path_provided else False

	if (base_path is None or termination is None)\
			and (not path_provided or path_is_dir):
		raise ValueError(
			"If path_obj is None or points to a directory, base_path and termination cannot be None.")

	missing_path_warner = MissingPathArgWarner(path_arg_name, path_exten)

	if path_provided:
		path_checker =\
			missing_path_warner.make_reactive_path_checker(path_obj)

		if path_is_dir:
			path_obj = path_obj/make_altered_name(
				base_path, after_stem=termination,
				extension=path_checker.extension_to_str())

		else:
			try:
				path_checker.check_extension_correct()

			except ValueError as e:
				print(_ERROR_INTRO + str(e))
				exit(1)

	else:
		path_obj = make_altered_path(
			base_path,
			after_stem=termination,
			extension=missing_path_warner.extension_to_str())

	return path_obj
