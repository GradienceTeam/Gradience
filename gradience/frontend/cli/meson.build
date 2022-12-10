clidir = 'gradience/frontend/cli'

configure_file(
  input: 'cli.in',
  output: 'gradience-cli',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gradience_sources = [
    '__init__.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: clidir)
