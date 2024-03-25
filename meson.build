project('gradience',
          version: '0.8.0-beta2',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2',
                     'werror=false',
                   ],
)

# Import modules
gnome = import('gnome')
i18n = import('i18n')
python = import('python')

# Project information
PROJECT_URL = 'https://github.com/GradienceTeam/Gradience'
BUGTRACKER_URL = 'https://github.com/GradienceTeam/Gradience/issues'
HELP_URL = 'https://github.com/GradienceTeam/Gradience/discussions'
TRANSLATE_URL = 'https://hosted.weblate.org/projects/GradienceTeam/gradience'

# Constants
PROJECT_RDNN_NAME = 'com.github.GradienceTeam.Gradience'

git_bin = find_program('git', required: false)

# Set APPLICATION_ID and VERSION_SUFFIX
if get_option('buildtype') == 'debug'
  if git_bin.found()
    VCS_TAG = run_command('git', 'rev-parse', '--short', 'HEAD', check: true).stdout().strip()
  else
    VCS_TAG = ''
  endif
  if VCS_TAG == ''
    VERSION_SUFFIX = '-devel'
  else
    VERSION_SUFFIX = '-@0@'.format(VCS_TAG)
  endif
  APPLICATION_ID = '@0@.Devel'.format(PROJECT_RDNN_NAME)
else
  VERSION_SUFFIX = ''
  APPLICATION_ID = PROJECT_RDNN_NAME
endif

dependency('glib-2.0')
dependency('gtk4', version: '>= 4.5.0')
dependency('libadwaita-1', version: '>= 1.2.alpha')
dependency('pygobject-3.0', version: '>= 3.42.0')
dependency('libsoup-3.0', version: '>= 3.2.0')

# Python installation directory
PY_INSTALLDIR = python.find_installation('python3', required: true, modules: ['lxml'])

# Check if python3 is installed
if not PY_INSTALLDIR.found()
    error('No valid python3 binary found')
endif

PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
MODULE_DIR = join_paths(PKGDATA_DIR, 'gradience')
PLUGINS_DIR = join_paths(PKGDATA_DIR, 'gradience', 'plugins')

# Install configuration data
conf = configuration_data()
conf.set('APP_ID', APPLICATION_ID)
conf.set('PKGDATA_DIR', PKGDATA_DIR)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', PY_INSTALLDIR.full_path())
conf.set('VERSION', meson.project_version() + VERSION_SUFFIX)
conf.set('BUILD_TYPE', get_option('buildtype'))
conf.set('SCHEMAS_DIR', PKGDATA_DIR)
conf.set('SOURCE_DIR', meson.current_source_dir())
conf.set('BUILD_DIR', meson.current_build_dir())

conf.set('local_build', 'False')

# Local install configuration data
local_conf = configuration_data()
local_conf.set('APP_ID', APPLICATION_ID)
local_conf.set('PKGDATA_DIR', join_paths(meson.current_build_dir(), 'data'))
local_conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
local_conf.set('PYTHON', meson.current_source_dir())
local_conf.set('VERSION', meson.project_version() + VERSION_SUFFIX)
local_conf.set('BUILD_TYPE', get_option('buildtype'))
local_conf.set('SCHEMAS_DIR', join_paths(meson.current_build_dir(), get_option('datadir')))
local_conf.set('SOURCE_DIR', meson.current_source_dir())
local_conf.set('BUILD_DIR', meson.current_build_dir())

local_conf.set('local_build', 'True')

# Subdirs
subdir('gradience')
subdir('data')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
