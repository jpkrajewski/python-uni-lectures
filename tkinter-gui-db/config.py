from iniparser import IniReader


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.config = IniReader(self.filename)

    def read_config(self):
        return self.config.get_parsed_data()

    def get_param(self, param):
        return self.config.get(param)
