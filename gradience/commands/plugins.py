import click

from gradience.modules.preset import Preset
from gradience.modules.plugins.manager import setup_pm


@click.group()
def plugins():
    pass


PLUGIN_MANAGER = None


@plugins.command()
def check():
    global PLUGIN_MANAGER
    PLUGIN_MANAGER = setup_pm()
