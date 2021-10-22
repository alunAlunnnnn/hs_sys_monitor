import os
from functools import cached_property


class FileProcessor:
    def __init__(self, file):
        if not os.path.isabs(file):
            file = os.path.abspath(file)
        self.file = file

    @property
    def exists(self):
        return True if os.path.exists(self.file) else False

    @property
    def type(self):
        if self.exists:
            if os.path.isfile(self.file):
                return "file"
            elif os.path.isdir(self.file):
                return "folder"
            else:
                return "unknown"
        return None

    @cached_property
    def dirname(self):
        return os.path.dirname(self.file)

    @cached_property
    def basename(self):
        return os.path.basename(self.file)

    @property
    def pre_folder_exist(self):
        return True if os.path.exists(self.dirname) else False

    def create_pre_folder(self):
        if not self.pre_folder_exist:
            os.makedirs(self.dirname)

        return self.pre_folder_exist

    def create_folder(self):
        if not os.path.exists(self.file):
            os.makedirs(self.file)

        return self.exists


if __name__ == '__main__':
    file_handler = FileProcessor("./test/test/test.txt")
    print("file: ", file_handler.file)
    print("exists: ", file_handler.exists)
    print("type: ", file_handler.type)
    print("dirname: ", file_handler.dirname)
    print("basename: ", file_handler.basename)
    # print("create_folder(): ", file_handler.create_folder())
    print("exists: ", file_handler.exists)
    print("pre_folder_exist: ", file_handler.pre_folder_exist)
    print("create_pre_folder: ", file_handler.create_pre_folder())
    print("pre_folder_exist: ", file_handler.pre_folder_exist)
