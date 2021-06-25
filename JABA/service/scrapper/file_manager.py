import os.path


class FileManagerInterface:

    DIRECTORY = "data/tweets/{day}"

    def get_file_name(self, args: dict):
        pass

    def open_file(self, args: dict):
        pass

    def save_file(self, data, args: dict):
        pass
