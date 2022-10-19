from email.policy import default
import click
import os

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from material_color_utilities_python import *

from gradience.modules.preset import Preset
from gradience.modules.themes import Theme


def rgba_from_argb(argb, alpha=None) -> str:
    base = "rgba({}, {}, {}, {})"

    red = redFromArgb(argb)
    green = greenFromArgb(argb)
    blue = blueFromArgb(argb)
    if not alpha:
        alpha = alphaFromArgb(argb)

    return base.format(red, green, blue, alpha)


@click.command()
@click.argument("background", type=click.Path(exists=True), required=True)
@click.option("--name", type=str, default="monet")
@click.option("--tone", type=click.INT, default=30)
def monet(background: click.Path, name, tone):
    if str(background).endswith(".svg"):
        drawing = svg2rlg(background)
        background = os.path.join(
            os.environ.get("XDG_RUNTIME_DIR"), "gradience_bg.png"
        )
        renderPM.drawToFile(drawing, background, fmt="PNG")

    if background.endswith(".xml"):
        click.echo("XML is not supported yet")
    else:

        try:
            monet_img = Image.open(background)
        except Exception:
            click.echo("Unsupported background type", err=True)
        else:
            basewidth = 64
            wpercent = basewidth / float(monet_img.size[0])
            hsize = int((float(monet_img.size[1]) * float(wpercent)))
            monet_img = monet_img.resize(
                (basewidth, hsize), Image.Resampling.LANCZOS
            )
            theme = themeFromImage(monet_img)

            # palettes = theme["palettes"]

            # palette = {}
            # i = 0
            # for color in palettes.values():
            #     i += 1
            #     palette[str(i)] = hexFromArgb(color.tone(tone))

            # print(palette)
            palette = {

                "blue_": {
                    "1": "#99c1f1",
                    "2": "#62a0ea",
                    "3": "#3584e4",
                    "4": "#1c71d8",
                    "5": "#1a5fb4"
                },
                "green_": {
                    "1": "#8ff0a4",
                    "2": "#57e389",
                    "3": "#33d17a",
                    "4": "#2ec27e",
                    "5": "#26a269"
                },
                "yellow_": {
                    "1": "#f9f06b",
                    "2": "#f8e45c",
                    "3": "#f6d32d",
                    "4": "#f5c211",
                    "5": "#e5a50a"
                },
                "orange_": {
                    "1": "#ffbe6f",
                    "2": "#ffa348",
                    "3": "#ff7800",
                    "4": "#e66100",
                    "5": "#c64600"
                },
                "red_": {
                    "1": "#f66151",
                    "2": "#ed333b",
                    "3": "#e01b24",
                    "4": "#c01c28",
                    "5": "#a51d2d"
                },
                "purple_": {
                    "1": "#dc8add",
                    "2": "#c061cb",
                    "3": "#9141ac",
                    "4": "#813d9c",
                    "5": "#613583"
                },
                "brown_": {
                    "1": "#cdab8f",
                    "2": "#b5835a",
                    "3": "#986a44",
                    "4": "#865e3c",
                    "5": "#63452c"
                },
                "light_": {
                    "1": "#ffffff",
                    "2": "#f6f5f4",
                    "3": "#deddda",
                    "4": "#c0bfbc",
                    "5": "#9a9996"
                },
                "dark_": {
                    "1": "#77767b",
                    "2": "#5e5c64",
                    "3": "#3d3846",
                    "4": "#241f31",
                    "5": "#000000"
                }
            }
            dark_theme = theme["schemes"]["dark"]
            dark_variable = {
                "accent_color": rgba_from_argb(dark_theme.primary),
                "accent_bg_color": rgba_from_argb(dark_theme.primaryContainer),
                "accent_fg_color": rgba_from_argb(dark_theme.onPrimaryContainer),
                "destructive_color": rgba_from_argb(dark_theme.error),
                "destructive_bg_color": rgba_from_argb(dark_theme.errorContainer),
                "destructive_fg_color": rgba_from_argb(
                    dark_theme.onErrorContainer
                ),
                "success_color": rgba_from_argb(dark_theme.tertiary),
                "success_bg_color": rgba_from_argb(dark_theme.onTertiary),
                "success_fg_color": rgba_from_argb(dark_theme.onTertiaryContainer),
                "warning_color": rgba_from_argb(dark_theme.secondary),
                "warning_bg_color": rgba_from_argb(dark_theme.onSecondary),
                "warning_fg_color": rgba_from_argb(dark_theme.primary, "0.8"),
                "error_color": rgba_from_argb(dark_theme.error),
                "error_bg_color": rgba_from_argb(dark_theme.errorContainer),
                "error_fg_color": rgba_from_argb(dark_theme.onError),
                "window_bg_color": rgba_from_argb(dark_theme.surface),
                "window_fg_color": rgba_from_argb(dark_theme.onSurface),
                "view_bg_color": rgba_from_argb(dark_theme.surface),
                "view_fg_color": rgba_from_argb(dark_theme.onSurface),
                "headerbar_bg_color": rgba_from_argb(dark_theme.surface),
                "headerbar_fg_color": rgba_from_argb(dark_theme.onSurface),
                "headerbar_border_color": rgba_from_argb(
                    dark_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": rgba_from_argb(dark_theme.shadow),
                "card_bg_color": rgba_from_argb(dark_theme.primary, "0.05"),
                "card_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                "card_shade_color": rgba_from_argb(dark_theme.shadow),
                "dialog_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                "dialog_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                "popover_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                "popover_fg_color": rgba_from_argb(
                    dark_theme.onSecondaryContainer
                ),
                "shade_color": rgba_from_argb(dark_theme.shadow),
                "scrollbar_outline_color": rgba_from_argb(dark_theme.outline),
            }
            light_theme = theme["schemes"]["light"]
            light_variable = {
                "accent_color": rgba_from_argb(light_theme.primary),
                "accent_bg_color": rgba_from_argb(light_theme.primary),
                "accent_fg_color": rgba_from_argb(light_theme.onPrimary),
                "destructive_color": rgba_from_argb(light_theme.error),
                "destructive_bg_color": rgba_from_argb(light_theme.errorContainer),
                "destructive_fg_color": rgba_from_argb(
                    light_theme.onErrorContainer
                ),
                "success_color": rgba_from_argb(light_theme.tertiary),
                "success_bg_color": rgba_from_argb(light_theme.tertiaryContainer),
                "success_fg_color": rgba_from_argb(
                    light_theme.onTertiaryContainer
                ),
                "warning_color": rgba_from_argb(light_theme.secondary),
                "warning_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "warning_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "error_color": rgba_from_argb(light_theme.error),
                "error_bg_color": rgba_from_argb(light_theme.errorContainer),
                "error_fg_color": rgba_from_argb(light_theme.onError),
                "window_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "window_fg_color": rgba_from_argb(light_theme.onSurface),
                "view_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "view_fg_color": rgba_from_argb(light_theme.onSurface),
                "headerbar_bg_color": rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "headerbar_fg_color": rgba_from_argb(light_theme.onSurface),
                "headerbar_border_color": rgba_from_argb(
                    light_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "card_bg_color": rgba_from_argb(light_theme.primary, "0.05"),
                "card_fg_color": rgba_from_argb(light_theme.onSecondaryContainer),
                "card_shade_color": rgba_from_argb(light_theme.shadow),
                "dialog_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "dialog_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "popover_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "popover_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "shade_color": rgba_from_argb(light_theme.shadow),
                "scrollbar_outline_color": rgba_from_argb(light_theme.outline),
            }

            dark_preset = {
                "palette": palette,
                "variables": dark_variable,
                "custom_css": {
                    "gtk3": "",
                    "gtk4": "",
                }
            }

            light_preset = {
                "palette": palette,
                "variables": light_variable,
                "custom_css": {
                    "gtk3": "",
                    "gtk4": "",
                }
            }

            preset = Preset(name, dark=dark_preset, light=light_preset)
            theme = Theme(preset.name, preset)
            theme.create()
