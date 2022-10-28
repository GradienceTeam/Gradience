import click

from gradience.modules.preset import Preset, OldPreset, DarkPreset, LightPreset
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

@presets.command()
@click.argument("preset_name", type=str, required=True)
@click.argument("repo", type=str, required=True)
def port(preset_name, repo):
    """Port the old preset to the new preset format."""
    old = OldPreset(preset_name, repo)
    new = old.port()
    new.save()

@presets.command()
@click.argument("dark", type=click.Path(exists=True), required=True)
@click.argument("light", type=click.Path(exists=True), required=True)
@click.argument("name", type=str, required=True)
@click.argument("repo", type=str, required=True)
def merge(dark, light, name, repo):
    """Merge two presets."""
    light = LightPreset(preset_path=light)
    dark = DarkPreset(preset_path=dark)
    merged = Preset(name=name, repo=repo, dark=dark, light=light)
    merged.save()

@presets.command()
def list():
    """List all the presets."""
    pm = PresetManager()
    for repo in pm.presets:
        for preset in pm.presets[repo]:
            print(preset)
