gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/error.blp',
    'ui/palette_shades.blp',
    'ui/option.blp',
    'ui/window.blp',
    'ui/app_type_dialog.blp',
    'ui/custom_css_group.blp',
    'ui/presets_manager_window.blp',
    'ui/plugin_row.blp',
    'ui/welcome.blp',
    'ui/preset_row.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('gradience',
  'gradience.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: PKGDATA_DIR,
  dependencies: blueprints,
)

configure_file(
  input: 'gradience.in',
  output: 'gradience',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: conf,
  install: true,
  install_dir: PY_INSTALLDIR.get_install_dir() / 'gradience',
)

launcher = join_paths(meson.project_build_root(), 'src', meson.project_name())

run_target('run',
  command: [launcher]
)

# Install sources
gradience_sources = [
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
  'presets_manager_window.py',
  'plugin_row.py',
  'welcome.py',
  'preset_row.py',
]

PY_INSTALLDIR.install_sources(gradience_sources, subdir: 'gradience')
#install_data(gradience_sources, install_dir: MODULE_DIR)