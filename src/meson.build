pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'adwcustomizer')
pluginsdir = join_paths(pkgdatadir, 'adwcustomizer', 'plugins')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/error.blp',
    'ui/palette_shades.blp',
    'ui/option.blp',
    'ui/window.blp',
    'ui/app_type_dialog.blp',
    'ui/custom_css_group.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('adwcustomizer',
  'adwcustomizer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'adwcustomizer.in',
  output: 'adwcustomizer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

adwcustomizer_sources = [
  '__init__.py',
  'settings_schema.py',
  'main.py',
  'error.py',
  'palette_shades.py',
  'plugin.py',
  'plugins_list.py',
  'setting.py',
  'option.py',
  'window.py',
  'app_type_dialog.py',
  'custom_css_group.py',
]

plugins_sources = [
  'plugins/__init__.py',
  'plugins/gtk4.py'
]

install_data(adwcustomizer_sources, install_dir: moduledir)
install_data(plugins_sources, install_dir: pluginsdir)