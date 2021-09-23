from sys_monitor.utils._db_sqlite import SqliteDB


def create_monitor_table():
    pass

def main(db_file, ):
    db = SqliteDB(db_file)
    fields = [
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


if __name__ == '__main__':
    main()
