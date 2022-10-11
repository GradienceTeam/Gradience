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
  'plugins_list.py',
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: 'gradience')

# Install utility modules
gradience_utils = [
  'utils/__init__.py',
  'utils/custom_presets.py',
  'utils/flatpak_overrides.py',
  'utils/utils.py',
  'utils/run_async.py',
  'utils/css.py',
  'utils/preset.py',
  'utils/repo.py',
]
PY_INSTALLDIR.install_sources(gradience_utils, subdir: 'gradience/utils')

# Install ui Python modules
gradience_ui_modules = [
  'ui/error_list_row.py',
  'ui/palette_shades.py',
  'ui/option_row.py',
  'ui/window.py',
  'ui/app_type_dialog.py',
  'ui/custom_css_group.py',
  'ui/presets_manager_window.py',
  'ui/preferences_window.py',
  'ui/plugin_row.py',
  'ui/explore_preset_row.py',
  'ui/builtin_preset_row.py',
  'ui/preset_row.py',
  'ui/welcome_window.py',
  'ui/repo_row.py',
  'ui/no_plugin_window.py',
  'ui/share_window.py',
]
PY_INSTALLDIR.install_sources(gradience_ui_modules, subdir: 'gradience/ui')
