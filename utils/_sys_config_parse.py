import os
import configparser
import json


def _sys_config_parse(config_ini):
    # get config init file
    config_ini = os.path.abspath(config_ini)

    # init config parser
    parser = configparser.ConfigParser()

    # read .ini file
    parser.read_file(config_ini)

    #




def _table_structure_parse(table_struc_json):
    with open(table_struc_json, "r", encoding="utf-8") as f:
        table_struc = json.loads(f.read())

    print(table_struc)


def main():
    _sys_config_parse()
    _table_structure_parse(table_structure_json)

sys_config_ini = "../config/sys_config.ini"
table_structure_json = "../config/table_structure.json"

if __name__ == '__main__':
    main()


