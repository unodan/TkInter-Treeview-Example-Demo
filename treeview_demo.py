import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from sys import platform
from enum import IntEnum
from pathlib import Path
from datetime import datetime

_path = Path(__file__).cwd()

SKIP = -1
CANCEL = -2
SHIFT_KEY = 1

LAST_ROW = 990
LAST_COLUMN = 990
WHEEL_MOUSE_UP = 5
WHEEL_MOUSE_DOWN = 4


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame = ttk.Frame(self)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(sticky=tk.NSEW)

        self.app_data = {}

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.platform = 'linux' if 'linux' in platform else platform

        self.title('Treeview Demo')
        self.protocol('WM_DELETE_WINDOW', self.exit)

        self.setup()

    def setup(self):
        def setup_app():
            file = _path.joinpath('app.json')
            if file.exists():
                with open(str(file)) as f:
                    self.app_data = json.load(f)
            else:
                self.app_data = {
                    'geometry': '500x700',
                }

        def setup_treeview():
            tv_line_padding = 8
            tv_heading_padding = 5
            tv_heading_border_width = 2
            font = tkfont.nametofont('TkDefaultFont')
            self.linespace = font.metrics('linespace')
            row_height = self.linespace + tv_line_padding
            tv_indent = row_height
            self.style.configure('Treeview', rowheight=row_height)
            self.style.configure('Treeview.Heading', padding=tv_heading_padding, borderwidth=tv_heading_border_width)
            self.style.configure('Treeview', indent=tv_indent)

            self.style.configure('TEntry', selectbackground='#0081c1')
            self.style.map('Treeview', background=[('selected', '#0081c1')])

            self.style.configure('TCombobox', selectbackground='#0081c1')
            self.style.map(
                'TCombobox',
                foreground=[('readonly', 'white')],
                fieldbackground=[('readonly', '#0081c1')],
            )
            self.option_add("*TCombobox*Listbox*Background", 'white')
            self.option_add("*TCombobox*Listbox*Foreground", '#000000')

            file = _path.joinpath('treeview.json')
            if file.exists():
                with open(str(file)) as f:
                    setup = json.load(f)
            else:
                now = datetime.now()
                dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                setup = {
                    'headings': (
                        {'text': 'Name', 'anchor': tk.W},
                        {'text': 'IID', 'anchor': tk.W},
                        {'text': 'Item', 'anchor': tk.W},
                        {'text': 'Open', 'anchor': tk.W},
                        {'text': 'Tags', 'anchor': tk.W},
                        {'text': 'Size', 'anchor': tk.W},
                        {'text': 'Last Modified', 'anchor': tk.W},
                        {'text': 'Data', 'anchor': tk.W},
                    ),
                    'columns': (
                        {'width': 180, 'minwidth': 3, 'stretch': tk.NO, 'type': 'Entry', 'unique': True},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO},
                        # {'width': 120, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 120, 'minwidth': 3, 'stretch': tk.NO, 'type': 'Entry'},
                        {'width': 80, 'minwidth': 3, 'stretch': tk.NO},
                        # {'width': 130, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 130, 'minwidth': 3, 'stretch': tk.NO, 'type': 'Combobox',
                            'values': ('Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5'),
                         },
                        {'width': 180, 'minwidth': 3, 'stretch': tk.YES, 'type': 'Combobox',
                            'values': ('Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5'),
                         },
                    ),
                    'data': (
                        {'text': 'Folder 0', 'open': 1, 'values': ('', 'Node', True, '', '', dt_string, ''),
                         'children': (
                             {'text': 'photo1.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                             {'text': 'photo2.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                             {'text': 'photo3.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                             {'text': 'Folder 0_1', 'open': 1, 'values': ('', 'Node', True, '', '', dt_string, ''),
                              'children': (
                                  {'text': 'photo1.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                                  {'text': 'photo2.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                                  {'text': 'photo3.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                              )},
                         )},
                        {'text': 'Folder 1', 'open': 1, 'values': ('', 'Node', True, '', '', dt_string, ''),
                         'children': (
                             {'text': 'photo4.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                             {'text': 'photo5.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                             {'text': 'photo6.png', 'values': ('', 'Leaf', '', '', '0 Kb', dt_string, '')},
                         )},
                    ),
                }

            tree = self.treeview = Treeview(self.frame, setup=setup)
            tree.focus_set()

            settings = dict(setup.get('settings', ()))
            item = settings.get('focus')
            if (not item or not tree.exists(item)) and tree.get_children():
                item = tree.get_children()[0]

            view = settings.get('view', None)
            if view:
                self.treeview.xview('moveto', view[0])
                self.treeview.yview('moveto', view[1])

            tree.focus(item)
            tree.selection_add(item)
            tree.grid(sticky=tk.NSEW, row=0, column=0)

        setup_app()
        setup_treeview()

        self.geometry(self.app_data['geometry'])

    def exit(self):
        self.app_data.update({'geometry': self.geometry()})

        self.save()
        self.destroy()

    def save(self):
        file = _path.joinpath('app.json')
        with open(str(file), 'w') as f:
            json.dump(self.app_data, f, indent=3)

        file = _path.joinpath('treeview.json')
        with open(str(file), 'w') as f:
            data = self.treeview.serialize()
            data['settings'] = tuple({
                'view': (self.treeview.xview()[0], self.treeview.yview()[0]),
                'focus': self.treeview.focus()
            }.items())

            for idx, c in enumerate(self.treeview.columns):
                c['width'] = self.treeview.column(f'#{idx}', 'width')

            json.dump(data, f, indent=3)


class Event:
    def __init__(self):
        super().__init__()
        self.x, self.y = None, None


class DialogBase(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        title = kwargs.pop('title', '')
        resizable = kwargs.pop('resizable', (True, True))
        super().__init__(parent, **kwargs)

        self.resizable(*resizable)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.results = None
        self.container = ttk.Frame(self)
        self.container.grid(sticky=tk.NSEW)

        self.options = kwargs

        geometry = self.geometry().split('+', 1)
        _width, _height = geometry[0].split('x')
        if width:
            _width = width
        if height:
            _height = height

        self.title(title)
        self.geometry(f'{_width}x{_height}+{geometry[1]}')


class RenameDialog(DialogBase):
    def __init__(self, parent, **kwargs):
        message = kwargs.pop('message', 'No Message!')
        super().__init__(parent, **kwargs)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        frame = self.row0 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.label = ttk.Label(frame, text=message)
        self.label.grid(sticky=tk.EW, pady=(0, 10), row=0, column=0)

        self.entry = Entry(frame)
        self.entry.config(textvariable=self.entry.var)
        self.entry.grid(sticky=tk.NSEW, row=1, column=0, padx=(5, 0))
        frame.grid(row=0, sticky=tk.NSEW, padx=10, pady=(20, 0))

        frame = self.row1 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.button_rename = ttk.Button(frame, text="Rename", width=8)
        self.button_rename.grid(sticky=tk.NS + tk.E, row=0, column=0, padx=(5, 0))
        self.button_skip = ttk.Button(frame, text="Skip", width=8)
        self.button_skip.grid(sticky=tk.NS + tk.E, row=0, column=1, padx=(5, 0))
        self.button_cancel = ttk.Button(frame, text="Cancel", width=8)
        self.button_cancel.grid(sticky=tk.NS+tk.E, row=0, column=2, padx=(5, 0))

        frame.grid(row=1, sticky=tk.EW+tk.S, padx=10, pady=(10, 20))


class Text(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.origin_x = self.origin_y = 0


class Frame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.scroll_x = \
            self.scroll_y = None


class Entry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)

        self.undo_data = {}
        self.popup = None
        self.menu_background = None
        self.style = ttk.Style()

        self.setup()
        self.bindings_set()

    def setup(self):
        def set_popup_menu():
            opts = dict(self.style.map('Treeview', 'background'))
            background = self.style.lookup('Treeview.Heading', 'background')

            popup = self.popup = tk.Menu(
                self.winfo_toplevel(),
                tearoff=0,
                background=background,
                foreground='#000000',
                activebackground=opts['selected']
            )

            popup.add_command(label="Select All", command=self.select_all)
            popup.add_separator()
            popup.add_command(label="Cut", command=lambda: self.event_generate('<Control-x>'))
            popup.add_command(label="Copy", command=lambda: self.event_generate('<Control-c>'))
            popup.add_command(label="Paste", command=lambda: self.event_generate('<Control-v>'))
            popup.add_separator()
            popup.add_command(label="Delete", command=self.clear)

        self.menu_background = self.style.lookup('TScrollbar.thumb', 'background')
        set_popup_menu()

    def clear(self):
        self.delete(0, tk.END)

    def select_all(self):
        self.select_range(0, tk.END)
        self.icursor(tk.END)

    def popup_menu(self, event):
        if not self.popup:
            return

        wdg = event.widget
        wdg.focus_set()

        self.popup.tk_popup(event.x_root, event.y_root)

    def bindings_set(self):
        self.bind('<ButtonPress-3>', self.popup_menu)


class Combobox(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)

        self.popup = None
        self.menu_background = None

        self.style = ttk.Style()

        self.setup()
        self.bindings_set()

    def setup(self):
        def set_popup_menu():
            opts = dict(self.style.map('Treeview', 'background'))
            background = self.style.lookup('Treeview.Heading', 'background')

            popup = self.popup = tk.Menu(
                self.winfo_toplevel(),
                tearoff=0,
                background=background,
                foreground='#000000',
                activebackground=opts['selected']
            )

            popup.add_command(label="Select All", command=self.select_all)
            popup.add_separator()
            popup.add_command(label="Cut", command=lambda: self.event_generate('<Control-x>'))
            popup.add_command(label="Copy", command=lambda: self.event_generate('<Control-c>'))
            popup.add_command(label="Paste", command=lambda: self.event_generate('<Control-v>'))
            popup.add_separator()
            popup.add_command(label="Delete", command=self.clear)

        self.menu_background = self.style.lookup('TScrollbar.thumb', 'background')
        set_popup_menu()

    def select_all(self):
        self.select_range(0, tk.END)
        self.icursor(tk.END)

    def clear(self):
        self.var.set('')

    def popup_menu(self, event):
        if not self.popup:
            return

        wdg = event.widget
        wdg.focus_set()

        self.popup.tk_popup(event.x_root, event.y_root)

    def bindings_set(self):
        self.bind('<ButtonPress-3>', self.popup_menu)


class Label(ttk.Label):
    def __init__(self, parent, **kwargs):
        self.var = tk.StringVar()
        super().__init__(parent, textvariable=self.var, **kwargs)

        self.var.set(kwargs.get('text', ''))


class Listbox(tk.Listbox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.config(listvariable=self.var)

    def set_row_colors(self, odd, even):
        for i in range(0, len(self.get(0, tk.END))):
            color = odd if i % 2 else even
            self.itemconfig(i, {'bg': color})


class Scrollbar(ttk.Scrollbar):
    def __init__(self, parent, **kwargs):
        self.callback = kwargs.pop('callback', None)
        super().__init__(parent, **kwargs)

    def set(self, low, high):
        if float(low) > 0 or float(high) < 1:
            ttk.Scrollbar.set(self, low, high)
            self.grid()
        else:
            self.grid_remove()

        if self.callback:
            self.callback(self)


class Treeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        setup = kwargs.pop('setup', {})
        data = setup.pop('data', [])
        self.columns = setup['columns']
        self.headings = setup['headings']
        self.scroll = kwargs.pop('scroll', (True, True))

        super().__init__(self.frame, **kwargs)

        self.detached = []

        self.undo_data = {}
        self.menu_images = {}
        self.sorted_columns = {}

        self.shift = \
            self.popup = \
            self.field = \
            self.scroll_x = \
            self.scroll_y = \
            self.selected = \
            self.dlg_results = \
            self.active_popup_widget = \
            self.active_popup_column = \
            self.menu_background = None

        self.cursor_offset = 0
        self.platform = parent.winfo_toplevel().platform

        self.style = ttk.Style()
        self.indent = self.style.lookup('Treeview', 'indent')
        self.rowheight = self.style.lookup('Treeview', 'rowheight')
        self.default_font = tkfont.nametofont('TkDefaultFont')

        if setup:
            self.setup(setup)

        if data:
            self.populate('', data)

        self.bindings_set()
        self.frame.grid(sticky=tk.NSEW)

    def setup(self, data):
        def set_style():
            background = self.style.lookup("TFrame", "background")

            self.tag_configure('odd', background=background)
            self.tag_configure('even', background='#ffffff')
            self.troughcolor = self.style.lookup('TScrollbar.trough', 'troughcolor')
            self.menu_background = self.style.lookup('TScrollbar.Heading', 'background')
            self.style.configure(".", indicatorsize=self.rowheight / 2 + 1)

            font = tkfont.nametofont('TkTextFont')
            font_width = font.measure('W')
            row_height = font.metrics('linespace')
            indent = row_height + font_width

            self.style.configure('Treeview', indent=indent)

        def set_popup_menu():
            opts = dict(self.style.map('Treeview', 'background'))
            background = self.style.lookup('Treeview.Heading', 'background')

            file = _path.joinpath('images')
            if file.exists():
                for name in ('cut', 'copy', 'paste', 'delete', 'activities', 'box', 'menu_new'):
                    if Path(file.joinpath(f'{name}.png')).is_file():
                        image = tk.PhotoImage(file=Path(file.joinpath(f'{name}.png')).resolve())
                        if image:
                            self.menu_images[name] = image

            popup = self.popup = tk.Menu(
                self.winfo_toplevel(),
                tearoff=0,
                background=background,
                foreground='#000000',
                activebackground=opts['selected']
            )
            create_new = tk.Menu(
                popup,
                tearoff=0,
                background=background,
                foreground='#000000',
                activebackground=opts['selected']
            )

            popup.add_cascade(label="Insert", menu=create_new, compound=tk.LEFT, image=self.menu_images['activities'])
            popup.add_separator()
            popup.add_command(label="Cut", command=self.cut, compound=tk.LEFT, image=self.menu_images['cut'])
            popup.add_command(label="Copy", command=self.copy, compound=tk.LEFT, image=self.menu_images['copy'])
            popup.add_command(label="Paste", command=self.paste, compound=tk.LEFT, image=self.menu_images['paste'])
            popup.add_separator()
            popup.add_command(label="Delete", command=self.detach, compound=tk.LEFT, image=self.menu_images['delete'])

            create_new.add_command(
                label="Folder", command=self.insert_node, compound=tk.LEFT, image=self.menu_images['menu_new'])
            create_new.add_separator()
            create_new.add_command(
                label="Item", command=self.insert_leaf, compound=tk.LEFT, image=self.menu_images['box'])

        def set_scrollbars():
            scroll_x, scroll_y = self.scroll

            if scroll_x:
                sb_x = self.scroll_x = Scrollbar(self.frame, callback=self.popup_widget_destroy)
                sb_x.configure(command=self.xview, orient=tk.HORIZONTAL)
                sb_x.grid(sticky=tk.NSEW, row=LAST_ROW, column=0)
                self.configure(xscrollcommand=sb_x.set)

                sb_x.bind('<Button-4>', self.scrollbars_scroll)
                sb_x.bind('<Button-5>', self.scrollbars_scroll)

            if scroll_y:
                sb_y = self.scroll_y = Scrollbar(self.frame, callback=self.popup_widget_destroy)
                sb_y.configure(command=self.yview)
                self.configure(yscrollcommand=sb_y.set)
                sb_y.grid(sticky=tk.NSEW, row=0, column=LAST_COLUMN)

                sb_y.bind('<Button-4>', self.scrollbars_scroll)
                sb_y.bind('<Button-5>', self.scrollbars_scroll)

        def set_rows_columns():
            ids = []
            columns = ''
            for idx, column in enumerate(data['headings'][1:], 1):
                ids.append(f'#{idx}')
                columns += ' '.join(column['text'].lower().split()).replace(' ', '_') + ' '
            self.field = IntEnum('Columns', columns, start=0)
            self["columns"] = ids

            for idx, cfg in enumerate(data['headings']):
                self.heading(f'#{idx}', text=cfg['text'], anchor=cfg['anchor'])
                self.sorted_columns[f'#{idx}'] = True

            for idx, cfg in enumerate(data['columns']):
                self.column(f'#{idx}', width=cfg['width'], minwidth=cfg['minwidth'], stretch=cfg['stretch'])

        set_style()
        set_popup_menu()
        set_scrollbars()
        set_rows_columns()
        self.after(1, self.tags_reset)

    def next(self, item):
        if self.item(item, 'open') and self.get_children(item):
            _next = self.get_children(item)[0]
            return _next

        _next = super(Treeview, self).next(item)
        if not _next and self.next(self.parent(item)):
            _next = self.next(self.parent(item))
        return _next

    def prev(self, item):
        _prev = super(Treeview, self).prev(item)
        if not _prev:
            parent = self.parent(item)
            _prev = parent if parent else ''

        return _prev

    def tag_add(self, tags, item):
        self.tags_update('add', tags, item)

    def tag_remove(self, tags, item=None):
        self.tags_update('remove', tags, item)

    def tags_reset(self, excluded=None):
        def reset(_item):
            tags = list(self.item(_item, 'tags'))
            for _tag in tags.copy():
                if _tag not in exclude:
                    tags.pop(tags.index(_tag))
            self.item(_item, tags=tags)

            for node in self.get_children(_item):
                reset(node)

        def set_tag(_item, _tag):
            _tag = 'even' if _tag == 'odd' else 'odd'
            self.tag_add(_tag, _item)
            self.value_set(self.field.tags, str(self.item(_item, 'tags')), _item)
            if int(self.item(_item, 'open')):
                for node in self.get_children(_item):
                    _tag = set_tag(node, _tag)
            return _tag

        exclude = []
        if excluded and not isinstance(excluded, tk.Event):
            if isinstance(excluded, str):
                excluded = (excluded,)

            for item in excluded:
                if item in excluded:
                    exclude.append(item)

        tag = 'odd'
        for item in self.get_children():
            reset(item)
            tag = set_tag(item, tag)
            self.value_set(self.field.tags, str(self.item(item, 'tags')), item)

    def tag_replace(self, old, new, item=None):
        for item in (item,) if item else self.tag_has(old):
            if self.tag_has(old, item):
                self.tags_update('add', new, item)
                self.tags_update('remove', old, item)

    def tags_update(self, opt, tags, item):
        def get_items(node):
            items.append(node)
            for node in self.get_children(node):
                get_items(node)

        if not tags:
            return
        elif isinstance(tags, str):
            tags = (tags,)

        if not item:
            items = []
            for child in self.get_children():
                get_items(child)
        else:
            items = (item,)

        for item in items:
            _tags = list(self.item(item, 'tags'))
            for _tag in tags:
                if opt == 'add':
                    if _tag not in _tags:
                        _tags.append(_tag)
                elif opt == 'remove':
                    if _tag in _tags:
                        _tags.pop(_tags.index(_tag))
            self.item(item, tags=_tags)

    def value_get(self, idx, item):
        idx = int(idx)
        if not item:
            return ''
        values = list(self.item(item, 'values'))
        if 0 <= idx <= len(values):
            return values[idx]

    def value_set(self, idx, value, item):
        idx = int(idx)
        values = list(self.item(item, 'values'))
        if idx < len(values):
            values[idx] = value
            self.item(item, values=values)

    def dlg_rename(self, title, message, current_name):
        def skip(_=None):
            self.dlg_results = SKIP
            dlg.destroy()

        def cancel(_=None):
            self.dlg_results = CANCEL
            dlg.destroy()

        def rename(_=None):
            self.dlg_results = dlg.entry.var.get()
            dlg.destroy()

        root = self.winfo_toplevel()
        dlg = RenameDialog(root, width=320, height=150, title=title, message=message)
        dlg.update_idletasks()

        dlg.label.config(wraplength=dlg.winfo_width())

        dlg.entry.var.set(current_name)
        dlg.entry.select_range(0, tk.END)
        dlg.entry.icursor(tk.END)
        dlg.entry.focus()
        dlg.entry.focus_set()

        dlg.bind('<Return>', rename)
        dlg.bind('<KP_Enter>', rename)

        dlg.button_rename.bind('<Button-1>', rename)
        dlg.button_rename.bind('<Return>', rename)
        dlg.button_rename.bind('<KP_Enter>', rename)

        dlg.button_skip.bind('<Button-1>', skip)
        dlg.button_skip.bind('<Return>', skip)
        dlg.button_skip.bind('<KP_Enter>', skip)

        dlg.button_cancel.bind('<Button-1>', cancel)
        dlg.button_cancel.bind('<Return>', cancel)
        dlg.button_cancel.bind('<KP_Enter>', cancel)

        self.selection_set(self.focus())
        if self.active_popup_widget:
            x = self.active_popup_widget.winfo_rootx()
            y = self.active_popup_widget.winfo_rooty()
        else:
            bbox = self.bbox(self.focus())
            x, y, _, _ = bbox
            x += root.winfo_rootx()
            y += root.winfo_rooty()

        widest = 0
        font = self.default_font
        for node in self.get_children(self.focus()):
            size = font.measure(self.item(node, 'text'))
            if size > widest:
                widest = size + font.measure('W')

        x += (widest + font.measure('W') + self.indent * self.item_depth(self.focus()))
        y += self.rowheight + self.rowheight // 2

        dlg.geometry(f'{dlg.geometry().split("+", 1)[0]}+{x}+{y}')

        root.wait_window(dlg)

        return self.dlg_results

    def cut(self, _=None):
        def set_selections(_item):
            self.tag_add('selected', _item)
            for _item in self.get_children(_item):
                set_selections(_item)

        selections = list(self.selection())
        for item in reversed(selections):
            if self.parent(item) in selections:
                selections.pop(selections.index(item))
                self.selection_remove(item)
            else:
                set_selections(item)

        self.undo_data = {}
        for node in selections:
            self.undo_data[node] = (self.parent(node), self.index(node))

        self.detach(*selections)
        self.detached = selections

        prev = self.prev(selections[0])
        self.focus(prev)
        self.selection_add(prev)
        self.tags_reset(excluded='selected')

    def undo(self, _=None):
        for item, (parent, idx) in self.undo_data.items():
            self.reattach(item, parent, idx)
            self.selection_remove(item)
        self.tags_reset()

    def copy(self, _=None):
        def set_selected(_item):
            self.selected.append(_item)
            self.tag_add('selected', _item)
            self.value_set(self.field.tags, str(self.item(_item, 'tags')), _item)
            if not self.item(_item, 'open'):
                for node in self.get_children(_item):
                    set_selected(node)

        if not self.shift:
            for item in self.tag_has('selected'):
                self.tag_remove('selected', item)
                self.value_set(self.field.tags, str(self.item(item, 'tags')), item)

        self.selected = []
        for item in self.selection():
            set_selected(item)

    def paste(self, _=None):
        selections = self.detached if self.detached else self.selected

        if not self.selected and not self.detached:
            selections = self.tag_has('selected')

        for dst_item in self.selection():
            if not len(selections) or self.value_get(self.field.item, dst_item) != 'Node':
                continue

            if self.detached:
                for item in selections:
                    self.reattach(item, dst_item, tk.END)
                self.detached = False
            else:
                selected = {}
                for item in selections:
                    parent = self.parent(item)
                    dst = selected[parent] if parent in selected else dst_item
                    self.value_set(self.field.last_modified, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), item)

                    iid = self.insert(dst, **self.item(item))
                    if iid == SKIP:
                        continue
                    elif iid == CANCEL:
                        break
                    elif iid:
                        self.value_set(self.field.iid, iid, iid)
                        self.tag_remove('selected', iid)
                        selected[item] = iid

            self.tags_reset(excluded='selected')
            self.selection_remove(self.tag_has('selected'))
            self.selection_set(self.focus())

    def delete(self, *items):
        items = list(items)
        for item in items:
            parent = self.parent(item)
            if parent:
                value = int(self.value_get(self.field.size, parent).split(' ')[0]) - 1
                word = 'item' if value == 1 else 'items'
                self.value_set(self.field.size, f'{value} {word}', parent)

        if '' in items:
            items.pop(items.index(''))
        if items:
            super(Treeview, self).delete(*items)

    def insert(self, parent, index=tk.END, **kwargs):
        kwargs.pop('children', None)

        for idx, column in enumerate(self.columns):
            if 'unique' in column and column['unique'] and not idx:
                text = kwargs['text']
                children = self.get_children(parent)

                column_values = []
                for node in children:
                    column_values.append(self.item(node, 'text'))

                for node in children:
                    while text == self.item(node, 'text'):
                        result = self.dlg_rename(
                            'Rename',
                            f'The name "{text}" already exists, please choose another name and try again.',
                            text,
                        )
                        if result in (SKIP, CANCEL):
                            return result

                        text = result

                kwargs['text'] = text

        iid = super(Treeview, self).insert(parent, index, **kwargs)

        child_count = len(self.get_children(parent))
        if child_count:
            word = 'item' if child_count == 1 else 'items'
            self.value_set(self.field.size, f'{len(self.get_children(parent))} {word}', parent)
        self.see(iid)

        return iid

    def escape(self, _):
        self.tags_reset()
        self.selection_remove(*self.selection())
        self.selection_set(self.focus())

    def control_a(self, _):
        def select(_child):
            self.selection_add(_child)
            for node in self.get_children(_child):
                select(node)
        for child in self.get_children():
            select(child)

    def shift_up(self, _):
        rowheight = self.style.lookup('Treeview', 'rowheight')

        focus = self.focus()
        x, y, _, _ = self.bbox(focus)
        x += self.winfo_rootx()

        _prev = self.identify('item', x, y-rowheight+1)
        if _prev:
            self.see(_prev)
            self.focus(_prev)
            self.cursor_offset += 1

            if self.cursor_offset > 0:
                self.selection_toggle(_prev)
            else:
                self.selection_toggle(focus)

            return 'break'

    def shift_down(self, _):
        rowheight = self.style.lookup('Treeview', 'rowheight')
        focus = self.focus()
        x, y, _, _ = self.bbox(focus)
        x += self.winfo_rootx()

        _next = self.identify('item', x, y+rowheight+1)
        if _next:
            self.see(_next)
            self.focus(_next)
            self.cursor_offset -= 1

            if self.cursor_offset >= 0:
                self.selection_toggle(focus)
            else:
                self.selection_toggle(_next)

            return 'break'

    def key_press(self, event):
        if 'Shift' in event.keysym:
            self.shift = True
            self.cursor_offset = 0

    def key_release(self, event):
        if 'Shift' in event.keysym:
            self.shift = False

    def expand_tree(self, _):
        def func():
            item = self.identify('item', self.winfo_pointerx(), self.winfo_pointery()-self.winfo_rooty())
            self.value_set(self.field.open, True, item)
            self.tags_reset(excluded='selected')
        self.after(1, func)

    def collapse_tree(self, _=None):
        def func():
            item = self.identify('item', self.winfo_pointerx(), self.winfo_pointery()-self.winfo_rooty())
            self.value_set(self.field.open, False, item)
            self.tags_reset(excluded='selected')
        self.after(1, func)

    def column_expand(self, event):
        def get_largest_string(_children):
            _largest = 0
            idx = int(column.lstrip('#'))-1

            for child in _children:
                if column == '#0':
                    _text = self.item(child, 'text')
                elif len(self.item(child, 'values')) > 1:
                    _text = self.item(child, 'values')[idx]
                else:
                    continue

                _length = font.measure(_text) + (indent * self.item_depth(child)) if column == '#0' \
                    else font.measure(_text)

                if _length > _largest:
                    _largest = _length

                _children = self.get_children(child)
                if not _children or not int(self.item(child, 'open')):
                    continue

                _length = get_largest_string(_children)
                if _length > _largest:
                    _largest = _length

            return _largest

        region = self.identify('region', event.x, event.y)

        if region != 'separator':
            return

        largest = 0
        column = self.identify('column', event.x, event.y)
        font = tkfont.nametofont('TkTextFont')
        font_width = font.measure('W')
        row_height = font.metrics('linespace')
        indent = row_height + font_width

        for item in self.get_children():
            text = self.item(item, 'text') if column == '#0' else self.item(item, 'values')[0]
            length = font.measure(text)+indent
            largest = length if length > largest else largest

            children = self.get_children(item)
            if not children or not int(self.item(item, 'open')):
                continue

            length = get_largest_string(children)
            if length > largest:
                largest = length

        self.column(column, width=largest+font_width)

    def detach(self, *items):
        if not items:
            items = self.selection()

        self.undo_data = {}
        for item in items:
            self.undo_data[item] = (self.parent(item), self.index(item))

            parent = self.parent(item)
            if parent:
                value = int(self.value_get(self.field.size, parent).split(' ')[0]) - 1
                word = 'item' if value == 1 else 'items'
                self.value_set(self.field.size, f'{value} {word}', parent)

        item = self.prev(self.focus())

        super(Treeview, self).detach(*self.selection())

        self.focus(item)
        self.selection_add(item)
        self.tags_reset(excluded='selected')

    def reattach(self, item, parent, index):
        for idx, column in enumerate(self.columns):
            if 'unique' in column and column['unique'] and not idx:
                text = self.item(item, 'text')
                children = self.get_children(parent)

                column_values = []
                for node in children:
                    column_values.append(self.item(node, 'text'))

                for node in children:
                    while text == self.item(node, 'text'):
                        result = self.dlg_rename(
                            'Rename',
                            f'The name "{text}" already exists, please choose another '
                            f'name and try again.',
                            text,
                        )
                        if result in (SKIP, CANCEL):
                            return result

                        text = result
                        self.item(item, text=text)

        iid = self.move(item, parent, index)

        return iid

    def wheel_mouse(self, event):
        if not self.item(self.focus(), 'text'):
            self.delete(self.focus())

        value = -0.1/3 if event.num == WHEEL_MOUSE_DOWN else 0.1/3
        self.yview('moveto', self.yview()[0] + value)

        return 'break'

    def button_click(self, _):
        if isinstance(self.focus_get(), Entry):
            if not self.focus_get().var.get().strip(' '):
                self.focus_get().destroy()
                self.delete(self.focus())
                self.tags_reset()
                return
            else:
                self.item(self.focus(), text=self.focus_get().var.get())
                self.focus_get().destroy()
                return

        if self.active_popup_widget:
            item = self.focus()
            item_text = self.item(item, 'text')
            wdg_text = self.active_popup_widget.var.get().strip(' ')

            column = int(self.active_popup_column.lstrip('#'))
            unique = self.columns[column].get('unique', False)

            self.active_popup_widget.destroy()
            self.active_popup_widget = None

            if item_text == wdg_text and not item_text:
                self.delete(item)
                self.tags_reset()
                return

            if not item_text and not wdg_text:
                self.delete(item)
                self.tags_reset()
                return

            if not item_text:
                if unique:
                    for node in self.get_children(self.parent(item)):
                        if wdg_text == self.item(node, 'text'):
                            self.delete(item)
                            self.tags_reset()
                            return
                else:
                    return

            if unique:
                for node in self.get_children(self.parent(item)):
                    if wdg_text == self.item(node, 'text'):
                        return

            if not column and wdg_text:
                self.item(self.focus(), text=wdg_text)
            else:
                self.value_set(column-1, wdg_text, self.focus())

            self.active_popup_widget = None
            self.tags_reset()

    def button_release(self, event):
        self.focus(self.identify('item', event.x, event.y))

    def button_double_click(self, event):
        region = self.identify_region(event.x, event.y)

        if region == 'tree' or region == 'cell':
            row = self.identify_row(event.y)
            column = self.identify_column(event.x)

            self.active_popup_column = None
            wdg = self.active_popup_widget = self.popup_widget(row, column)
            if wdg:
                self.active_popup_column = column
                wdg.focus()
                wdg.focus_set()
                wdg.select_range(0, tk.END)

        elif region == 'separator':
            self.column_expand(event)
        elif region == 'heading':
            self.after(1, self.tags_reset)

        return 'break'

    def scrollbars_scroll(self, event):
        wdg = event.widget

        if not isinstance(wdg, Scrollbar):
            return

        if self.scroll_x and str(wdg.cget('orient')) == tk.HORIZONTAL:
            units = self.default_font.measure('W')
            if event.num == WHEEL_MOUSE_UP:
                self.xview_scroll(units, tk.UNITS)
            elif event.num == WHEEL_MOUSE_DOWN:
                self.xview_scroll(-units, tk.UNITS)
        elif self.scroll_y:
            if event.num == WHEEL_MOUSE_UP:
                self.yview_scroll(1, tk.UNITS)
            elif event.num == WHEEL_MOUSE_DOWN:
                self.yview_scroll(-1, tk.UNITS)

        return 'break'

    def item_depth(self, item):
        depth = 1
        parent = self.parent(item)
        while parent:
            depth += 1
            parent = self.parent(parent)

        return depth

    def insert_leaf(self):
        item = self.identify('item', self.popup.x, self.popup.y-self.winfo_rooty())

        if not item:
            parent = ''
            idx = tk.END
        elif self.value_get(self.field.item, item) == 'Node':
            idx = 0
            parent = item
        else:
            idx = self.index(item) + 1
            parent = self.parent(item)

        iid = self.insert(
            parent,
            idx,
            text='',
            values=('', 'Leaf', '', '', '0 Kb', datetime.now().strftime("%Y/%m/%d %H-%M-%S"), ''),
        )

        self.focus(iid)
        self.tags_reset()
        self.value_set(self.field.iid, iid, iid)
        self.popup_widget(iid, '#0')

        # wdg.focus()
        # wdg.focus_set()
        # wdg.select_range(0, tk.END)

    def insert_node(self):
        item = self.identify('item', self.popup.x, self.popup.y-self.winfo_rooty())

        if not item:
            parent = ''
            idx = tk.END
        elif self.value_get(self.field.item, item) == 'Node':
            idx = 0
            parent = item
        else:
            idx = self.index(item) + 1
            parent = self.parent(item)

        iid = self.insert(
            parent,
            idx,
            open=True,
            text='',
            values=('', 'Node', True, '', '', datetime.now().strftime("%Y/%m/%d %H:%M:%S"), ''),
        )

        self.focus(iid)
        self.value_set(self.field.iid, iid, iid)
        self.tags_reset()
        self.popup_widget(iid, '#0')

    def populate(self, parent, data=()):
        for item in data:
            iid = self.insert(parent, tk.END, **item)
            self.value_set(self.field.iid, iid, iid)

            if 'children' in item:
                self.populate(iid, item['children'])

    def serialize(self):
        def get_data(_item, _data):
            for node in self.get_children(_item):
                _item_data = self.item(node)
                _data.append(_item_data)
                if self.get_children(node):
                    _item_data['children'] = []
                    get_data(node, _item_data['children'])

        data = {'headings': self.headings, 'columns': self.columns, 'data': {}}

        tree_data = []
        for item in self.get_children():
            item_data = self.item(item)
            if self.get_children(item):
                item_data['children'] = []
                tree_data.append(item_data)
                get_data(item, item_data['children'])
            else:
                tree_data.append(item_data)

        data['data'] = tree_data

        return data

    def popup_menu(self, event):
        region = self.identify_region(event.x, event.y)
        if region == 'heading':
            return

        if self.active_popup_widget:
            self.active_popup_widget.destroy()
            self.active_popup_widget = None

        self.popup.x, self.popup.y = event.x_root, event.y_root
        item = self.identify('item', event.x, event.y)
        self.focus(item)
        self.focus_set()
        self.popup.tk_popup(event.x_root, event.y_root, 0)

    def popup_widget(self, row, column):
        if not row or not column:
            return

        bbox = self.bbox(row, column)
        if not bbox:
            return

        if self.active_popup_widget:
            self.active_popup_widget.destroy()
            self.active_popup_widget = None

        x_pos, y_pos, width, height = self.bbox(row, column)
        item = self.identify('item', x_pos, y_pos+self.rowheight)
        y_pos += height // 2

        if column == '#0':
            idx = 0
            text = self.item(item, 'text')
            x_pos += self.indent // 2
            width -= self.indent // 2 + 1
        else:
            idx = int(column.lstrip('#'))
            text = self.value_get(idx-1, item)
            x_pos += 1

        wdg = None
        mode = self.columns[idx].get('mode', tk.WRITABLE)
        unique = self.columns[idx].get('unique', False)
        _type = self.columns[idx].get('type', None)

        if _type == 'Entry':
            def tab(event):
                offset = int(column.lstrip('#'))
                column_count = len(self.field)

                if not idx and event.state & SHIFT_KEY:
                    self.active_popup_column = f'#{column_count}'
                elif offset >= column_count:
                    self.active_popup_column = '#0'
                elif 1 if event.state & 1 else 0:
                    for index in reversed(list(range(0, offset))):
                        data = self.columns[index]
                        if 'type' in data:
                            self.active_popup_column = f'#{index}'
                            break
                else:
                    for index, data in enumerate(self.columns[offset+1:], offset):
                        if 'type' in data:
                            self.active_popup_column = f'#{index+1}'
                            break

                self.active_popup_widget = _wdg = self.popup_widget(self.focus(), self.active_popup_column)

                _wdg.focus()
                _wdg.focus_set()
                _wdg.select_range(0, tk.END)

                return 'break'

            def update(_):
                _item = self.focus()
                wdg_text = wdg.var.get().strip(' ')
                item_text = self.item(_item, 'text')

                if item_text != wdg_text:
                    if not item_text and not wdg_text:
                        wdg.destroy()
                        self.active_popup_widget = None
                        self.delete(_item)
                        return

                    elif item_text and not wdg_text:
                        self.item(_item, text=item_text)
                        wdg.destroy()
                        self.active_popup_widget = None
                        self.focus_set()
                        self.focus(_item)
                        return

                    if not idx:
                        if unique:
                            parent = self.parent(_item)
                            children = self.get_children(parent)

                            column_values = []
                            for node in children:
                                column_values.append(self.item(node, 'text'))

                            for node in children:
                                while wdg_text == self.item(node, 'text'):
                                    result = self.dlg_rename(
                                        'Rename',
                                        f'The name "{wdg_text}" already exists, please choose another '
                                        f'name and try again.',
                                        wdg_text,
                                    )
                                    if result == '':
                                        continue

                                    if result in (SKIP, CANCEL):
                                        return result

                                    wdg_text = result
                                    self.item(item, text=text)

                                if wdg_text == self.item(node, 'text'):
                                    return

                        self.item(_item, text=wdg_text)
                    else:
                        self.value_set(idx-1, wdg.get(), _item)

                wdg.destroy()
                self.active_popup_widget = None
                # self.tags_reset()
                self.focus_set()
                self.selection_set(_item)

            def destroy(_=None):
                wdg.destroy()
                self.active_popup_widget = None

                _item = self.focus()
                _text = self.item(_item, 'text')
                self.tags_reset()
                if not _text:
                    self.delete(item)

                self.tags_reset()
                self.focus_set()

            def control_a(_=None):
                def func():
                    wdg.select_range(0, tk.END)
                    wdg.icursor(tk.END)
                self.after(1, func)

            def move_focus(event):
                if event.keysym == 'Up':
                    update(event)
                    _item = self.focus()

                    wdg.destroy()
                    self.active_popup_widget = None
                    self.focus_set()
                    prev = self.prev(_item)

                    if prev and event.state & 1:
                        self.selection_add(prev)
                        self.focus(prev)
                    else:
                        self.selection_set(prev)
                        self.focus(prev)

                else:
                    update(event)
                    _item = self.focus()

                    wdg.destroy()
                    self.active_popup_widget = None
                    self.focus_set()
                    _next = self.next(_item)

                    if _next and event.state & 1:
                        self.selection_add(_next)
                        self.focus(_next)
                    else:
                        self.selection_set(_next)
                        self.focus(_next)

            if mode == tk.WRITABLE:
                wdg = Entry(self)
                wdg.var.set(text)
                # wdg.icursor(tk.END)
                wdg.focus()
                wdg.focus_set()
                wdg.icursor(tk.END)
                wdg.select_range(0, tk.END)
                wdg.place(x=x_pos+4, y=y_pos, anchor='w', width=width-4)

                self.selection_remove(*self.selection())
                self.selection_set(self.focus())

                for command, callback in (
                        ('<Up>', move_focus),
                        ('<Shift-Up>', move_focus),
                        ('<Down>', move_focus),
                        ('<Shift-Down>', move_focus),
                        ('<KeyPress-Tab>', tab),
                        ('<ISO_Left_Tab>' if self.platform == 'linux' else '<Control-Shift-KeyPress-Tab>', tab),
                        ('<Return>', update),
                        ('<KP_Enter>', update),
                        ('<Escape>', destroy),
                        ('<Control-z>', destroy),
                        ('<Control-a>', control_a)):
                    wdg.bind(command, callback)

        elif _type == 'Combobox':
            def tab(event):
                offset = int(column.lstrip('#'))
                column_count = len(self.field)

                if offset >= column_count and not event.state & 1:
                    self.active_popup_column = '#0'
                elif 1 if event.state & 1 else 0:
                    for index in reversed(list(range(0, offset))):
                        data = self.columns[index]
                        if 'type' in data:
                            self.active_popup_column = f'#{index}'
                            break
                else:
                    for index, data in enumerate(self.columns[offset+1:], offset):
                        if 'type' in data:
                            self.active_popup_column = f'#{index+1}'
                            break

                self.active_popup_widget = self.popup_widget(self.focus(), self.active_popup_column)
                self.active_popup_widget.focus()
                self.active_popup_widget.focus_set()
                self.active_popup_widget.select_range(0, tk.END)

                return 'break'

            def update(_):
                _text = wdg.get().strip(' ')
                if not idx:
                    self.item(self.focus(), text=_text)
                else:
                    self.value_set(idx-1, _text, self.focus())
                destroy()
                self.focus_set()

            def destroy(_=None):
                wdg.destroy()
                self.active_popup_widget = None
                self.focus_set()

            def control_a(_=None):
                def func():
                    wdg.select_range(0, tk.END)
                    wdg.icursor(tk.END)
                self.after(1, func)

            state = '' if mode == tk.WRITABLE else 'readonly'
            values = self.columns[idx].get('values', '')
            wdg = Combobox(self, state=state, values=values)
            wdg.place(x=x_pos, y=y_pos, anchor='w', width=width-2)

            wdg.var.set(text)
            wdg.icursor(tk.END)
            wdg.select_range(0, tk.END)

            self.selection_remove(*self.selection())
            self.selection_set(self.focus())

            for command, callback in (
                    ('<KeyPress-Tab>', tab),
                    ('<ISO_Left_Tab>' if self.platform == 'linux' else '<Control-Shift-KeyPress-Tab>', tab),
                    ('<Return>', update),
                    ('<KP_Enter>', update),
                    ('<Escape>', destroy),
                    ('<Control-z>', destroy),
                    ('<Control-a>', control_a)):
                wdg.bind(command, callback)

        return wdg

    def popup_widget_edit(self, _):
        self.active_popup_widget = self.popup_widget(self.focus(), '#0')
        if self.active_popup_widget:
            self.active_popup_widget.select_range(0, tk.END)
            self.active_popup_widget.icursor(tk.END)
            self.active_popup_widget.focus_set()
            self.active_popup_column = '#0'

        return 'break'

    def popup_widget_destroy(self, _):
        if self.active_popup_widget:
            self.active_popup_widget.destroy()
            self.active_popup_widget = None

    def bindings_set(self):
        for command, callback in (
                ('<Up>', self.popup_widget_destroy),
                ('<Down>', self.popup_widget_destroy),
                ('<Key>', self.key_press),
                ('<Tab>', self.popup_widget_edit),
                ('<Escape>', self.escape),
                ('<Return>', self.popup_widget_edit),
                ('<KP_Enter>', self.popup_widget_edit),
                ('<Button-1>', self.button_click),
                ('<Button-4>', self.wheel_mouse),
                ('<Button-5>', self.wheel_mouse),
                ('<Shift-Up>', self.shift_up),
                ('<Shift-Down>', self.shift_down),
                ('<Control-a>', self.control_a),
                ('<Control-x>', self.cut),
                ('<Control-c>', self.copy),
                ('<Control-v>', self.paste),
                ('<Control-z>', self.undo),
                ('<KeyRelease>', self.key_release),
                ('<ButtonPress-3>', self.popup_menu),
                ('<Double-Button-1>', self.button_double_click),
                ('<ButtonRelease-1>', self.button_release),
                ('<<TreeviewOpen>>', self.expand_tree),
                ('<<TreeviewClose>>', self.collapse_tree)):
            self.bind(command, callback)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()