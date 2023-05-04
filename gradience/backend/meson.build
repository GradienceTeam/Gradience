backenddir = 'gradience/backend'

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
    'DATA_DIR': conf.get('DATA_DIR'),
    'PKGDATA_DIR': PKGDATA_DIR,
    'LOCALE_DIR': conf.get('LOCALE_DIR'),
  }),
  install: true,
  install_dir: PY_INSTALLDIR.get_install_dir() / backenddir
)

subdir('models')
subdir('theming')
subdir('utils')

gradience_sources = [
    '__init__.py',
    'css_parser.py',
    'flatpak_overrides.py',
    'globals.py',
    'logger.py',
    'preset_downloader.py',
    'exceptions.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: backenddir)
