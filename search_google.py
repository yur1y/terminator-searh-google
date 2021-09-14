#!/usr/bin/python
# -*- coding: utf-8 -*-
import terminatorlib.plugin as plugin
import webbrowser
import urllib.parse
from terminatorlib.util import err, dbg
from terminatorlib.translation import _
from terminatorlib.terminator import Terminator
from terminatorlib.version import APP_VERSION
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import re

# AVAILABLE must contain a list of all the classes that you want exposed

AVAILABLE = ['SearchGoogle']

_spaces = re.compile(" +")


class SearchGoogle(plugin.MenuItem):

    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)
        self.entry = Terminator().windows[0]
        self.searchstring = ""
        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

    def callback(
        self,
        menuitems,
        menu,
        terminal,
        ):
        item = Gtk.MenuItem(_('SearchGoogle'))
        if terminal.vte.get_has_selection():
            self.searchstring = self.clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 40:
                displaystring = self.searchstring[:37] + "..."
            else:
                displaystring = self.searchstring
            item.set_label("Google for \"%s\"" % displaystring)
            item.set_sensitive(True)
        else:
            item.set_label("Search Google")
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        item.connect('activate', self.search_google)
        menuitems.append(item)
        self.entry.connect('key-release-event', self.onKeyPress)
    def search_google(self, widget):
        """Launch Google search for string"""
        if not self.searchstring:
           return
        base_uri = "https://www.google.com/search?q=%s"
        uri = base_uri % urllib.parse.quote(self.searchstring.encode("utf-8"))
        Gtk.show_uri_on_window(None, uri, Gdk.CURRENT_TIME)

    def onKeyPress(self, widget, event):
        self.searchstring = self.clip.wait_for_text().strip()
        if float(APP_VERSION) <= 0.98:
            if event.state & Gtk.gdk.MOD1_MASK == Gtk.gdk.MOD1_MASK \
                and (event.keyval == 96 or event.keyval == 126):  # Alt+` or Alt+~
                self.search_google(widget)
        else:
            if event.state & Gdk.ModifierType.MOD1_MASK \
                == Gdk.ModifierType.MOD1_MASK and (event.keyval ==96
                    or event.keyval == 126):  # Alt+~ or Alt+`
                self.search_google(widget)
