from sys_monitor.utils._db_sqlite import SqliteDB
import click

config = {
    "sqlite": {
        "tables":
            {
                "t_hs_sys_monitor": [
                    {
                        "name": "time",
                        "type": "text"
                    },
                    {
                        "name": "cpu_use_avg",
                        "type": "float"
                    },
                    {
                        "name": "cpu_use_max",
                        "type": "float"
                    },
                    {
                        "name": "cpu_use_percore",
                        "type": "text"
                    },
                    {
                        "name": "mem_total",
                        "type": "float"
                    },
                    {
                        "name": "mem_use_size",
                        "type": "float"
                    },
                    {
                        "name": "mem_free",
                        "type": "float"
                    },
                    {
                        "name": "mem_use",
                        "type": "float"
                    },
                    {
                        "name": "swap_total",
                        "type": "float"
                    },
                    {
                        "name": "swap_use_size",
                        "type": "float"
                    },
                    {
                        "name": "swap_free",
                        "type": "float"
                    },
                    {
                        "name": "swap_use",
                        "type": "float"
                    },
                    {
                        "name": "unit",
                        "type": "text"
                    },
                    {
                        "name": "disk_io",
                        "type": "text"
                    }
                ],
                "t_hs_hard_info": [
                    {
                        "name": "time",
                        "type": "text"
                    },
                    {
                        "name": "cpu_physical",
                        "type": "integer"
                    },
                    {
                        "name": "cpu_logical",
                        "type": "integer"
                    },
                    {
                        "name": "mem_total",
                        "type": "float"
                    },
                    {
                        "name": "mem_use_size",
                        "type": "float"
                    },
                    {
                        "name": "mem_free",
                        "type": "float"
                    },
                    {
                        "name": "swap_total",
                        "type": "float"
                    },
                    {
                        "name": "swap_use_size",
                        "type": "float"
                    },
                    {
                        "name": "swap_free",
                        "type": "float"
                    },
                    {
                        "name": "disk_info",
                        "type": "text"
                    },
                    {
                        "name": "unit",
                        "type": "text"
                    }
                ]
            }
    },
    "postgresql": {},
    "mysql": {}
}


def init_sqlite(db_file):
    # get sqlite configs
    sqlite_config = config.get("sqlite")

    # init sqlite handler
    sqlite_handler = SqliteDB(db_file)

    # click.echo(f"Sqlite {sqlite_handler.cur}")
    # click.echo(f"Sqlite {type(sqlite_handler.cur)}")
    # click.echo(f"Sqlite {sqlite_handler.cur.__dict__}")

    # create tables
    for table_name, fields in sqlite_config.get("tables").items():
        sqlite_handler.create_table(table_name, fields)

    return sqlite_handler


if __name__ == '__main__':
    init_sqlite("D:/systemonitor/example.db")
