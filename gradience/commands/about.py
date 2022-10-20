import click

from gradience.about import version, COPYRIGHT


@click.command()
def about():
    print("Gradience version: " + version)
    print(COPYRIGHT)
