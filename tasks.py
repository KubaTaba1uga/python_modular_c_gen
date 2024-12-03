###############################################
#                Imports                      #
###############################################
import os
import subprocess

from invoke import task

###############################################
#                Constants                    #
###############################################
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(ROOT_PATH, "src")
BUILD_PATH = os.path.join(ROOT_PATH, "build")
REQUIREMENTS_FILE = os.path.join(ROOT_PATH, "app-requirements.txt")
PYC_PARSER_REPO = "https://github.com/eliben/pycparser.git"

###############################################
#                Public API                   #
###############################################


@task
def clean(c, bytecode=False, extra=""):
    """
    Clean up build and temporary files.

    This task removes the specified patterns of files and directories,
    including build artifacts, temporary files, and optionally Python
    bytecode files.

    Args:
        bytecode (bool, optional): If True, also removes Python bytecode files (.pyc). Defaults to False.
        extra (str, optional): Additional pattern to remove. Defaults to "".

    Usage:
        inv clean
        inv clean --bytecode
        inv clean --extra='**/*.log'
    """
    patterns = ["build", "**/*~", "**/#*", "*~", "#*", "**/*.stl"]

    if bytecode:
        patterns.append("**/*.pyc")
    if extra:
        patterns.append(extra)

    for pattern in patterns:
        _pr_info(f"Removing pattern {pattern}")
        c.run(f"rm -vrf {pattern}", warn=True)


@task
def build(c):
    """
    Build repo.

    Usage:
        inv build
    """
    raise NotImplementedError()


@task
def open(c):
    """
    Open repo.

    Usage:
        inv open
    """
    raise NotImplementedError()


@task
def install(c):
    """
    Install Python requirements from app-requirements.txt.

    Usage:
        inv install-requirements
    """
    if not os.path.exists(REQUIREMENTS_FILE):
        _pr_error(f"Requirements file not found: {REQUIREMENTS_FILE}")
        return

    _pr_info(f"Installing requirements from {REQUIREMENTS_FILE}")
    try:
        c.run(f"pip install -r {REQUIREMENTS_FILE}", pty=True)
    except Exception as e:
        _pr_error(f"Failed to install requirements: {str(e)}")

    fetch_pycparser(c)


def fetch_pycparser(c, release="v2.22"):
    """
    Clone the pycparser repository into the build directory and checkout a specific release.

    Args:
        release (str): The release version to checkout. Defaults to "v2.22".

    Usage:
        inv fetch-pycparser --release=v2.22
    """
    pycparser_dir = os.path.join(BUILD_PATH, "pycparser")

    # Ensure the build directory exists
    os.makedirs(BUILD_PATH, exist_ok=True)

    if os.path.exists(pycparser_dir):
        _pr_info(
            f"pycparser already exists in {pycparser_dir}. Fetching latest updates..."
        )
        try:
            with c.cd(pycparser_dir):
                c.run("git pull", pty=True)
        except Exception as e:
            _pr_error(f"Failed to fetch pycparser updates: {str(e)}")
            return
    else:
        _pr_info(f"Cloning pycparser into {BUILD_PATH}")
        try:
            c.run(f"git clone {PYC_PARSER_REPO} {pycparser_dir}", pty=True)
        except Exception as e:
            _pr_error(f"Failed to clone pycparser: {str(e)}")
            return

    # Checkout the specified release
    try:
        with c.cd(pycparser_dir):
            _pr_info(f"Checking out release {release}")
            c.run(f"git checkout release_{release}", pty=True)
    except Exception as e:
        _pr_error(f"Failed to checkout release {release}: {str(e)}")


###############################################
#                Private API                   #
###############################################
def _get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension


def _command_exists(command):
    try:
        # Attempt to run the command with '--version' or any other flag that doesn't change system state
        subprocess.run(
            [command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        # The command exists but returned an error
        return True
    except Exception:
        # Catch any other exceptions
        return False


def _cut_path_to_directory(full_path, target_directory):
    """
    Cuts the path up to the specified target directory.

    :param full_path: The full path to be cut.
    :param target_directory: The directory up to which the path should be cut.
    :return: The cut path if the target directory is found, otherwise raises ValueError.
    """
    parts = full_path.split(os.sep)

    target_index = parts.index(target_directory)
    return os.sep.join(parts[: target_index + 1])


def _pr_info(message: str):
    """
    Print an informational message in blue color.

    Args:
        message (str): The message to print.

    Usage:
        pr_info("This is an info message.")
    """
    print(f"\033[94m[INFO] {message}\033[0m")


def _pr_warn(message: str):
    """
    Print a warning message in yellow color.

    Args:
        message (str): The message to print.

    Usage:
        pr_warn("This is a warning message.")
    """
    print(f"\033[93m[WARN] {message}\033[0m")


def _pr_debug(message: str):
    """
    Print a debug message in cyan color.

    Args:
        message (str): The message to print.

    Usage:
        pr_debug("This is a debug message.")
    """
    print(f"\033[96m[DEBUG] {message}\033[0m")


def _pr_error(message: str):
    """
    Print an error message in red color.

    Args:
        message (str): The message to print.

    Usage:
        pr_error("This is an error message.")
    """
    print(f"\033[91m[ERROR] {message}\033[0m")
