import os

from glad.opener import URLOpener
from glad.spec import GLSpec


class OpenGLGenerator:
    def __init__(self):
        opener = URLOpener()

        self.spec = GLSpec.from_svn(opener)

        self.enums = {}

        for enum in self.spec.enums.values():
            val = int(enum.value, 0)
            if val not in self.enums:
                self.enums[val] = []

            self.enums[val].append(enum.name)

    def print_enums(self, file):
        file.write("def get_enum_map():\n")
        file.write("    return {\n")

        for key, value in self.enums.items():
            file.write("        {} : [{}],\n".format(str(key), ",".join("'" + x + "'" for x in value)))

        file.write("    }\n")


if __name__ == '__main__':
    generator = OpenGLGenerator()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "..", "enum_map.py"), "w") as f:
        generator.print_enums(f)

