.. highlight:: shell

======
⚙️ CLI
======

In version 0.4.0 we introduced an initial command-line interface, with a basic set of features from Gradience UI.

How to launch CLI
-----------------

There are two different ways to launch CLI, one is for Flatpak version of Gradience, and another is for Gradience installed from other sources.

Flatpak approach:
-----------------

If using Gradience as a Flatpak package, launch CLI with:

.. code-block:: console

    flatpak run --command=gradience-cli com.github.GradienceTeam.Gradience --help


Alternative approach:
---------------------

Launch CLI with a dedicated command: `gradience-cli`

CLI global help:
----------------

.. code-block:: console

    usage: gradience-cli [-h] [-V] {presets,favorites,import,apply,download,monet,access-file,flatpak-overrides} ...

    Gradience - Change the look of Adwaita, with ease

    positional arguments:
      {presets,favorites,import,apply,download,monet,access-file,flatpak-overrides}
        presets             list installed presets
        favorites           list favorite presets
        import              import a preset
        apply               apply a preset
        download            download preset from a preset repository
        monet               generate Material You preset from an image
        access-file         allow or disallow Gradience to access a certain file or directory
        flatpak-overrides   enable or disable Flatpak theming

    options:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit


Available arguments
-------------------

Presets
-------

.. code-block:: console

    usage: gradience-cli presets [-h] [-j]

    options:
      -h, --help  show this help message and exit
      -j, --json  print out a result of this command directly in JSON format


Favorites
---------

.. code-block:: console

    usage: gradience-cli favorites [-h] [-a PRESET_NAME] [-r PRESET_NAME] [-j]

    options:
      -h, --help            show this help message and exit
      -a PRESET_NAME, --add-preset PRESET_NAME
                            add a preset to favorites
      -r PRESET_NAME, --remove-preset PRESET_NAME
                            remove a preset from favorites
      -j, --json            print out a result of this command directly in JSON format


Import
------

.. code-block:: console

    usage: gradience-cli import [-h] -p PRESET_PATH

    options:
      -h, --help            show this help message and exit
      -p PRESET_PATH, --preset-path PRESET_PATH
                            absolute path to a preset file


Apply
-----

.. code-block:: console

    usage: gradience-cli apply [-h] (-n PRESET_NAME | -p PRESET_PATH) [--gtk {gtk4,gtk3,both}]

    options:
      -h, --help            show this help message and exit
      -n PRESET_NAME, --preset-name PRESET_NAME
                            display name for a preset
      -p PRESET_PATH, --preset-path PRESET_PATH
                            absolute path to a preset file
      --gtk {gtk4,gtk3,both}
                            types of applications you want to theme (default: gtk4)


Download
--------

.. code-block:: console

    usage: gradience-cli download [-h] -n PRESET_NAME

    options:
      -h, --help            show this help message and exit
      -n PRESET_NAME, --preset-name PRESET_NAME
                            name of a preset you want to get


Monet
-----

.. code-block:: console

    usage: gradience-cli monet [-h] -n PRESET_NAME -p IMAGE_PATH [--tone TONE] [--theme {light,dark}] [-j]

    options:
      -h, --help            show this help message and exit
      -n PRESET_NAME, --preset-name PRESET_NAME
                            name for a generated preset
      -p IMAGE_PATH, --image-path IMAGE_PATH
                            absolute path to image
      --tone TONE           a tone for colors (default: 20)
      --theme {light,dark}  choose whatever it should be a light or dark theme (default: light)
      -j, --json            print out a result of this command directly in JSON format


Access-file
-----------

.. code-block:: console

    usage: gradience-cli access-file [-h] [-l] [-a PATH | -d PATH]

    options:
      -h, --help            show this help message and exit
      -l, --list            list allowed directories and files
      -a PATH, --allow PATH
                            allow Gradience access to this file or directory
      -d PATH, --disallow PATH
                            disallow Gradience access to this file or directory


Flatpak-overrides
-----------------

.. code-block:: console

    usage: gradience-cli flatpak-overrides [-h] (-e {gtk4,gtk3,both} | -d {gtk4,gtk3,both})

    options:
      -h, --help            show this help message and exit
      -e {gtk4,gtk3,both}, --enable-theming {gtk4,gtk3,both}
                            enable overrides for Flatpak theming
      -d {gtk4,gtk3,both}, --disable-theming {gtk4,gtk3,both}
                            disable overrides for Flatpak theming


Raw JSON output
---------------

Some commands contain local parameter `--json` to help developers in implementing interactions with Gradience. Currently it can only be used with a handful of available arguments, but there are plans to extend this feature to all arguments. This parameter when used with supported argument, will output argument result in JSON format.

Example with `favorites` command:

.. code-block:: console

    $ gradience-cli favorites --json
    {"favorites": ["Oblivion", "Peninsula", "Kate", "Yaru Dark", "Cobalt Dark", "Nord Dark"], "amount": 6}

