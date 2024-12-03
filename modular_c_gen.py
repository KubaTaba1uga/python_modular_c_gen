import argparse

from src import modular_c_gen
from src._logging import configure_logger


def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Automatically generate modularization boilerplate code for C."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the source header file."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="build",
        help="Directory where the boilerplate code will be saved. Defaults to 'build'.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    print("Start")
    if args.verbose:
        configure_logger("modular_c_gen", level="DEBUG")
        print("Debug")
    else:
        print("Write")
        configure_logger("modular_c_gen", level="INPUT")

    modular_c_gen.generate_boilercode(args.input, args.output)


if __name__ == "__main__":
    main()
