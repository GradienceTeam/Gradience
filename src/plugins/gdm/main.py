from gradience.plugin import GradiencePluginCore


class GDMPlugin(GradiencePluginCore):
    def validate(self):
        print("validate")

    def apply(self, dark_theme=False):
        print("apply")

    def save(self):
        print("save")
