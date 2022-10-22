from gradience.commands import about
from gradience.commands import monet
from gradience.commands import apply_preset
from gradience.commands import plugins
from gradience.commands import presets
import click
import sys


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # UI
    if ctx.invoked_subcommand is None:
        from gradience import main

        sys.exit(main.main())


cli.add_command(apply_preset.apply_preset, "apply")
cli.add_command(monet.monet, "monet")
cli.add_command(about.about, "about")
cli.add_command(plugins.plugins, "plugins")
cli.add_command(presets.presets, "presets")
