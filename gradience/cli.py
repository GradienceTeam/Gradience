from gradience.commands import about
from gradience.commands import monet
from gradience.commands import apply_preset
from gradience.commands import plugins
from gradience.commands import presets
import click
import click_completion
import sys

click_completion.init()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # UI
    if ctx.invoked_subcommand is None:
        from gradience import main

        sys.exit(main.main())

@click.group()
def completion():
    pass


@completion.command()
@click.option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion")
@click.argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells))
def show(shell, case_insensitive):
    """Show the click-completion-command completion code"""
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))


@completion.command()
@click.option('--append/--overwrite', help="Append the completion code to the file", default=None)
@click.option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion")
@click.argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells))
@click.argument('path', required=False)
def install(append, case_insensitive, shell, path):
    """Install the click-completion-command completion"""
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
    click.echo('%s completion installed in %s' % (shell, path))

cli.add_command(completion, "completion")

cli.add_command(apply_preset.apply_preset, "apply")
cli.add_command(monet.monet, "monet")
cli.add_command(about.about, "about")
cli.add_command(plugins.plugins, "plugins")
cli.add_command(presets.presets, "presets")
