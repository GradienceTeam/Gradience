from jinja2 import Environment, FileSystemLoader

import os

def modify_colors(scss_path, output_path, **vars):
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(scss_path)),
    )
    template = env.get_template('_colors.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template.render(**vars))
