"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    ui.phoenix.main_settings.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import wx

from sppas.src.config import sppasBaseSettings

# ---------------------------------------------------------------------------


class WxAppSettings(sppasBaseSettings):
    """Manage the application global settings for look&feel.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self):
        """Create the dictionary of settings."""
        super(WxAppSettings, self).__init__()

    # -----------------------------------------------------------------------

    def load(self):
        """Load the dictionary of settings from a json file."""
        self.reset()

    # -----------------------------------------------------------------------

    def reset(self):
        """Fill the dictionary with the default values."""
        font = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_height = font.GetPixelSize()[1]

        self.__dict__ = dict(
            frame_style=wx.DEFAULT_FRAME_STYLE | wx.CLOSE_BOX,
            frame_size=self.__frame_size(),

            icons_theme="Refine",

            fg_color=wx.Colour(230, 230, 230),
            header_fg_color=wx.Colour(160, 160, 160),
            action_fg_color=wx.Colour(130, 130, 130),

            bg_color=wx.Colour(20, 20, 20, alpha=wx.ALPHA_OPAQUE),
            header_bg_color=wx.Colour(40, 40, 40, alpha=wx.ALPHA_OPAQUE),
            action_bg_color=wx.Colour(30, 30, 30, alpha=wx.ALPHA_OPAQUE),

            text_font=self.__text_font(),
            header_text_font=self.__header_font(),
            action_text_font=self.__action_font(),
            mono_text_font=self.__mono_font(),

            title_height=font_height*5,
            action_height=font_height*3,
        )

    # -----------------------------------------------------------------------

    def set(self, key, value):
        """Set a new value to a key."""
        setattr(self, key, value)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __text_font(self):
        s = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()
        text_font = wx.Font(s,                      # point size
                            wx.FONTFAMILY_DEFAULT,  # family,
                            wx.FONTSTYLE_NORMAL,    # style,
                            wx.FONTWEIGHT_NORMAL,   # weight,
                            underline=False,
                            faceName="Calibri",
                            encoding=wx.FONTENCODING_SYSTEM)
        return text_font

    # -----------------------------------------------------------------------

    def __header_font(self):
        s = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()
        title_font = wx.Font(s*2,                    # point size
                             wx.FONTFAMILY_DEFAULT,  # family,
                             wx.FONTSTYLE_NORMAL,    # style,
                             wx.FONTWEIGHT_BOLD,     # weight,
                             underline=False,
                             faceName="Calibri",
                             encoding=wx.FONTENCODING_SYSTEM)
        return title_font

    # -----------------------------------------------------------------------

    def __action_font(self):
        s = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()
        button_font = wx.Font(int(s*1.2),             # point size
                              wx.FONTFAMILY_DEFAULT,  # family,
                              wx.FONTSTYLE_NORMAL,    # style,
                              wx.FONTWEIGHT_NORMAL,   # weight,
                              underline=False,
                              faceName="Calibri",
                              encoding=wx.FONTENCODING_SYSTEM)
        return button_font

    # -----------------------------------------------------------------------

    def __mono_font(self):
        s = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()
        mono_font = wx.Font(int(s * 0.9),           # point size
                            wx.FONTFAMILY_MODERN,   # family,
                            wx.FONTSTYLE_NORMAL,    # style,
                            wx.FONTWEIGHT_NORMAL,   # weight,
                            underline=False,
                            encoding=wx.FONTENCODING_SYSTEM)
        return mono_font

    # -----------------------------------------------------------------------

    def __frame_size(self):
        (w, h) = wx.GetDisplaySize()
        w *= 0.6
        h = min(0.9*h, w*9/16)
        return wx.Size(max(int(w), 640), max(int(h), 480))
