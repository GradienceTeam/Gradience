from ..settings_schema import settings_schema
import json
import os

from .utils import buglog, to_slug_case

PRESET_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
    "presets",
)


class Preset:
    variables = {}
    palette = {}
    custom_css = {
        "gtk4": "",
        "gtk3": "",
    }
    plugins = {}
    repo = "user"
    name = "new_preset"
    badges = {}

    def __init__(self, name=None, repo=None, preset_path=None, text=None, preset=None):
        if text:  # load from ressource
            self.load_preset(text=text)
        elif preset:  # css or dict
            self.load_preset(preset=preset)
        else:
            self.preset_name = name
            if name is not None:
                self.name = to_slug_case(name)
            if repo is not None:
                self.repo = repo
            if preset_path is None:
                self.preset_path = os.path.join(
                    PRESET_DIR, repo, self.name + ".json")
            else:
                self.preset_path = preset_path
            self.load_preset()

    def __repr__(self) -> str:
        return f"Preset <{self.name}> with {self.variables}\n {self.palette}\n {self.custom_css}"

    def load_preset(self, text=None, preset=None):
        try:
            if not preset:
                if text:
                    preset_text = text
                else:
                    with open(self.preset_path, "r", encoding="utf-8") as file:
                        preset_text = file.read()
                preset = json.loads(preset_text)

            self.name = preset["name"]
            self.preset_name = to_slug_case(self.name)
            self.variables = preset["variables"]
            self.palette = preset["palette"]

            if "badges" in preset:
                self.badges = preset["badges"]
            else:
                self.badges = {}

            if "custom_css" in preset:
                self.custom_css = preset["custom_css"]
            else:
                for app_type in settings_schema["custom_css_app_types"]:
                    self.custom_css[app_type] = ""
        except Exception as error:
            buglog(error, " -> preset : ", self.preset_path)

    def save_preset(self, name=None, plugins_list=None, to=None):
        if to is None:
            self.preset_path = os.path.join(
                PRESET_DIR, self.repo, self.name + ".json")
        else:
            self.preset_path = to
        if not os.path.exists(
            os.path.join(
                PRESET_DIR,
                "user",
            )
        ):
            os.makedirs(
                os.path.join(
                    PRESET_DIR,
                    "user",
                )
            )

        if name is None:
            name = self.preset_name

        if plugins_list is None:
            plugins_list = {}
        else:
            plugins_list = plugins_list.save()

        with open(
            self.preset_path,
            "w",
            encoding="utf-8",
        ) as file:
            object_to_write = {
                "name": name,
                "variables": self.variables,
                "palette": self.palette,
                "custom_css": self.custom_css,
                "plugins": plugins_list,
            }
            file.write(json.dumps(object_to_write, indent=4))

    def validate(self):
        return True


if __name__ == "__main__":
    p = Preset("test", "user")
    print(p.variables)
    print(p.palette)
