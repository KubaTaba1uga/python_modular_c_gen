import os

from src._logging import get_logger
from src._pycparser import generate_ast


def generate_boilercode(src_header_path, output_dir):
    # This function assumes that all input data is valid.
    # Data validation is in ../modular_c_gen.py
    logger = get_logger()
    logger.debug("Input file: %s", src_header_path)
    logger.debug("Output directory: %s", output_dir)
    logger.debug(f"Current working directory: {os.getcwd()}")
    # with open(src_header_path) as fp:
    #     src_header_content = fp.read()

    c_code_ast = generate_ast(src_header_path)

    c_code_ast.show()
    # print(c_code_ast)
