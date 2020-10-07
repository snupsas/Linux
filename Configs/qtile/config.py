# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, extension
from typing import List  # noqa: F401

mod = "mod4"                                        # Sets mod key to SUPER/WINDOWS
myTerm = "terminology"                              # My terminal of choice
myConfig = "/home/ben/.config/qtile/config.py"      # The Qtile config file location

keys = [
         ### Test ###
        Key([mod], "q", lazy.run_extension(extension.DmenuRun(
            dmenu_prompt=">",
            #dmenu_font="Andika-8",
            background="#15181a",
            foreground="#00ff00",
            selected_background="#079822",
            selected_foreground="#fff",
            dmenu_bottom="true",
            #dmenu_height=26,  # Only supported by some dmenu forks
        ))),

         ### The essentials
         Key([mod], "x",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         #Key([mod], "q",
        #     lazy.spawn("dmenu_run -p 'Run: '"),
        #     desc='Dmenu Run Launcher'
        #     ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Treetab controls
         Key([mod, "control"], "k",
             lazy.layout.section_up(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "control"], "j",
             lazy.layout.section_down(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "k",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod, "shift"], "m",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "space",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "control"], "Return",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             )
]

group_names = [("WWW", {'layout': 'monadtall',      'label': ''}),
               ("DEV", {'layout': 'monadtall',      'label': ''}),
               ("TERM", {'layout': 'monadtall',     'label': ''}),
               ("FILE", {'layout': 'monadtall',     'label': ''}),
               ("MUSIC", {'layout': 'monadtall',    'label': ''}),
               ("LAB", {'layout': 'monadtall',      'label': ''})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 1,
                "margin": 3,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND"],
         section_fontsize = 11,
         bg_color = "141414",
         active_bg = "90C435",
         active_fg = "000000",
         inactive_bg = "384323",
         inactive_fg = "a0a0a0",
         padding_y = 5,
         section_top = 10,
         panel_width = 320
         ),
    layout.Floating(**layout_theme)
]

colors = [["#292d3e", "#292d3e"], # [0] panel background
          ["#434758", "#434758"], # [1] background for current screen tab
          ["#ffffff", "#ffffff"], # [2] font color for group names
          ["#ff5555", "#ff5555"], # [3] border line color for current tab
          ["#8d62a9", "#8d62a9"], # [4] border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # [5] color for the even widgets
          ["#e1acff", "#e1acff"]] # [6] window name

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
                widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0]
                ),
                widget.TextBox(
                #text = "",            # house
                text = "",             # poop
                foreground = colors[2],
                background = colors[0],
                fontsize = 15,
                mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('dmenu_run')}
                ),
                widget.GroupBox(
                font = "Ubuntu Bold",
                fontsize = 16,
                margin_y = 5,
                margin_x = 15,
                padding_y = 0,
                padding_x = 0,
                borderwidth = 3,
                active = colors[2],
                inactive = colors[2],
                rounded = False,
                highlight_color = colors[1],
                highlight_method = "line",
                this_current_screen_border = colors[4],
                this_screen_border = colors [4],
                other_current_screen_border = colors[0],
                other_screen_border = colors[0],
                foreground = colors[2],
                background = colors[0]
                ),
                widget.Prompt(
                prompt = prompt,
                font = "Ubuntu Mono",
                padding = 10,
                foreground = colors[3],
                background = colors[1]
                ),
                widget.Sep(
                linewidth = 0,
                padding = 20,
                foreground = colors[2],
                background = colors[0]
                ),
                widget.WindowName(
                foreground = colors[6],
                background = colors[0],
                padding = 0,
                fontsize = 14
                ),
                widget.TextBox(
                text = "",
                padding = 2,
                foreground = colors[2],
                background = colors[0],
                fontsize = 14
                ),
                widget.ThermalSensor(
                foreground = colors[2],
                background = colors[0],
                threshold = 90,
                padding = 5,
                fontsize = 14
                ),
                widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[4],
                background = colors[0],
                size_percent = 60
                ),
                widget.TextBox(
                text = "",
                padding = 2,
                foreground = colors[2],
                background = colors[0],
                fontsize = 14
                ),
                widget.Memory(
                foreground = colors[2],
                background = colors[0],
                mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
                padding = 5,
                fontsize = 14
                ),
                widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[4],
                background = colors[0],
                size_percent = 60
                ),
                widget.TextBox(
                text = '',
                foreground = colors[2],
                background = colors[0],
                padding = 0,
                fontsize = 14
                ),
                widget.Volume(
                foreground = colors[2],
                background = colors[0],
                padding = 5,
                fontsize = 14
                ),
                #widget.TextBox(
                #text = " 🔋",
                #foreground = colors[2],
                #background = colors[0],
                #padding = 0
                #),
                widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[4],
                background = colors[0],
                size_percent = 60
                ),
                widget.Battery(
                foreground = colors[2],
                background = colors[0],
                padding = 5,
                charge_char = '',
                discharge_char = '',
                format = "{percent:2.0%}",
                update_interval = 60,
                fontsize = 14
                ),
                #widget.Wlan(
                #foreground = colors[2],
                #background = colors[0]
                #),
                widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[4],
                background = colors[0],
                size_percent = 60
                ),
                widget.TextBox(
                text = '',
                foreground = colors[2],
                background = colors[0],
                padding = 3,
                fontsize = 14
                ),
                widget.Clock(
                foreground = colors[2],
                background = colors[0],
                format = "%H:%M %Y/%m/%d",
                fontsize = 14
                ),
                widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[4],
                background = colors[0],
                size_percent = 60
                ),
                widget.Systray(
                background = colors[0],
                padding = 5
                ),
                widget.CurrentLayoutIcon(
                custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                foreground = colors[0],
                background = colors[0],
                padding = 0,
                scale = 0.7
                ),
                #widget.CurrentLayout(
                #foreground = colors[2],
                #background = colors[0],
                #padding = 5,
                #fontsize = 14
                #),
                ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=28))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

#@hook.subscribe.startup_once
#def start_once():
#    home = os.path.expanduser('~')
#    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(["bash", home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
