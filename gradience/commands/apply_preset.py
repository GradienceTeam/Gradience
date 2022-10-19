import click

@click.command()
@click.argument("preset", type=click.Path(exists=True), required=True)
def apply_preset(preset):
    print(preset)
