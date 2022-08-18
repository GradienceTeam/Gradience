from adwcustomizer.plugin import AdwcustomizerPluginCore

class GDMPlugin(AdwcustomizerPluginCore):
    def validate(self):
        print("validate")
    def apply(self, dark_theme=False):
        print("apply")

    def save(self):
        print("save")