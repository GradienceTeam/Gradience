blueprints = custom_target('blueprints',
  input: files(
    'error.blp',
    'palette_shades.blp',
    'option.blp',
    'window.blp',
    'app_type_dialog.blp',
    'custom_css_group.blp',
    'presets_manager_window.blp',
    'plugin_row.blp',
    'welcome.blp',
    'preset_row.blp',
    'builtin_preset_row.blp',
    'explore_preset_row.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)
