from email.policy import default
import click
import os


from gradience.modules.preset import Preset
from gradience.modules.themes import Theme


@click.command()
@click.argument("background", type=click.Path(exists=True), required=True)
@click.option("--name", type=str, default="monet")
def monet(background: click.Path, name, tone):
    preset = Preset.new_from_background(background, name)
    theme = Theme(preset.name, preset)
    theme.create()
