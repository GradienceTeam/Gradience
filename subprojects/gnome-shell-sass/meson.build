project('gnome-shell-sass',
        meson_version: '>= 0.51',
        license : ['GPL.2'])

sassc = find_program('sassc')

gnome_shell_sass_dir = join_paths(get_option('datadir'), 'gradience', 'gnome-shell-sass')


install_subdir('widgets', install_dir : gnome_shell_sass_dir, strip_directory : false)

theme_sources = files([
    '_colors.scss',
    '_common.scss',
    '_drawing.scss',
    '_high-contrast-colors.scss',
    '_palette.scss',
    '_widgets.scss',
    'gnome-shell.scss',
    'gnome-shell-high-contrast.scss',
])

install_data(theme_sources, install_dir : gnome_shell_sass_dir)
install_data('COPYING', install_dir : gnome_shell_sass_dir)
