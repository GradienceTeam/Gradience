moduledir = 'gradience'

subdir('backend')
subdir('frontend')

launcher = join_paths(meson.project_build_root(), moduledir, 'frontend', 'local-' + meson.project_name())

run_target('run',
  command: [launcher]
)

gradience_sources = [
  '__init__.py'
]
PY_INSTALLDIR.install_sources(gradience_sources, subdir: moduledir)
