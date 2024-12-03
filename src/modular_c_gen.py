import os

from src import _logging, _pycparser


def generate_boilercode(src_header_path, output_dir):
    # This function assumes that all input data is valid.
    # Data validation is in ../modular_c_gen.py
    logger = _logging.get_logger()
    logger.debug("Input file: %s", src_header_path)
    logger.debug("Output directory: %s", output_dir)
    logger.debug(f"Current working directory: {os.getcwd()}")

    c_file = _pycparser.parse_c_file(src_header_path)
