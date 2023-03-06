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

  launcher = join_paths(meson.project_build_root(), moduledir, 'frontend', 'local-' + meson.project_name())

  run_target('run',
    command: [launcher]
  )
endif

subdir('cli')
subdir('dialogs')
subdir('schemas')
subdir('utils')
subdir('views')
subdir('widgets')

gradience_sources = [
    '__init__.py',
    'main.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: frontenddir)
