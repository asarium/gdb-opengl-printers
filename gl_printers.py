import gdb
import gdb.printing
from gdb.printing import PrettyPrinter

import enum_map

cached_enum_map = None


def get_enum_map():
    global cached_enum_map

    if cached_enum_map is not None:
        return cached_enum_map

    cached_enum_map = enum_map.get_enum_map()
    return cached_enum_map


class GlEnumPrinter(PrettyPrinter):
    def __init__(self, val):
        super().__init__("GLenum")
        self.val = int(val)

    def to_string(self):
        map = get_enum_map()

        if self.val not in map:
            return str(self.val) + " (no associated enum name)"

        names = get_enum_map()[self.val]

        return ", ".join(names)


def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("OpenGL")
    pp.add_printer('GLenum', '^GLenum$', GlEnumPrinter)
    return pp


def add_gl_printers():
    # import pydevd as pydevd
    # pydevd.settrace('localhost', port=41879, stdoutToServer=True, stderrToServer=True)

    gdb.printing.register_pretty_printer(gdb.current_objfile(), build_pretty_printer())

