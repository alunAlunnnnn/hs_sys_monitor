import click


@click.group(invoke_without_command=False)
def cli():
    pass


@cli.group()
def lunch():
    pass


@cli.group()
def dinner():
    pass


@click.command()
@click.option("-n", "--name", help="Please enter you name")
def burger(name):
    print(f"{name}, please enjoy your burger")


# @click.command()
# def burger():
#     print(f"please enjoy your burger")


lunch.add_command(burger)
dinner.add_command(burger)

if __name__ == '__main__':
    cli()
