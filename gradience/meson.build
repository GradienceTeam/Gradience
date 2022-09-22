configure_file(
  input: 'gradience.in',
  output: 'gradience',
  configuration: conf,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'gradience.in',
  output: 'local-gradience',
  configuration: local_conf
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: configuration_data({
    'APP_ID': APPLICATION_ID,
    'RELEASE_VER': meson.project_version(),
    'VERSION': meson.project_version() + VERSION_SUFFIX,
    'BUILD_TYPE': get_option('buildtype'),
    'PROJECT_URL': PROJECT_URL,
    'BUGTRACKER_URL': BUGTRACKER_URL,
    'HELP_URL': HELP_URL,
    'TRANSLATE_URL': TRANSLATE_URL,
    'PKGDATA_DIR': PKGDATA_DIR,
    'LOCALE_DIR': LOCALE_DIR,
  }),
  install: true,
  install_dir: PY_INSTALLDIR.get_install_dir() / 'gradience',
)

launcher = join_paths(meson.project_build_root(), 'gradience', 'local-' + meson.project_name())

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
  'window.py',
  'app_type_dialog.py',
  'custom_css_group.py',
  'presets_manager_window.py',
  'preferences.py',
  'plugin_row.py',
  'explore_preset_row.py',
  'builtin_preset_row.py',
  'preset_row.py',
  'welcome.py',
  'repo_row.py',
]

PY_INSTALLDIR.install_sources(gradience_sources, subdir: 'gradience')

# Install modules
gradience_modules = [
  'modules/__init__.py',
  'modules/custom_presets.py',
  'modules/flatpak_overrides.py',
  'modules/utils.py',
  'modules/run_async.py',
  'modules/css.py',
  'modules/preset.py',
  'modules/repo.py',
]

PY_INSTALLDIR.install_sources(gradience_modules, subdir: 'gradience/modules')
