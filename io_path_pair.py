from jazal import\
	MissingPathArgWarner,\
	make_altered_name,\
	make_altered_path


ERROR_INTRO = "ERROR! "


def check_io_path_pair(input_path, input_path_name, input_path_exten,
		output_path, output_path_name, output_path_exten, dflt_output_termin):
	# Input path checks
	missing_input_warner = MissingPathArgWarner(
		input_path_name, input_path_exten)

	if input_path is None:
		print(ERROR_INTRO + missing_input_warner.make_missing_arg_msg())
		exit()

	try:
		input_path_checker =\
			missing_input_warner.make_reactive_path_checker(input_path)
		input_path_checker.check_path_exists()
		input_path_checker.check_extension_correct()

	except Exception as e:
		print(ERROR_INTRO + str(e))
		exit()

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
			print(ERROR_INTRO + str(e))
			exit()

	return output_path
