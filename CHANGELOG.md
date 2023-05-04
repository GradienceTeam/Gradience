# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for GNOME Shell theming
- New, refreshed design for `Theming` tab
- Preferences options for enabling built-in Theme Engines

### Changed

- Update runtime to GNOME 44
- Move reset and restore preset options to preferences

### Fixed

- Improve contrasts in Monet generated error/destructive colors
- Don't fail at compilation if host doesn't have `git` installed
- Don't fail at resetting presets if `gtk.css` isn't found

## [0.4.1] - 2023-03-05

### Changed

- Only configure local CLI if `buildtype` is set to debug
- Margins in popup explanations and some other widgets
- Object names in preferences window
- Translation updates

### Fixed

- Local CLI executable making issues with Fedora CI
- Theme variant menu in Monet Engine not working with non-english locales
- Applied temporary patch for `CssProvider.load_from_data()` new behavior in GTK 4.9

## [0.4.0] - 2023-02-09

### Added

- Command-line interface, useful for creating scripts or for those who prefer terminal tools
- New logging facility, with easier to understand error messages

### Removed

- Preset preview button and "Repositories" tab in Preset Manager have been removed due to lack of proper implementation

### Changed

- Now Gradience warns user when switching to other presets, if current one has unsaved changes
- Gradience started internally use hexadecimal color values or RGBA formatted colors if transparency is provided
- Start moving out remaining backend functions from frontend modules
- Codebase is now linted by pylint
- Translation updates

### Fixed

- Fixed color palette leaking into preset variables in some rare occasions
- Fixed list index out of range error in Custom CSS editor
- Fixed sorting in "Explore" tab of Preset Manager not working with non-English locales

## [0.3.3] - 2022-12-03

## Changed

- The Firefox GNOME theme plugin now parses profiles from `profiles.ini`
- Theme Preview button is accessible again
- Plugin row now has the correct controls placement
- Codebase structure has been refactored
- Improved details tab in About dialog
- Added new "Log out" dialog logic
- Updated translations

## [0.3.2] - 2022-11-20

### Changed

- The Firefox GNOME theme plugin now correctly parses installations with multiple profiles
- Added mnemonics for dialogs
- Save is now a default response in dialogs
- Plugin rows now look cleaner and are correctly placed
- File picker is now modal and sticks to the parent window
- <kbd>Esc</kbd> now closes dialogs and Preset Manager
- Grandience can now be closed with <kbd>Ctrl</kbd> + <kbd>Q</kbd>
- "Favourite(s)" was renamed to "Favorite(s)"
- Тransitioned from `cssutils` library to an in-house solution
- Presets are now removed correctly
- The internal structure was refactored
- Various typos were fixed
- The `README.md` was fully rewritten
- All screenshots were taken in high resolution
- New and updated translations

### Fixed

- Fixed issues with the CSS parser
- Fixed an issue with presets always being saved as User.json

## [0.3.1] - 2022-10-08

### Added

- Added ability to star preset to display it in Palette menu
- Added filter to search presets by preset repositories in Preset Manager
- Added "No Preferences" window for use in plugins
- Added "Log Out" dialog showing after applying a preset

### Changed

- Updated Firefox GNOME Theme plugin
- Welcome screen have been improved
- Preset Manager window size has changed
- "Offline" and "Nothing Found" fallback pages have been added to Preset Manager
- Many strings were rewritten to follow GNOME HIG
- Switch from `aiohttp` to `libsoup3`
- Migrate to GNOME SDK 43
- All contributors have been added to "About" window
- Some symbolics have changed, removed unnecessary hardcoded symbolics
- New and updated translations

### Fixed

- Flatpak theme override is now fixed
- Margins in color info popovers are fixed

## [0.3.0] - 2022-09-23

### Added

- Added plugins support, this will allow users to create plugins for customizing other apps
- Added support for custom preset repositories, this allows creating your own remote selection of presets
- Added search feature to Preset Manager
- Added Quick Preset Switcher back, with it you can switch presets with less clicks

### Changed

- Preset Manager performance has significantly increased, presets are downloading much faster and app don't freeze on preset removal
- Preset Manager is attached to the main window
- Save dialog now shows up when you close app with unsaved preset
- Currently applied preset now auto-loads on app start-up
- Toasts are less annoying
- Added support for aarch64 builds

<!-- TODO: Below version changelogs aren't yet filled -->

## [0.2.2] - 2022-09-02

## [0.2.1] - 2022-08-30

## [0.2.0] - 2022-08-26

## [0.1.0] - 2022-08-12
