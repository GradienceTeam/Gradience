scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.svg').format(APPLICATION_ID)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(PROJECT_RDNN_NAME)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir),
  rename: '@0@-symbolic.svg'.format(APPLICATION_ID)
)
