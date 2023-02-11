clidir = 'gradience/frontend/cli'

configure_file(
  input: 'cli.in',
  output: 'gradience-cli',
  configuration: conf,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'cli.in',
  output: 'gradience-cli',
  configuration: local_conf,
  install_dir: join_paths(meson.project_build_root(), 'gradience', 'frontend')
)

gradience_sources = [
    '__init__.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: clidir)
