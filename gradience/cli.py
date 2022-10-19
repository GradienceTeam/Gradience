import click
import sys

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # UI
    if ctx.invoked_subcommand is None:
        from gradience import main
        sys.exit(main.main())


from gradience.commands import apply_preset
cli.add_command(apply_preset.apply_preset, "apply")
