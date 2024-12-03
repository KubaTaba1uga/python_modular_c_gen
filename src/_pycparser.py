from dataclasses import dataclass
from typing import List

import pycparser


@dataclass
class CArg:
    name: str | None
    type: str


@dataclass
class CFuncDeclaration:
    name: str
    return_type: str
    args: CArg


@dataclass
class CFuncDefinition:
    name: str
    return_type: str
    args: CArg


@dataclass
class CFile:
    func_declarations: List[CFuncDeclaration]
    func_definitions: List[CFuncDefinition]


def parse_c_file(c_file_path) -> CFile:
    return _parse_c_ast(
        pycparser.parse_file(
            c_file_path,
            use_cpp=True,
            cpp_path="gcc",
            cpp_args=["-E", r"-Ibuild/pycparser/utils/fake_libc_include"],
        )
    )


def _parse_c_ast(c_ast):
    c_file = CFile([], [])

    field_name_is_type_map = {
        "func_declarations": lambda el: isinstance(el, pycparser.c_ast.Decl)
        and isinstance(el.type, pycparser.c_ast.FuncDecl),
        "func_definitions": lambda el: isinstance(el, pycparser.c_ast.FuncDef)
        and isinstance(el.decl.type, pycparser.c_ast.FuncDecl),
    }
    field_name_create_type_map = {
        "func_declarations": lambda el: CFuncDeclaration(
            name=el.name,
            return_type=" ".join(el.type.type.type.names),
            args=_create_c_func_args(el.type.args),
        ),
        "func_definitions": lambda el: CFuncDefinition(
            name=el.decl.name,
            return_type=" ".join(el.decl.type.type.type.names),
            args=_create_c_func_args(el.decl.type.args),
        ),
    }

    for field_name, is_func in field_name_is_type_map.items():
        for element in c_ast:
            if is_func(element):
                getattr(c_file, field_name).append(
                    field_name_create_type_map[field_name](element)
                )

    print(f"{c_file=}")


def _create_c_func_args(args):
    output = []

    for arg in args:
        output.append(_create_c_func_arg(arg))

    return output


# TO-DO use more recursion in _parse_c_ast, we can parse whole tree with recursion
def _create_c_func_arg(arg, name=None, is_ptr=False):
    if isinstance(arg, pycparser.c_ast.PtrDecl):
        is_ptr = True

    if getattr(arg, "type", None):
        if getattr(arg, "declname", None):
            name = arg.declname

        return _create_c_func_arg(arg.type, name=name, is_ptr=is_ptr)

    type = " ".join(arg.names)
    if is_ptr:
        type = f"{type} *"

    return CArg(name=name, type=type)
