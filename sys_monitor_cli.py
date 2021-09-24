import click
from sys_monitor.utils._db_sqlite import SqliteDB
from sys_monitor._initial_sqlite import init_sqlite as _init_sqlite
from sys_monitor._update_monitor_value import update_monitor_value_sqlite
import time


@click.group()
def cli():
    pass


@cli.command()
@click.option("-d", "--database", "db_file", nargs=1, required=True,
              help="Please enter sqlite3 database file with it's full path.")
def init(db_file: str):
    if not db_file.endswith(".db"):
        db_file = f"{db_file}.db"

    click.echo(f"Power by HiSpatial GIS group.")
    click.echo(f"Start init database {db_file}.")
    try:
        # if database have been already inited, copy exists table and save name with _bak
        sqlite_handler = SqliteDB(db_file)
        click.echo("**** Step1 ****")

        # if get table success, copy table
        _back_up_table(sqlite_handler, "t_hs_sys_monitor")
        _back_up_table(sqlite_handler, "t_hs_hard_info")
        click.echo("**** Step2 ****")

        # init databse
        _init_sqlite(db_file)
        click.echo(f"Success init databse {db_file}, you can enter xxx to try save system info.")
    except BaseException as e:
        click.echo(f"Faild to init databse {db_file}, please connect with hispatial@alun.")
        click.echo(f"Error message {str(e)}")


@cli.command()
@click.option("-d", "--database", "db_file", nargs=1, required=True,
              help="Please enter sqlite3 database file with it's full path.")
@click.option("-l", "--loop", is_flag=True, required=False,
              help="Loop run until command stop.")
@click.option("-s", "--loopSecond", "second", nargs=1, required=False,
              help="The time(second) between twice collect.")
def run(db_file, loop, second):
    if loop:
        click.echo("Start loop collect system info, if you want to cancle, double press 'ctrl + c'.")
    while loop:
        _run(db_file, loop)
        try:
            second = int(second)
            time.sleep(second)
        except:
            time.sleep(30)
    _run(db_file, loop)


def _run(db_file, loop):
    if not db_file.endswith(".db"):
        db_file = f"{db_file}.db"

    try:
        if not loop:
            click.echo("Start collect system info.")

        update_monitor_value_sqlite(db_file)
        if not loop:
            click.echo("Success collect system info.")
    except BaseException as e:
        click.echo(f"Faild to init databse {db_file}, please connect with hispatial@alun.")
        click.echo(f"Error message {str(e)}")

    return None


def _back_up_table(sqlite_handler, table_name):
    # if get table success, copy table
    try:
        sqlite_handler.get_table(table_name)

        target_table = f"{table_name}_{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}"
        click.echo("Warning, database already inited. Avoid lose data,"
                   f" start back up table {table_name} to {target_table}")
        sqlite_handler.copy_table(table_name, target_table)
        click.echo(f"Back up {table_name} successful")
    except:
        pass

    return None


if __name__ == '__main__':
    cli()
