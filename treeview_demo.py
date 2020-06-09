import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from datetime import datetime
from os import path, makedirs
ABS_PATH = path.dirname(path.realpath(__file__))

_IID = 0
_TYPE = 1
_OPEN = 2
_TAGS = 3
_MODIFIED = 4
_DATA1 = 5


def dump(data, indent=None):
    if not isinstance(data, dict):
        print('Value:', data)
        return

    indent = indent if indent else '.'

    print('-------------------------------------------------------------------------------------------------------')
    if data:
        def walk(_data, count):
            count += 1
            for key, value in _data.items():
                if isinstance(value, dict):
                    print(indent * count, key)
                    walk(value, count)
                else:
                    if isinstance(value, str):
                        value = f'"{value}"'
                    print(indent * count, key, f'value={value}')

        walk(data, 0)
    else:
        print(' (No Data)')

    print('-------------------------------------------------------------------------------------------------------')


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

        self.title('Treeview Demo')
        self.protocol('WM_DELETE_WINDOW', self.exit)

        self.setup()

    def setup(self):
        def setup_app():
            file = path.join(ABS_PATH, 'app.json')
            if path.exists(file):
                with open(file) as f:
                    self.app_data = json.load(f)
            else:
                self.app_data = {
                    'geometry': '500x700',
                    'treeview': {
                        'type': 'Treeview',
                        'settings': (
                            ('columns', {
                                'widths': [100, 100, 100]
                            }),
                        ),
                    }
                }

        def setup_treeview():
            tv_line_padding = 8
            tv_heading_padding = 5
            tv_heading_border_width = 2
            font = tkfont.nametofont('TkDefaultFont')
            font_width = font.measure('W')
            self.linespace = font.metrics('linespace')
            row_height = self.linespace + tv_line_padding
            tv_indent = row_height+font_width
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

            file = path.join(ABS_PATH, 'treeview.json')
            if path.exists(file):
                with open(file) as f:
                    data = json.load(f)
            else:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                data = {
                    'headings': (
                        {'text': 'Name', 'anchor': tk.W},
                        {'text': 'IID', 'anchor': tk.W},
                        {'text': 'Item', 'anchor': tk.W},
                        {'text': 'Open', 'anchor': tk.W},
                        {'text': 'Tags', 'anchor': tk.W},
                        {'text': 'Last Modified', 'anchor': tk.W},
                        {'text': 'Data', 'anchor': tk.W},
                    ),
                    'columns': (
                        {'width': 180, 'minwidth': 3, 'stretch': tk.NO, 'type': 'Entry', 'unique': True},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO, 'mode': tk.READABLE},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO, 'mode': tk.READABLE},
                        {'width': 70, 'minwidth': 3, 'stretch': tk.NO, 'mode': tk.READABLE},
                        {'width': 120, 'minwidth': 3, 'stretch': tk.NO, 'mode': tk.READABLE},
                        {'width': 100, 'minwidth': 3, 'stretch': tk.NO, 'mode': tk.READABLE},
                        {'width': 180, 'minwidth': 3, 'stretch': tk.YES, 'type': 'Combobox',
                            'values': (' Value 1 ', ' Value 2 ', ' Value 3 ', ' Value 4 ', ' Value 5 '),
                         },
                    ),
                    'data': (
                        {'text': 'Folder 0', 'open': 1, 'values': ('', 'Node', True, '', dt_string, ''),
                         'children': (
                             {'text': 'photo1.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                             {'text': 'photo2.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                             {'text': 'photo3.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                             {'text': 'Folder 0_1', 'open': 1, 'values': ('', 'Node', True, '', dt_string, ''),
                              'children': (
                                  {'text': 'photo1.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                                  {'text': 'photo2.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                                  {'text': 'photo3.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                              )},
                         )},
                        {'text': 'Folder 1', 'open': 1, 'values': ('', 'Node', True, '', dt_string, ''),
                         'children': (
                             {'text': 'photo4.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                             {'text': 'photo5.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                             {'text': 'photo6.png', 'values': ('', 'Leaf', '', '', dt_string, '')},
                         )},
                    )
                }

            tree = self.treeview = Treeview(self.frame, setup=data)
            tree.focus_set()

            settings = dict(self.app_data['treeview']['settings'])

            item = settings.get('focus', None)
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
        settings = dict(self.app_data['treeview']['settings'])
        settings['view'] = (self.treeview.xview()[0], self.treeview.yview()[0])
        settings['focus'] = self.treeview.focus()

        self.app_data['treeview']['settings'] = tuple(settings.items())

        self.save()
        self.destroy()

    def save(self):
        file = path.join(ABS_PATH, 'app.json')
        if file:
            dirname = path.dirname(file)
            if not path.exists(dirname):
                makedirs(dirname)

            with open(file, 'w') as f:
                json.dump(self.app_data, f, indent=3)

        file = path.join(ABS_PATH, 'treeview.json')
        if file:
            dirname = path.dirname(file)
            if not path.exists(dirname):
                makedirs(dirname)

            with open(file, 'w') as f:
                data = self.treeview.serialize()
                for idx, c in enumerate(self.treeview.columns):
                    c['width'] = self.treeview.column(f'#{idx}', 'width')
                    # if 'mode' in c:
                    #     data['columns'][idx]['mode'] = self.treeview.columns[idx]['mode']

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

        self.container = ttk.Frame(self)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
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


class MessageDialog(DialogBase):
    def __init__(self, parent, **kwargs):
        message = kwargs.pop('message', '')
        super().__init__(parent, **kwargs)

        frame = self.row0 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.label = ttk.Label(frame, text=message)
        self.label.grid(sticky=tk.NSEW, pady=5, row=0, column=0)
        frame.grid(sticky=tk.EW, padx=10, pady=(20, 0))

        frame = self.row1 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.button_ok = ttk.Button(frame, text="Okay")
        self.button_ok.grid(sticky=tk.NS + tk.E, row=0, column=0, padx=(5, 0))
        frame.grid(row=1, sticky=tk.EW, padx=10, pady=(10, 20))


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
        self.popup = \
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
        bindings = {
            '<ButtonPress-3>': self.popup_menu,
        }
        for command, callback in bindings.items():
            self.bind(command, callback)


class Combobox(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)

        self.popup = \
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
        bindings = {
            '<ButtonPress-3>': self.popup_menu,
        }
        for command, callback in bindings.items():
            self.bind(command, callback)


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
            self.callback('scrollbar')


class Treeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        setup = kwargs.pop('setup', {})
        data = setup.pop('data', [])
        self.cursor = setup.pop('cursor', [0, 0])
        self.columns = setup['columns']
        self.headings = setup['headings']
        self.scroll = kwargs.pop('scroll', (True, True))

        super().__init__(self.frame, **kwargs)

        self.detached = []
        self.undo_data = {}
        self.shift = \
            self.popup = \
            self.selected = \
            self.menu_background = \
            self.active_cell = \
            self.cursor_offset = \
            self.scroll_x = \
            self.scroll_y = None

        self.style = ttk.Style()

        if setup:
            self.setup(setup)

        if data:
            self.populate('', data)

        self.indent = self.style.lookup('Treeview', 'indent')
        self.rowheight = self.style.lookup('Treeview', 'rowheight')
        self.bindings_set()
        self.frame.grid(sticky=tk.NSEW)

    def setup(self, data):
        def set_style():
            background = self.style.lookup("TFrame", "background")

            self.tag_configure('odd', background=background)
            self.tag_configure('even', background='#ffffff')
            self.troughcolor = self.style.lookup('TScrollbar.trough', 'troughcolor')
            self.menu_background = self.style.lookup('TScrollbar.Heading', 'background')

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
            create_new = tk.Menu(
                popup,
                tearoff=0,
                background=background,
                foreground='#000000',
                activebackground=opts['selected']
            )

            popup.add_cascade(label="Insert", menu=create_new)
            popup.add_separator()
            popup.add_command(label="Cut", command=self.cut)
            popup.add_command(label="Copy", command=self.copy)
            popup.add_command(label="Paste", command=self.paste)
            popup.add_separator()
            popup.add_command(label="Delete", command=self.detach)

            create_new.add_command(label="Item", command=self.insert_leaf)
            create_new.add_separator()
            create_new.add_command(label="Folder", command=self.insert_node)

        def set_scrollbars():
            scroll_x, scroll_y = self.scroll

            if scroll_x:
                sb_x = self.scroll_x = Scrollbar(self.frame)
                sb_x.configure(command=self.xview, orient=tk.HORIZONTAL)
                sb_x.grid(sticky=tk.NSEW, row=980, column=0)
                self.configure(xscrollcommand=sb_x.set)

            if scroll_y:
                sb_y = self.scroll_y = Scrollbar(self.frame)
                sb_y.configure(command=self.yview)
                self.configure(yscrollcommand=sb_y.set)
                sb_y.grid(sticky=tk.NSEW, row=0, column=990)

        def set_rows_columns():
            ids = []
            columns = len(data['columns'])
            for column in range(1, columns):
                ids.append(f'#{column}')
            self["columns"] = ids

            for idx, cfg in enumerate(data['headings']):
                _id = cfg['column'] if 'column' in cfg else f'#{idx}'
                self.heading(_id, text=cfg['text'], anchor=cfg['anchor'])

            for idx, cfg in enumerate(data['columns']):
                _id = cfg['column'] if 'column' in cfg else f'#{idx}'
                self.column(_id, width=cfg['width'], minwidth=cfg['minwidth'], stretch=cfg['stretch'])

        set_style()
        set_popup_menu()
        set_scrollbars()
        set_rows_columns()
        self.after(1, self.tags_reset)

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
            self.value_set(_TAGS, str(self.item(_item, 'tags')), _item)
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
            self.value_set(_TAGS, str(self.item(item, 'tags')), item)

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
        if not item:
            return ''
        values = list(self.item(item, 'values'))
        if 0 <= idx <= len(values):
            return values[idx]

    def value_set(self, idx, value, item):
        values = list(self.item(item, 'values'))
        values[idx] = value
        self.item(item, values=values)

    def dlg_message(self, title, message):
        def ok(_=None):
            dlg.destroy()

        root = self.winfo_toplevel()
        dlg = MessageDialog(root, width=320, height=130, title=title, message=message)
        dlg.update_idletasks()
        dlg.label.config(wraplength=dlg.container.winfo_width())
        dlg.button_ok.focus()

        dlg.button_ok.config(command=ok)
        dlg.button_ok.bind('<Return>', ok)
        dlg.button_ok.bind('<KP_Enter>', ok)

        x = self.active_cell.winfo_rootx()
        y = self.active_cell.winfo_rooty()
        item = self.identify('item', x, y-self.winfo_rooty())

        widest = 0
        font = tkfont.nametofont('TkDefaultFont')
        for node in self.get_children(self.parent(item)):
            size = font.measure(self.item(node, 'text'))
            if size > widest:
                widest = size + font.measure('W')

        x += widest
        y += self.rowheight + self.rowheight // 2

        dlg.geometry(f'{dlg.geometry().split("+", 1)[0]}+{x}+{y}')

        root.wait_window(dlg)

    def select(self, _):
        item = self.identify('item', self.winfo_pointerx(), self.winfo_pointery() - self.winfo_rooty())
        self.focus(item)

    def expand(self, _):
        def func():
            item = self.identify('item', self.winfo_pointerx(), self.winfo_pointery()-self.winfo_rooty())
            self.value_set(_OPEN, True, item)
            self.tags_reset(excluded='selected')
        self.after(1, func)

    def collapse(self, _=None):
        def func():
            item = self.identify('item', self.winfo_pointerx(), self.winfo_pointery()-self.winfo_rooty())
            self.value_set(_OPEN, False, item)
            self.tags_reset(excluded='selected')
        self.after(1, func)

    def widget_popup(self, row, column):
        bbox = self.bbox(row, column)
        if not bbox:
            return

        x, y, width, height = self.bbox(row, column)
        item = self.identify('item', x, y+self.rowheight)
        y += height // 2

        if column == '#0':
            col = 0
            text = self.item(item, 'text')
            x += self.indent / 2
            width -= self.indent / 2 + 1
        else:
            col = int(column.lstrip('#'))
            text = self.value_get(col-1, item)
            x += 1

        wdg = None
        mode = self.columns[col].get('mode', tk.WRITABLE)
        unique = self.columns[col].get('unique', False)
        _type = self.columns[col].get('type', None)

        if _type == 'Combobox':
            def enter(_):
                _text = wdg.get().strip(' ')
                if not col:
                    self.item(self.focus(), text=_text)
                else:
                    self.value_set(col-1, _text, self.focus())
                destroy()

            def destroy(_=None):
                wdg.destroy()
                self.active_cell = None

            def control_a(_=None):
                def func():
                    wdg.select_range(0, tk.END)
                    wdg.icursor(tk.END)
                self.after(1, func)

            state = '' if mode == tk.WRITABLE else 'readonly'
            values = self.columns[col].get('values', '')
            wdg = Combobox(self, state=state, values=values)
            wdg.place(x=x-1, y=y, anchor='w', width=width)
            wdg.var.set(text)
            wdg.icursor(tk.END)

            wdg.bind('<Return>', enter)
            wdg.bind('<KP_Enter>', enter)
            wdg.bind('<Escape>', destroy)
            wdg.bind('<Control-z>', destroy)
            wdg.bind('<Control-a>', control_a)

        elif _type == 'Entry':
            def enter(_):
                _item = self.focus()
                wdg_text = wdg.var.get().strip(' ')
                item_text = self.item(_item, 'text')

                if item_text != wdg_text:

                    if not item_text and not wdg_text:
                        wdg.destroy()
                        self.active_cell = None
                        self.delete(_item)
                        return

                    elif item_text and not wdg_text:
                        self.item(_item, text=item_text)
                        wdg.destroy()
                        self.active_cell = None
                        return

                    if not col:
                        if unique:
                            parent = self.parent(_item)
                            for node in self.get_children(parent):
                                if wdg_text == self.item(node, 'text'):
                                    self.dlg_message(
                                        'Duplicate Name',
                                        f'The name "{wdg_text}" already exists, please choose another name and try again.')
                                    return

                        self.item(_item, text=wdg_text)
                    else:
                        self.value_set(col-1, wdg.get(), _item)

                wdg.destroy()
                self.active_cell = None
                self.tags_reset()
                self.selection_set(_item)

            def destroy(_=None):
                wdg.destroy()
                self.active_cell = None

                _item = self.focus()
                _text = self.item(_item, 'text')
                self.tags_reset()
                if not _text:
                    self.delete(item)
                self.tags_reset()

            def control_a(_=None):
                def func():
                    wdg.select_range(0, tk.END)
                    wdg.icursor(tk.END)
                self.after(1, func)

            if mode == tk.WRITABLE:
                wdg = Entry(self)
                wdg.place(x=x-1, y=y, anchor='w', width=width)
                wdg.var.set(text)
                wdg.icursor(tk.END)

                wdg.bind('<Return>', enter)
                wdg.bind('<KP_Enter>', enter)
                wdg.bind('<Escape>', destroy)
                wdg.bind('<Control-z>', destroy)
                wdg.bind('<Control-a>', control_a)

        return wdg

    def wheel_mouse(self, event):
        if self.active_cell:
            self.active_cell.destroy()
            self.active_cell = None

            if not self.item(self.focus(), 'text'):
                self.delete(self.focus())

        value = 0.1 if event.num == 5 else -0.1
        self.yview('moveto', self.yview()[0] + value)

        return 'break'

    def single_click(self, _):
        if self.active_cell:
            item = self.focus()
            item_text = self.item(item, 'text')
            wdg_text = self.active_cell.var.get().strip(' ')

            column = int(self.active_cell.column.lstrip('#'))
            unique = self.columns[column].get('unique', False)

            self.active_cell.destroy()
            self.active_cell = None

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

            self.active_cell = None
            self.tags_reset()

    def double_click(self, event):
        row = self.identify_row(event.y)
        column = self.identify_column(event.x)

        self.active_cell = self.widget_popup(row, column)
        if self.active_cell:
            self.active_cell.column = column
            self.active_cell.focus()
            if isinstance(self.active_cell, Entry):
                self.active_cell.select_range(0, tk.END)

        return 'break'

    def button_release(self, event):
        self.focus(self.identify('item', event.x, event.y))

    def cut(self, _=None):
        def set_selections(_item):
            self.tag_add('selected', _item)
            for _item in self.get_children(_item):
                set_selections(_item)

        selections = list(self.selection())
        for item in reversed(selections):
            if self.parent(item) in selections:
                selections.pop(selections.index(item))
            else:
                set_selections(item)

        item = self.focus()
        item = self.prev(item)

        if not item and self.get_children():
            item = self.get_children()[0]

        self.undo_data = {}
        for node in selections:
            self.undo_data[node] = (self.parent(node), self.index(node))

        self.detach(*selections)
        self.detached = selections

        self.focus(item)
        self.selection_add(item)
        self.tags_reset(excluded='selected')

    def copy(self, _=None):
        def set_selected(_item, copy_all=False):
            self.selected.append(_item)
            self.tag_add('selected', _item)
            self.value_set(_TAGS, str(self.item(_item, 'tags')), _item)
            if not self.item(_item, 'open') or copy_all:
                for node in self.get_children(_item):
                    set_selected(node, True)

        if not self.shift:
            for item in self.tag_has('selected'):
                self.tag_remove('selected', item)
                self.value_set(_TAGS, str(self.item(item, 'tags')), item)

        self.selected = []
        for item in self.selection():
            set_selected(item)

    def undo(self, _=None):
        for item, (parent, idx) in self.undo_data.items():
            self.reattach(item, parent, idx)
            self.selection_remove(item)
        self.tags_reset()

    def paste(self, _=None):
        selections = self.detached if self.detached else self.selected

        if not self.selected and not self.detached:
            selections = self.tag_has('selected')

        for dst_item in self.selection():
            if not len(selections) or self.value_get(_TYPE, dst_item) != 'Node':
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
                    self.value_set(_MODIFIED, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), item)

                    iid = self.insert(dst, **self.item(item))
                    self.value_set(_IID, iid, iid)
                    self.tag_remove('selected', iid)
                    selected[item] = iid

            self.tags_reset(excluded='selected')
            self.selection_remove(self.tag_has('selected'))
            self.selection_set(self.focus())

    def detach(self, *selections):
        if not selections:
            selections = self.selection()

        self.undo_data = {}
        for item in selections:
            self.undo_data[item] = (self.parent(item), self.index(item))

        item = self.focus()
        item = self.prev(item)

        super(Treeview, self).detach(*self.selection())

        self.focus(item)
        self.selection_add(item)
        self.tags_reset(excluded='selected')

    def insert(self, parent, index=tk.END, **kwargs):
        kwargs.pop('children', None)
        iid = super(Treeview, self).insert(parent, index, **kwargs)
        self.see(iid)
        return iid

    def insert_leaf(self):
        item = self.identify('item', self.popup.x, self.popup.y-self.winfo_rooty())

        if not item:
            parent = ''
            idx = tk.END
        elif self.value_get(_TYPE, item) == 'Node':
            idx = 0
            parent = item
        else:
            idx = self.index(item) + 1
            parent = self.parent(item)

        iid = self.insert(
            parent,
            idx,
            values=['', 'Leaf', '', '', datetime.now().strftime("%d/%m/%Y %H:%M:%S"), '']
        )

        self.focus(iid)
        self.value_set(_IID, iid, iid)
        self.tags_reset()

        bbox = self.bbox(iid, '#0')
        if bbox:
            event = Event()
            event.x = bbox[0]
            event.y = bbox[1] + self.rowheight
            self.double_click(event)

    def insert_node(self):
        item = self.identify('item', self.popup.x, self.popup.y-self.winfo_rooty())

        if not item:
            parent = ''
            idx = tk.END
        elif self.value_get(_TYPE, item) == 'Node':
            idx = 0
            parent = item
        else:
            idx = self.index(item) + 1
            parent = self.parent(item)

        iid = self.insert(
            parent,
            idx,
            open=True,
            values=['', 'Node', '', '', datetime.now().strftime("%d/%m/%Y %H:%M:%S"), '']
        )

        self.focus(iid)
        self.value_set(_IID, iid, iid)
        self.tags_reset()

        bbox = self.bbox(iid, '#0')
        if bbox:
            event = Event()
            event.x = bbox[0]
            event.y = bbox[1] + self.rowheight
            self.double_click(event)

    def next(self, item):
        _next = super(Treeview, self).next(item)

        return _next

    def prev(self, item):
        _prev = super(Treeview, self).prev(item)
        if not _prev:
            parent = self.parent(item)
            _prev = parent if parent else ''

        return _prev

    def control_a(self, _):
        def select(_child):
            self.selection_add(_child)
            for node in self.get_children(_child):
                select(node)
        for child in self.get_children():
            select(child)

    def key_press(self, event):
        if 'Shift' in event.keysym:
            self.shift = True
            self.cursor_offset = 0

    def key_release(self, event):
        if 'Shift' in event.keysym:
            self.shift = False

    def escape(self, _):
        self.tags_reset()
        self.selection_remove(*self.selection())
        self.selection_set(self.focus())

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

    def populate(self, parent, data=()):
        for item in data:
            iid = self.insert(parent, tk.END, **item)
            self.value_set(_IID, iid, iid)

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
        if self.active_cell:
            self.active_cell.destroy()
            self.active_cell = None

        self.popup.x, self.popup.y = event.x_root, event.y_root
        item = self.identify('item', event.x, event.y)
        self.focus(item)
        self.focus_set()
        self.popup.tk_popup(event.x_root, event.y_root, 0)

    def bindings_set(self):
        bindings = {
            '<Key>': self.key_press,
            '<KeyRelease>': self.key_release,
            '<Double-Button-1>': self.double_click,
            '<Button-1>': self.single_click,
            '<Button-4>': self.wheel_mouse,
            '<Button-5>': self.wheel_mouse,
            '<ButtonRelease-1>': self.button_release,
            '<Escape>': self.escape,
            # '<Escape>': self.tags_reset,
            '<Shift-Up>': self.shift_up,
            '<Shift-Down>': self.shift_down,
            '<Control-a>': self.control_a,
            '<Control-x>': self.cut,
            '<Control-c>': self.copy,
            '<Control-v>': self.paste,
            '<Control-z>': self.undo,
            '<ButtonPress-3>': self.popup_menu,
            # '<<TreeviewSelect>>': self.select,
            '<<TreeviewOpen>>': self.expand,
            '<<TreeviewClose>>': self.collapse,
        }
        for command, callback in bindings.items():
            self.bind(command, callback)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
