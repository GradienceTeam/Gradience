.. highlight:: shell

================
📦️ Installation
================

Flatpak
-------

To install Gradience, run this command in your terminal:

.. code-block:: console

    $ flatpak install com.github.GradienceTeam.Gradience

This is the preferred method to install Gradience, as it will always install the most recent stable release in a portable way whatever the distribution you use.

If you don't have `flatpak`_ installed, this `Flatpak installation guide`_ can guide
you through the process.

.. _flatpak: https://flatpak.org
.. _Flatpak installation guide: https://flatpak.org/setup/

COPR (RPM Based)
----------------

Gradience is available on COPR. You can install it using the following command:

.. code-block:: console

    $ dnf copr enable lyessaadi/gradience
    $ dnf install gradience

AUR
---

Gradience is available on AUR:

Using `Paru`_:

.. code-block:: console

    $ paru -S gradience


For latest changes (git version maybe unstable):

.. code-block:: console

    $ paru -S gradience-git

.. _Paru: https://github.com/morganamilo/paru


From sources
------------

The sources for Gradience can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/GradienceTeam/Gradience

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/GradienceTeam/Gradience/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make install


.. _Github repo: https://github.com/GradienceTeam/Gradience
.. _tarball: https://github.com/GradienceTeam/Gradience/tarball/master
