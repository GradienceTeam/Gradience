pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'adwcustomizer')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/error.blp',
    'ui/palette_shades.blp',
    'ui/option.blp',
    'ui/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('adwcustomizer',
  'adwcustomizer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'adwcustomizer.in',
  output: 'adwcustomizer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

adwcustomizer_sources = [
  '__init__.py',
  'main.py',
  'error.py',
  'palette_shades.py',
  'option.py',
  'window.py',
]

install_data(adwcustomizer_sources, install_dir: moduledir)
