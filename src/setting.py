class AdwcustomizerSetting:
    def __init__(self, name, title, value_type, explanation=None, default_value=None):
        # TODO supported types:
        #  text
        #  integer
        #  float
        #  color only
        #  color shades
        #  color and text
        #  code field
        self.name = name
        self.title = title
        self.value_type = value_type
        self.explanation = explanation
        self.value = default_value

    def set_value(self, new_value):
        # TODO checks
        self.value = new_value