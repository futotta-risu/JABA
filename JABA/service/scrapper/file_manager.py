import os.path


class FileManagerInterface:
    '''
        File management interface for data models
    '''


    DIRECTORY = "data/tweets/{day}"

    def get_file_name(self, args: dict):
        ''' Returns the file name of the data '''
        pass

    def open_file(self, args: dict):
        ''' Opens file and returns data '''
        pass

    def save_file(self, data, args: dict):
        ''' Saves the file of the data '''
        pass
