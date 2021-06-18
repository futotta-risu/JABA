import os.path


class FileManagerInterface:

    DIRECTORY = "data/tweets/{day}"

    def get_file_name(self, args: dict):
        pass

    def open_file(self, date):
        pass

    def save_file(self, data, date, status):
        pass


def file_exists(date_from):
    _, file_name, _ = get_file_names(date_from)

    return os.path.isfile(file_name)
