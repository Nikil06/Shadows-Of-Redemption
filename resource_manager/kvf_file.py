from typing import Literal
import os

KVF_FILE_EXT = ".kvf"

class File:
    def __init__(self, path):
        self.path = path

    def get_lines(self):
        with open(self.path, encoding='utf-8') as file:
            return file.readlines()

    def get_content(self):
        with open(self.path, encoding='utf-8')as file:
            return file.read()

class KVF_File(File):
    def __init__(self, path, delimiter="$$$ ", comment_marker="#", escape_prefix="/$"):

        if os.path.splitext(path)[1] != KVF_FILE_EXT:
            raise ValueError(f"given path is not a kvf file.\ngiven path:{path}")

        super().__init__(path)

        self.delimiter = delimiter
        self.comment_marker = comment_marker
        self.escape_prefix = escape_prefix

        self.sections = self._extract_sections()

    def _filter_lines(self):
        _lines = self.get_lines()
        filtered = []

        for line in _lines:
            if line.endswith('\n'):
                line = line[:-1]

            if line.startswith(self.comment_marker):
                pass
            elif line.startswith(self.escape_prefix + "n"):
                filtered.append("")
            elif line.strip() == "":
                pass
            else:
                filtered.append(line)

        return filtered

    def _extract_sections(self):
        lines = self._filter_lines()

        current_section = ''
        current_section_first_idx = None
        sections = {}

        delimiter_length = len(self.delimiter)

        for i, line in enumerate(lines):
            if line[: delimiter_length] == self.delimiter:
                if current_section:
                    sections[current_section] = "\n".join(lines[current_section_first_idx: i])
                current_section = line[delimiter_length:].strip()
                current_section_first_idx = i + 1

            if i == len(lines) - 1 and current_section_first_idx is not None:
                sections[current_section] = "\n".join(lines[current_section_first_idx:])

        return sections

    def get_sections(self, section_key, return_type: Literal['list', 'str'] = 'str'):
        if section_key not in self.sections:
            raise KeyError(f"\nKey : '{section_key}' is not defined in the kvf file."+
                           f"\nfile_path: {self.path}")
        if return_type == 'list':
            return self.sections[section_key].split('\n')
        elif return_type == 'str':
            return self.sections[section_key]
        else:
            raise TypeError("Invalid return_type. return_type can only be 'list' or 'str'.")
