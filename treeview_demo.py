import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from datetime import datetime
from os import path, makedirs
ABS_PATH = path.dirname(path.realpath(__file__))


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

        self.title('Default Demo')
        self.style = ttk.Style()
        self.style.theme_use('clam')
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
            font = tkfont.nametofont('TkDefaultFont')
            self.linespace = font.metrics('linespace')
            rowheight = self.linespace + tv_line_padding
            self.style.configure('Treeview', rowheight=rowheight)
            self.style.configure('Treeview.Heading', padding=tv_heading_padding)

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
                        {'text': 'Date Modified', 'anchor': tk.W},
                        {'text': 'Type', 'anchor': tk.W},
                        {'text': 'Size', 'anchor': tk.W},
                    ),
                    'columns': (
                        {'width': 180, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 80, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 120, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 100, 'minwidth': 3, 'stretch': tk.NO},
                        {'width': 100, 'minwidth': 3, 'stretch': tk.YES},
                    ),
                    'data': (
                        {'text': 'Folder 0', 'open': 1, 'values': ('', dt_string, "Folder", ""),
                         'children': (
                             {'text': 'photo1.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                             {'text': 'photo2.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                             {'text': 'photo3.png', 'values': ('', dt_string, 'Item', "2.7 KB")},
                             {'text': 'Folder 0_1', 'open': 1, 'values': ('', dt_string, "Folder", ""),
                              'children': (
                                  {'text': 'photo1.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                                  {'text': 'photo2.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                                  {'text': 'photo3.png', 'values': ('', dt_string, 'Item', "2.8 KB")},
                              )},
                         )},
                        {'text': 'Folder 1', 'open': 1, 'values': ('', dt_string, "Folder", ""),
                         'children': (
                             {'text': 'photo4.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                             {'text': 'photo5.png', 'values': ('', dt_string, 'Item', "2.6 KB")},
                             {'text': 'photo6.png', 'values': ('', dt_string, 'Item', "2.9 KB")},
                         )},
                    )
                }

            tree = self.treeview = Treeview(self.frame, selectmode=tk.EXTENDED, setup=data)
            tree.grid(sticky=tk.NSEW, row=0, column=0)

        setup_app()
        setup_treeview()

        self.geometry(self.app_data['geometry'])

    def exit(self):
        self.app_data.update({'geometry': self.geometry()})

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
                json.dump(self.treeview.serialize(), f, indent=3)


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

        self.options = kwargs

        geometry = self.geometry().split('+', 1)
        _width, _height = geometry[0].split('x')
        if width:
            _width = width
        if height:
            _height = height

        self.title(title)
        self.geometry(f'{_width}x{_height}+{geometry[1]}')


class AddNodeDialog(DialogBase):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.container = ttk.Frame(self)
        self.container.rowconfigure(1, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.grid(sticky=tk.NSEW)

        frame = self.row0 = ttk.Frame(self.container)
        frame.columnconfigure(1, weight=1)
        self.label = ttk.Label(frame, text="Name")
        self.label.grid(sticky=tk.NSEW, row=0, column=0)
        self.entry = Entry(frame, width=30)
        self.entry.config(textvariable=self.entry.var)
        self.entry.grid(sticky=tk.NSEW, row=0, column=1, padx=(5, 0))
        frame.grid(sticky=tk.EW, padx=10, pady=(20, 0))

        frame = self.row1 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.button_ok = ttk.Button(frame, text="Ok")
        self.button_ok.grid(sticky=tk.NS + tk.E, row=0, column=0, padx=(5, 0))
        self.button_cancel = ttk.Button(frame, text="Cancel")
        self.button_cancel.grid(sticky=tk.NS+tk.E, row=0, column=1, padx=(5, 0))
        frame.grid(sticky=tk.EW+tk.S, padx=10, pady=(10, 20))


class AddLeafDialog(DialogBase):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.container = ttk.Frame(self)
        self.container.rowconfigure(1, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.grid(sticky=tk.NSEW)

        frame = self.row0 = ttk.Frame(self.container)
        frame.columnconfigure(1, weight=1)
        self.label = ttk.Label(frame, text="Name")
        self.label.grid(sticky=tk.NSEW, row=0, column=0)
        self.entry = Entry(frame, width=30)
        self.entry.config(textvariable=self.entry.var)
        self.entry.grid(sticky=tk.NSEW, row=0, column=1, padx=(5, 0))
        frame.grid(sticky=tk.EW, padx=10, pady=(20, 0))

        frame = self.row1 = ttk.Frame(self.container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.button_ok = ttk.Button(frame, text="Ok")
        self.button_ok.grid(sticky=tk.NS + tk.E, row=0, column=0, padx=(5, 0))
        self.button_cancel = ttk.Button(frame, text="Cancel")
        self.button_cancel.grid(sticky=tk.NS+tk.E, row=0, column=1, padx=(5, 0))
        frame.grid(sticky=tk.EW+tk.S, padx=10, pady=(10, 20))


class Text(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.origin_x = self.origin_y = 0


class Entry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)


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


class Treeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        setup = kwargs.pop('setup', {})
        data = setup.pop('data', [])
        super().__init__(parent, **kwargs)

        self.detached = []
        self.popup = None
        self.selected = None
        self.header_height = None

        self.style = ttk.Style()

        if setup:
            self.setup(setup)

        if data:
            self.populate('', data)

        self.bindings_set()

    def setup(self, data):
        def set_style():
            background = self.style.lookup("TFrame", "background")

            self.tag_configure('odd', background=background)
            self.tag_configure('even', background='#ffffff')

        def set_popup_menu():
            popup = self.popup = tk.Menu(self.winfo_toplevel(), tearoff=0)
            create_new = tk.Menu(popup, tearoff=0)

            popup.add_cascade(label="Create New", menu=create_new)
            popup.add_separator()
            popup.add_command(label="Cut", command=self.cut)
            popup.add_command(label="Copy", command=self.copy)
            popup.add_command(label="Paste", command=self.paste)
            popup.add_separator()
            popup.add_command(label="Delete", command=self.delete)
            popup.add_separator()
            popup.add_command(label="Rename", )

            create_new.add_command(label="Item", command=self.add_leaf)
            create_new.add_separator()
            create_new.add_command(label="Folder", command=self.add_folder)

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
        set_rows_columns()
        self.set_row_colors()

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

    def value_update(self, idx, value, item):
        values = list(self.item(item, 'values'))
        values[idx] = value
        self.item(item, values=values)

    def add_leaf(self):
        def ok():
            text = dlg.entry.get().strip(' ')
            if text:
                now = datetime.now()
                iid = self.insert(
                    self.focus(),
                    text=text,
                    values=['', now.strftime("%d/%m/%Y %H:%M:%S"), 'Item', '3.5Mb']
                )
                self.value_update(0, iid, iid)
                self.tags_reset()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        root = self.winfo_toplevel()
        dlg = AddLeafDialog(root, width=300, height=110, title='Add Item')

        dlg.button_ok.config(command=ok)
        dlg.button_cancel.config(command=cancel)
        dlg.entry.focus_set()
        dlg.update_idletasks()

        if hasattr(self.popup, 'x') and hasattr(self.popup, 'y'):
            dlg.geometry(f'{dlg.geometry().split("+", 1)[0]}+{self.popup.x}+{self.popup.y}')

        root.wait_window(self)

    def add_folder(self):
        def ok():
            text = dlg.entry.get().strip(' ')
            if text:
                now = datetime.now()
                iid = self.insert(
                    self.focus(),
                    text=text,
                    values=['', now.strftime("%d/%m/%Y %H:%M:%S"), 'Folder', '']
                )
                self.value_update(0, iid, iid)
                self.item(iid, open=1)
                self.tags_reset()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        root = self.winfo_toplevel()
        dlg = AddLeafDialog(root, width=300, height=110, title='Add Folder')

        dlg.button_ok.config(command=ok)
        dlg.button_cancel.config(command=cancel)
        dlg.entry.focus_set()
        dlg.update_idletasks()

        if hasattr(self.popup, 'x') and hasattr(self.popup, 'y'):
            dlg.geometry(f'{dlg.geometry().split("+", 1)[0]}+{self.popup.x}+{self.popup.y}')

        root.wait_window(self)

    def set_row_colors(self, _=None):
        self.after(1, self.tags_reset)

    def cut(self, _=None):
        selections = list(self.selection())
        for item in reversed(selections):
            if self.parent(item) in selections:
                selections.pop(selections.index(item))

        def walk(_item):
            self.tag_add('copy', _item)
            for _item in self.get_children(_item):
                walk(_item)

        for item in selections:
            walk(item)

        self.detach(*selections)
        self.detached = selections
        self.tags_reset(excluded='copy')

    def copy(self, _=None):
        self.selected = self.selection()

    def paste(self, _=None):
        selections = self.detached if self.detached else self.selected

        if not self.selected and not self.detached:
            selections = self.tag_has('copy')

        if not len(selections):
            return

        now = datetime.now()
        parent = self.focus()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if self.detached:
            for item in selections:
                self.reattach(item, parent, tk.END)
            self.detached = False
        else:
            cr = {}  # Cross reference.
            for item in selections:
                ancestor = self.parent(item)
                dst = cr[ancestor] if ancestor in cr else parent
                self.value_update(1, dt_string, item)
                iid = self.insert(dst, **self.item(item))
                self.value_update(0, iid, iid)

                self.tag_remove('copy', iid)
                cr[item] = iid

        self.tags_reset(excluded='copy')
        self.selection_remove(self.tag_has('copy'))
        self.selection_set(self.focus())
        self.reindex()

    def delete(self):
        super(Treeview, self).delete(*self.selection())
        self.tags_reset(excluded='copy')

    def insert(self, parent, index=tk.END, **kwargs):
        kwargs.pop('children', None)
        return super(Treeview, self).insert(parent, index, **kwargs)

    def control_a(self, _):
        def select(_child):
            self.selection_add(_child)
            for node in self.get_children(_child):
                select(node)
        for child in self.get_children():
            select(child)

    def key_press(self, event):
        if 'Shift' in event.keysym:
            self.anchor = self.focus()

    def shift_up(self, event):
        prev = self.prev(self.focus())
        parent = self.parent(self.focus())
        if prev and parent:
            self.focus(prev)
            self.selection_toggle(prev)
        elif not parent:
            print(f'I0{hex(int(self.focus().lstrip("I"), 16)-1).split("x")[1]}', self.focus())
            prev = f'I0{hex(int(self.focus().lstrip("I"), 16)-1).split("x")[1]}'
            self.focus(prev)
            self.selection_add(prev)

        else:
            self.focus(parent)
            self.selection_toggle(parent)

        return 'break'

    def populate(self, parent, data=()):
        for item in data:
            iid = self.insert(parent, tk.END, **item)
            self.value_update(0, iid, iid)

            if 'children' in item:
                self.populate(iid, item['children'])

            self.value_update(0, iid, iid)

    def serialize(self):
        def get_data(_item, _data):
            for node in self.get_children(_item):
                _item_data = self.item(node)
                _data.append(_item_data)
                if self.get_children(node):
                    _item_data['children'] = []
                    get_data(node, _item_data['children'])

        data = {'headings': [], 'columns': [], 'data': {}}
        for idx in range(0, len(self['columns'])+1):
            data['headings'].append(self.heading(f'#{idx}'))
            data['columns'].append(self.column(f'#{idx}'))

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

    def reindex(self):
        def walk(_item):
            self.value_update(0, _item, _item)
            for node in self.get_children(_item):
                walk(node)

        for item in self.get_children():
            walk(item)

    def popup_menu(self, event):
        self.popup.x, self.popup.y = event.x_root, event.y_root
        item = self.identify('item', event.x, event.y)
        self.focus(item)
        self.focus_set()
        self.popup.tk_popup(event.x_root, event.y_root, 0)

    def bindings_set(self):
        bindings = {
            # '<Key>': self.key_press,
            '<Escape>': self.tags_reset,
            '<Shift-Up>': self.shift_up,
            '<Control-a>': self.control_a,
            '<Control-x>': self.cut,
            '<Control-c>': self.copy,
            '<Control-v>': self.paste,
            '<ButtonPress-3>': self.popup_menu,
            '<<TreeviewOpen>>': self.set_row_colors,
            '<<TreeviewClose>>': self.set_row_colors,
        }
        for command, callback in bindings.items():
            self.bind(command, callback)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
