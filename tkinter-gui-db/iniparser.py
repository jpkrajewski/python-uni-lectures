class IniReader:
    def __init__(self, file):
        self.__file_data = dict()
        self.__file = file

    def __read_file(self):
        try:
            ini_file = open(self.__file, "r")
            file_contents = ini_file.readlines()
            ini_file.close()
        except FileNotFoundError:
            exit("Input file not found.")

        return file_contents

    def __convert_to_type(self, value):
        value = str(value).replace("\"", "")
        value = value.strip()

        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            return float(value)
        else:
            return str(value)

    def __remove_quotes_and_comments(self, value):
        result = str(value).replace("\"", "").strip()

        if result.find("#") != -1:
            result = value[1:value.find("#")]

        if value.find(";") != -1:
            result = value[1:value.find(";")]

        return result

    # get only given element
    def get(self, key):
        key = str(key)

        file_contents = self.__read_file()
        name, value = "", ""

        for line in file_contents:
            if '=' in line:
                name, value = line.split('=', 1)  # split only once (ignore = in values)
            elif ':' in line:
                name, value = line.split(':')

            if name.strip() == key:
                return self.__remove_quotes_and_comments(value)

        return print("Key not found!")

    def __parse_file(self):
        value, name, section = "", "", ""
        file_contents = self.__read_file()

        # loop through each line in file
        for line in file_contents:
            if line.strip() == '':
                continue

            # check for comment line
            if line[0] == '#' or line[0] == ';':
                continue

            # check for new section
            elif line[0] == '[':
                index = line.index(']')
                section = line[1:index]
                self.__file_data[section] = dict()
            else:
                # read name:value pair
                if '=' in line:
                    name, value = line.split('=', 1)  # split only once (ignore = in values)
                elif ':' in line:
                    name, value = line.split(':', 1)

                value = self.__remove_quotes_and_comments(value)
                value = self.__convert_to_type(value)

                if '[]' in name:
                    arr = str(name).replace('[', '').replace(']', '').strip()

                    try:
                        self.__file_data[section][arr]  # check, if we can get to key (if not exists, it throws KeyError)
                    except KeyError:
                        self.__file_data[section][arr] = list()
                    finally:
                        self.__file_data[section][arr].append(value)
                    continue

                if section == '':
                    self.__file_data[name.strip()] = value
                else:
                    self.__file_data[section][name.strip()] = value

    def display_file(self):
        if not self.__file_data:
            self.__parse_file()

        file = self.__file_data
        print(file)

        for section in file:
            if type(file[section]) is dict:
                print('[' + str(section) + ']')
                for option in file[section]:
                    print(str(option) + ' = ' + str(file[section][option]))
                print()
            else:
                print(str(section) + ' = ' + str(file[section]))

    def get_parsed_data(self):
        if not self.__file_data:
            self.__parse_file()

        return self.__file_data
