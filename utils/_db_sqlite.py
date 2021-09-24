import sqlite3

import click

from sys_monitor.utils._file_process import FileProcessor


# from functools import cached_property


class SqliteDB:
    # table type
    class Table:
        # field type
        class Field:
            def __init__(self, name, type, primary=False, notnull=False, autoincrement=False, default=None):
                self.name = name
                self.type = type
                self.primary = primary
                self.notnull = notnull
                self.autoincrement = autoincrement
                self.default = default

            def __str__(self):
                return self.name

        def __init__(self, name, fields):
            """

            :param name:
            :param fields: tuple of list, like [("name", "zs"), ("age", 18)]
            """
            self.name = name
            # print("table name: ", self.name)
            # print("table name: ", type(self.name))
            # save all fields
            self.fields = [each.__str__() for each in fields]
            self.fields_ori = [each for each in fields]
            # set each field to a single attribute
            self.set_field()

        def add_column(self, column_name: str, field_type: str, primary_key: bool = False, not_null: bool = False,
                       auto_increment: bool = False) -> object:
            # column parameter available check
            self._vali_column_para(column_name, field_type, primary_key, not_null, auto_increment)

            if not not_null:
                not_null = ""

            if not auto_increment:
                auto_increment = ""

            if not primary_key:
                primary_key = ""
                sql = f"ALTER TABLE {self.name} ADD COLUMN {column_name} {field_type} {not_null}"
            else:
                primary_key = "PRIMARY KEY"
                sql = f"ALTER TABLE {self.name} ADD COLUMN {column_name} {field_type} {primary_key} {auto_increment}"

            # execute sql
            SqliteDB.instance.cur.execute(sql)
            SqliteDB.instance.conn.commit()

            self.fields.append({"name": column_name, "type": field_type})

            return self

        def _vali_column_para(self, name, field_type, primary_key, not_null, auto_increment):
            name_key_word = ()

            # field name check
            assert isinstance(name, str) and name.strip() != "" and name not in name_key_word, \
                "(Field Error) Field name is not available."

            # field type check
            assert isinstance(field_type,
                              str) and field_type.strip() != "", "(Field Error) Field type is not available."

            # # field length check
            # if field_length:
            #     assert isinstance(field_length, (str, int)), "(Field Error) Field length is not available."
            #     try:
            #         int(field_length)
            #     except:
            #         raise ValueError("(Field Error) Field length is not available.")
            #
            # # field precision check
            # if field_precision:
            #     assert isinstance(field_precision, (str, int)), "(Field Error) Field precision is not available."
            #     try:
            #         int(field_precision)
            #     except:
            #         raise ValueError("(Field Error) Field precision is not available.")

            # primary_key check
            assert isinstance(primary_key, bool)
            # not null
            assert isinstance(not_null, bool)
            # auto increment
            assert isinstance(auto_increment, bool)

        def insert(self, fields, values):
            # field structure match
            assert set(fields).issubset(set(self.fields)), "(Error) Field not match."
            # field count and value count match
            assert fields.__len__() == values.__len__(), "(Error) Field count not match"

            SqliteDB.instance.cur.execute(f"INSERT INTO {self.name}{tuple(fields)} VALUES{tuple(values)}")
            SqliteDB.instance.conn.commit()

            return self

        def set_field(self):
            for field in self.fields_ori:
                self.__dict__[f"field_{field.__str__()}"] = field

            return self

        def __str__(self):
            return self.name

    def __init__(self, sqlite_db_file):
        self.file_handler = FileProcessor(sqlite_db_file)

        self.conn = self.conn()
        self.cur = self.conn.cursor()

        SqliteDB.instance = self

        self.tables = []

    # @cached_property
    # @property
    def conn(self):
        # create sqlite db
        if not self.file_handler.exists:
            # create folders
            self.file_handler.create_pre_folder()

        conn = sqlite3.connect(self.file_handler.file)

        return conn

    # @cached_property
    # @property
    def cur(self):
        return self.conn.cursor()

    # todo field validity test
    def create_table(self, table_name: str, fields_info: list):
        """

        :param table_name: str
        :param fields_info: list of some dict, like this
                            [{
                                "name": "example",
                                "type": "text",
                                "primary": False,       # (option)
                                "nullable": True,       # (option)
                                "autoincrement": False, # (option)
                                "default": "0"          # (option, if nullable this is must)
                            },
                            { ... }, ...
                            ]
        :return:
        """
        fields_sql = ""
        fields = []
        for field in fields_info:
            field_name, field_type, primary_key, nullable, autoincrement, default = field.get("name"), field.get(
                "type"), field.get("primary"), field.get("nullable"), field.get("autoincrement"), field.get("default")

            # class Table.Field's instance
            field_obj = SqliteDB.Table.Field(field_name, field_type, bool(primary_key),
                                             bool(nullable), bool(autoincrement), default)

            # only when filed type is INTEGER and primary autoincrement is available
            if field_type.upper() == "INTEGER" and primary_key and autoincrement:
                autoincrement = "AUTOINCREMENT"
            else:
                autoincrement = ""

            # primary is False and nullable is True
            if not primary_key and nullable:
                # have default parameters
                if default:
                    nullable = f"NOT NULL DEFAULT {default}"
                else:
                    nullable = "NOT NULL DEFAULT 0"
            else:
                nullable = ""

            if primary_key:
                primary_key = "PRIMARY KEY"
            else:
                primary_key = ""

            field_sql = f"{field_name} {field_type} {primary_key} {nullable} {autoincrement}, "
            fields_sql += field_sql
            fields.append(field_obj)

        self.cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        self.cur.execute(f"CREATE TABLE {table_name}({fields_sql[:-2]});")
        self.conn.commit()

        # class Table's instance
        table = SqliteDB.Table(table_name, fields)
        self.tables.append(table)

        return table

    def get_table(self, table_name):
        # get table structure
        fields_info = self.cur.execute(f"PRAGMA table_info({table_name})").fetchall()

        assert fields_info.__len__() > 0, f"(Error) Get table '{table_name}' failed"
        # get fields obj
        fields = self._field_info_parse(fields_info)

        # get table obj
        table = SqliteDB.Table(table_name, fields)

        return table

    def copy_table(self, origin_table_name, target_table_name):
        # make sure origin table is exists
        assert self.get_table(origin_table_name), f"(Error) Table '{origin_table_name}' is not exists"

        self.cur.execute(f"DROP TABLE IF EXISTS {target_table_name}")
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {target_table_name} AS SELECT * FROM {origin_table_name}")
        self.conn.commit()

        return self.get_table(target_table_name)

    def _field_info_parse(self, field_info):
        fields = []
        for field in field_info:
            field_cid, field_name, field_type, field_notnull, field_dflt_value, field_pk = field

            field_obj = SqliteDB.Table.Field(field_name, field_type, bool(field_pk),
                                             bool(field_notnull), bool(field_dflt_value))
            fields.append(field_obj)

        return fields


if __name__ == '__main__':
    # usage
    # connect sqlite db
    db = SqliteDB("./db/example.db")

    # create table
    fields = [
        {
            "name": "id",
            "type": "integer",
            "primary": True,
            "autoincrement": True
        },
        {
            "name": "name",
            "type": "text",
        },
        {
            "name": "age",
            "type": "integer",
        },
        {
            "name": "sal",
            "type": "real",
        },
    ]

    # table = db.create_table("test2", fields)

    # get exists table
    table = db.get_table("test3")

    # insert values
    table.insert(["name", "age", "sal"], ["张三", 18, 3500])
    table.insert(["name", "age", "sal"], ["张三", 18, 3500])
    table.insert(["name", "age", "sal"], ["张三", 18, 3500])
    table.insert(["name", "age", "sal"], ["张三", 18, 3500])
    table.insert(["name", "age", "sal"], ["张三", 18, 3500])
