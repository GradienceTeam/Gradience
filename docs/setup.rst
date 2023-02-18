.. highlight:: shell

===============
🎨️ First setup
===============

.. note::

    You can go to `Preferences` and apply overrides for Flatpak

Manual setup
----------------

Libadwaita applications
~~~~~~~~~~~~~~~~~~~~~~~

No additional setup is required for native Libadwaita applications.

For Flatpak Libadwaita applications, you need to override their permissions:

+ Run `sudo flatpak override --filesystem=xdg-config/gtk-4.0` or
+ Use `Flatseal`_ and adding `xdg-config/gtk-4.0` to **Other files** in the **Filesystem** section of **All Applications**

Vanilla GTK 4 applications
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use `this guide`_ to theme vanilla GTK 4 applications.

GTK 3 applications
~~~~~~~~~~~~~~~~~~~~~~

- Install and apply the `adw-gtk3`_ theme (don't forget to install the Flatpak package!)
- For Flatpak applications, you need to override their permissions:

  - Run `sudo flatpak override --filesystem=xdg-config/gtk-3.0` or
  - Use `Flatseal`_ and adding `xdg-config/gtk-3.0` to **Other files** in the **Filesystem** section of **All Applications**

.. _Flatseal: https://github.com/tchx84/Flatseal
.. _adw-gtk3: https://github.com/lassekongo83/adw-gtk3#readme
.. _this guide: https://github.com/lassekongo83/adw-gtk3/blob/main/gtk4.md


Revert Theming
------------------

.. note::
    You can press on the menu button in the headerbar and press `Reset Applied Color Scheme`

    .. image:: https://raw.githubusercontent.com/GradienceTeam/Design/main/Screenshots/hamburger_menu.png
        :alt: Image of the hamburger menu

Manual revert
~~~~~~~~~~~~~~~~~

Remove GTK 3 and GTK 4 configs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the following command in your terminal

.. code-block:: console

    rm -rf .config/gtk-4.0 .config/gtk-3.0

Remove adw-gtk3 theme
^^^^^^^^^^^^^^^^^^^^^

Run the following command in your terminal to remove Flatpak adw-gtk3 theme

.. code-block:: console

    flatpak uninstall adw-gtk3

Run the following command in your terminal to remove local adw-gtk3 theme

.. code-block:: console

    rm -rf .themes/adw-gtk3 .themes/adw-gtk3-dark .local/share/themes/adw-gtk3 .local/share/themes/adw-gtk3-dark

Reset Flatpak overrides
^^^^^^^^^^^^^^^^^^^^^^^^

Run the following command in your terminal

.. code-block:: console

    sudo flatpak override --reset

.. warning::

    This will reset all Flatpak overrides, such as Firefox Wayland override


