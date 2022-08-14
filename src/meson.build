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
  install_dir: PKGDATA_DIR,
  dependencies: blueprints,
)

configure_file(
  input: 'adwcustomizer.in',
  output: 'adwcustomizer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: conf,
  install: true,
  install_dir: MODULE_DIR
)

launcher = join_paths(meson.project_build_root(), 'src', meson.project_name())

run_target('run',
  command: [launcher]
)

# Install sources
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
  'run_async.py',
  'window.py',
  'app_type_dialog.py',
  'custom_css_group.py',
]
install_data(adwcustomizer_sources, install_dir: MODULE_DIR)