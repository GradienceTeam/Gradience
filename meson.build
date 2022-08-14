project('gradience',
          version: '0.1.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2',
                     'werror=false',
                   ],
)

# Import modules
gnome = import('gnome')
i18n = import('i18n')
python = import('python')

# Constants
PROJECT_RDNN_NAME = 'com.github.AdwCustomizerTeam.AdwCustomizer'
APPLICATION_ID = PROJECT_RDNN_NAME

dependency('glib-2.0')
dependency('gtk4', version: '>= 4.5.0')
dependency('libadwaita-1', version: '>= 1.2.alpha')
dependency('pygobject-3.0', version: '>= 3.42.0')

# Python installation directory
PY_INSTALLDIR = python.find_installation('python3')

# Check if python3 is installed
if not PY_INSTALLDIR.found()
    error('No valid python3 binary found')
endif

PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
MODULE_DIR = join_paths(PKGDATA_DIR, 'adwcustomizer')
PLUGINS_DIR = join_paths(PKGDATA_DIR, 'adwcustomizer', 'plugins')

# Install configuration data
conf = configuration_data()
conf.set('APP_ID', PROJECT_RDNN_NAME)
conf.set('PKGDATA_DIR', PKGDATA_DIR)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', PY_INSTALLDIR.full_path())
conf.set('VERSION', meson.project_version())
conf.set('BUILD_TYPE', get_option('buildtype'))

# Subdirs
subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
