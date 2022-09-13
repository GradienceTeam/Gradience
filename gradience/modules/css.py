import cssutils

COLORS = [
    "blue_",
    "green_",
    "yellow_",
    "orange_",
    "red_",
    "purple_",
    "brown_",
    "light_",
    "dark_",
]


def load_preset_from_css(path):
    css = ""
    variables = {}
    palette = {}

    for color in COLORS:
        palette[color] = {}

    with open(path, "r", encoding="utf-8") as f:
        sheet = cssutils.parseString(f.read())
        for rule in sheet:
            css_text = rule.cssText
            if rule.type == rule.UNKNOWN_RULE:
                if css_text.startswith("@define-color"):
                    name, color = css_text.split(" ", 1)[1].split(" ", 1)
                    for color_name in COLORS:
                        if name.startswith(color_name):
                            palette[name[:-1]][name[-1:]] = color[:-1]
                            break
                    else:
                        variables[name] = color[:-1]
                    print(f"{name} = {color}")
            elif rule.type == rule.STYLE_RULE:
                css += f"\n{rule.cssText}"
    return variables, palette, css


# if __name__ == "__main__":
#     load_preset_from_css("/home/user/.config/gtk-4.0/gtk.css")
