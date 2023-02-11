frontenddir = 'gradience/frontend'

configure_file(
  input: 'gradience.in',
  output: 'gradience',
  configuration: conf,
  install_dir: get_option('bindir')
)

if get_option('buildtype') == 'debug'
  configure_file(
    input: 'gradience.in',
    output: 'local-gradience',
    configuration: local_conf
  )
endif

subdir('cli')
subdir('dialogs')
subdir('utils')
subdir('views')
subdir('widgets')

gradience_sources = [
    '__init__.py',
    'main.py',
    'settings_schema.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: frontenddir)
