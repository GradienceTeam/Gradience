# gsettings.py
#
# Change the look of Adwaita, with ease
# Copyright (c) 2011, John Stowers
# Copyright (C) 2023, Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# NOTICE:
# This code is from the GNOME Tweaks application, which is licensed under the GPL-3.0 license.
# https://gitlab.gnome.org/GNOME/gnome-tweaks/-/blob/master/gtweak/gsettings.py

import os
import re
import shutil
import os.path
import xml.dom.minidom
import gettext

from subprocess import SubprocessError, CompletedProcess

from gi.repository import Gio, GLib

from gradience.backend.utils.subprocess import GradienceSubprocess
from gradience.backend.constants import localedir, app_id

from gradience.backend.logger import Logger

logging = Logger(logger_name="GSettings")


_SCHEMA_CACHE = {}
_GSETTINGS_SCHEMAS = set(Gio.Settings.list_schemas())
_GSETTINGS_RELOCATABLE_SCHEMAS = set(Gio.Settings.list_relocatable_schemas())


class GSettingsMissingError(Exception):
    pass


class _GSettingsSchema:
    def __init__(self, schema_name, schema_dir=None, schema_filename=None, **options):
        if not schema_filename:
            schema_filename = schema_name + ".gschema.xml"
        if not schema_dir:
            schema_dir = app_id
            for xdg_dir in GLib.get_system_data_dirs():
                dir = os.path.join(xdg_dir, "glib-2.0", "schemas")
                if os.path.exists(os.path.join(dir, schema_filename)):
                    schema_dir = dir
                    break

        schema_path = os.path.join(schema_dir, schema_filename)
        if not os.path.exists(schema_path):
            logging.critical("Could not find schema %s" % schema_path)
            assert (False)

        self._schema_name = schema_name
        self._schema = {}

        try:
            dom = xml.dom.minidom.parse(schema_path)
            global_gettext_domain = dom.documentElement.getAttribute(
                'gettext-domain')
            try:
                if global_gettext_domain:
                    # We can't know where the schema owner was installed, let's assume it's
                    # the same prefix as ours
                    global_translation = gettext.translation(
                        global_gettext_domain, localedir)
                else:
                    global_translation = gettext.NullTranslations()
            except IOError:
                global_translation = None
                logging.debug("No translated schema for %s (domain: %s)" % (
                    schema_name, global_gettext_domain))
            for schema in dom.getElementsByTagName("schema"):
                gettext_domain = schema.getAttribute('gettext-domain')
                try:
                    if gettext_domain:
                        translation = gettext.translation(
                            gettext_domain, localedir)
                    else:
                        translation = global_translation
                except IOError:
                    translation = None
                    logging.debug("Schema not translated %s (domain: %s)" % (
                        schema_name, gettext_domain))
                if schema_name == schema.getAttribute("id"):
                    for key in schema.getElementsByTagName("key"):
                        name = key.getAttribute("name")
                        # summary is 'compulsory', description is optional
                        # …in theory, but we should not barf on bad schemas ever
                        try:
                            summary = key.getElementsByTagName(
                                "summary")[0].childNodes[0].data
                        except:
                            summary = ""
                            logging.info("Schema missing summary %s (key %s)" %
                                         (os.path.basename(schema_path), name))
                        try:
                            description = key.getElementsByTagName(
                                "description")[0].childNodes[0].data
                        except:
                            description = ""

                        # if missing translations, use the untranslated values
                        self._schema[name] = dict(
                            summary=translation.gettext(
                                summary) if translation else summary,
                            description=translation.gettext(
                                description) if translation else description
                        )

        except:
            logging.critical("Error parsing schema %s (%s)" %
                             (schema_name, schema_path), exc_info=True)

    def __repr__(self):
        return "<gradience._GSettingsSchema: %s>" % self._schema_name


class GSettingsSetting(Gio.Settings):
    def __init__(self, schema_name, schema_dir=None, schema_path=None, **options):

        if schema_dir is None:
            if schema_path is None and schema_name not in _GSETTINGS_SCHEMAS:
                raise GSettingsMissingError(schema_name)

            if schema_path is not None and schema_name not in _GSETTINGS_RELOCATABLE_SCHEMAS:
                raise GSettingsMissingError(schema_name)

            if schema_path is None:
                Gio.Settings.__init__(self, schema=schema_name)
            else:
                Gio.Settings.__init__(
                    self, schema=schema_name, path=schema_path)
        else:
            GioSSS = Gio.SettingsSchemaSource
            schema_source = GioSSS.new_from_directory(schema_dir,
                                                      GioSSS.get_default(),
                                                      False)
            schema_obj = schema_source.lookup(schema_name, True)
            if not schema_obj:
                raise GSettingsMissingError(schema_name)

            Gio.Settings.__init__(self, None, settings_schema=schema_obj)

        if schema_name not in _SCHEMA_CACHE:
            _SCHEMA_CACHE[schema_name] = _GSettingsSchema(
                schema_name, schema_dir=schema_dir, **options)
            logging.debug("Caching gsettings: %s" % _SCHEMA_CACHE[schema_name])

        self._schema = _SCHEMA_CACHE[schema_name]

    def _on_changed(self, settings, key_name):
        logging.debug("Change: %s %s -> %s" %
              (self.props.schema, key_name, self[key_name]))

    def _setting_check_is_list(self, key):
        variant = Gio.Settings.get_value(self, key)
        return variant.get_type_string() == "as"

    def schema_get_summary(self, key):
        return self._schema._schema[key]["summary"]

    def schema_get_description(self, key):
        return self._schema._schema[key]["description"]

    def schema_get_all(self, key):
        return self._schema._schema[key]

    def setting_add_to_list(self, key, value):
        """ helper function, ensures value is present in the GSettingsList at key """
        assert self._setting_check_is_list(key)

        vals = self[key]
        if value not in vals:
            vals.append(value)
            self[key] = vals
            return True

    def setting_remove_from_list(self, key, value):
        """ helper function, removes value in the GSettingsList at key (if present)"""
        assert self._setting_check_is_list(key)

        vals = self[key]
        try:
            vals.remove(value)
            self[key] = vals
            return True
        except ValueError:
            # not present
            pass

    def setting_is_in_list(self, key, value):
        assert self._setting_check_is_list(key)
        return value in self[key]


class FlatpakGSettings:
    def __init__(self, schema_name, schema_dir=None, **options):
        self.schema_name = schema_name
        self.schema_dir = schema_dir

    def list_keys(self) -> str:
        dconf_cmd = ["gsettings", "list-keys", self.schema_name]
        process = GradienceSubprocess()

        if self.schema_dir:
            self._insert_schemadir(dconf_cmd)

        try:
            completed = process.run(dconf_cmd, allow_escaping=True)
            stdout = process.get_stdout_data(completed, decode=True)
        except SubprocessError:
            raise
        else:
            return stdout

    def get(self, key:str) -> CompletedProcess:
        dconf_cmd = ["gsettings", "get", self.schema_name, key]
        process = GradienceSubprocess()

        if self.schema_dir:
            self._insert_schemadir(dconf_cmd)

        try:
            completed = process.run(dconf_cmd, allow_escaping=True)
            stdout = process.get_stdout_data(completed, decode=True)
        except SubprocessError:
            raise
        else:
            return stdout

    def set(self, key:str, value:str) -> None:
        dconf_cmd = ["gsettings", "set", self.schema_name, key, value]
        process = GradienceSubprocess()

        if self.schema_dir:
            self._insert_schemadir(dconf_cmd)

        try:
            process.run(dconf_cmd, allow_escaping=True)
        except SubprocessError:
            raise

    def reset(self, key:str = None) -> None:
        dconf_cmd = ["gsettings", "reset", self.schema_name, key]
        process = GradienceSubprocess()

        if self.schema_dir:
            self._insert_schemadir(dconf_cmd)

        try:
            process.run(dconf_cmd, allow_escaping=True)
        except SubprocessError:
            raise

    def _insert_schemadir(self, dconf_cmd):
        dconf_cmd.insert(1, "--schemadir")
        dconf_cmd.insert(2, self.schema_dir)
