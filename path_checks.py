"""
This module uses library Jazal to check path arguments provided to other
modules of this repository.
"""


from jazal import\
	MissingPathArgWarner,\
	make_altered_name,\
	make_altered_path


_ERROR_INTRO = "ERROR! "


def check_io_path_pair(input_path, input_path_name, input_path_exten,
		output_path, output_path_name, output_path_exten, dflt_output_termin):
	"""
	Performs verifications for a pair of path arguments provided to a script.
	The first one, the input path, points to a file from which the script
	extracts data. It is verified by function check_mandatory_path. The second
	path argument, the output path, is optional. If it is not provided, a
	default value is generated from input_path and dflt_output_termin. If the
	output path points to a directory, a default name is generated from
	input_path's file name. If the output path as an incorrect extension, an
	error message is printed in the console and the script is interrupted.

	The first three arguments are given to function check_mandatory_path. Read
	its documentation to get the full information about them. The next three
	arguments are the same, but applied to the output path.

	Args:
		input_path (pathlib.Path): the input path
		input_path_name (str): the input path argument's name
		input_path_exten (str tuple): the input path's extension
		output_path (pathlib.Path): the output path
		output_path_name (str): the output path argument's name
		output_path_exten (str tuple): the output path's extension
		dflt_output_termin (str): a string appended to input_path's file name
			to make a default output file name if necessary

	Returns:
		pathlib.Path: the output path, since it can have been modified
	"""
	check_mandatory_path(input_path, input_path_name, input_path_exten)

	# Output path checks
	missing_output_warner = MissingPathArgWarner(
		output_path_name, output_path_exten)

	if output_path is None:
		output_path = make_altered_path(
			input_path,
			after_stem=dflt_output_termin,
			extension=missing_output_warner.extension_to_str())

	output_path_checker =\
		missing_output_warner.make_reactive_path_checker(output_path)

	if output_path_checker.path_is_dir():
		output_path = output_path/make_altered_name(
			input_path, after_stem=dflt_output_termin,
			extension=output_path_checker.extension_to_str())

	else:
		try:
			output_path_checker.check_extension_correct()

		except Exception as e:
			print(_ERROR_INTRO + str(e))
			exit()

	return output_path


def check_mandatory_path(path_obj, path_arg_name, path_exten):
	"""
	Performs verifications for a path argument that must be provided to a
	script. An error message is printed in the console and the script is
	interrupted if the path is not given, if it points to an inexistent file
	of if has an incorrect extension.

	Args:
		path_obj (pathlib.Path): the path argument being checked. Set this
			parameter to None to indicated that the path was not provided.
		path_arg_name (str): the name of the path argument
		path_exten (str tuple): the extension that path_obj is supposed to
			have. It must conform to the specification of the Jazal library.
	"""
	missing_path_warner = MissingPathArgWarner(
		path_arg_name, path_exten)

	if path_obj is None:
		print(_ERROR_INTRO + missing_path_warner.make_missing_arg_msg())
		exit()

	try:
		path_checker =\
			missing_path_warner.make_reactive_path_checker(path_obj)
		path_checker.check_path_exists()
		path_checker.check_extension_correct()

	except Exception as e:
		print(_ERROR_INTRO + str(e))
		exit()
