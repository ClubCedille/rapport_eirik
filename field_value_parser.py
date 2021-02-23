from pathlib import Path
from yaml import FullLoader, load


def parse_field_values(field_config_path):
	if type(field_config_path) is not Path:
		field_config_path = Path(field_config_path)

	with field_config_path.open() as config_stream:
		return load(config_stream, FullLoader)


def print_dictionary(d):
	for key, value in d.items():
		print(str(key) + ": " + str(value))


if __name__ == "__main__":
	print_dictionary(parse_field_values("field_filling.yml"))
