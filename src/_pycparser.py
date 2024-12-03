import pycparser


def generate_ast(c_file_path):
    return pycparser.parse_file(
        c_file_path,
        use_cpp=True,
        cpp_path="gcc",
        cpp_args=["-E", r"-Ibuild/pycparser/utils/fake_libc_include"],
    )
