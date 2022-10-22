import click

from gradience.modules.preset import Preset
from gradience.modules.manager import PresetManager

@click.group()
def presets():
    pass

@presets.command()
def update():
    """Update all the presets."""
    pm = PresetManager()
    pm.update_all()

@presets.command()
@click.argument("preset_name", type=str, required=True)
@click.argument("repo", type=str, required=True)
@click.option("--url", type=str, required=False)
def download(preset_name, repo, url):
    """Download a preset."""
    pm = PresetManager()
    pm.download(preset_name, repo, url)
