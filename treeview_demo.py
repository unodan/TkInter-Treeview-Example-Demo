import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from os import path, makedirs


ABS_PATH = path.dirname(path.realpath(__file__))


def dump(data, indent=None):
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


def filter_dict_only(data):
    _data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            _data[k] = v
    return _data


class Dialog(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.title('Rename')
        self.container = ttk.Frame(self)
        self.container.rowconfigure(1, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.grid(sticky=tk.NSEW)

        frame = self.row0 = ttk.Frame(self.container)
        frame.columnconfigure(1, weight=1)
        self.label = ttk.Label(frame, text="Name")
        self.label.grid(sticky=tk.NSEW, row=0, column=0)
        self.entry = ttk.Entry(frame, width=30)
        self.entry.config(textvariable=self.var)
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


class Treeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.root = parent.winfo_toplevel()
        self.selected_items = []
        self.origin_x = \
            self.origin_y = \
            self.popup_x = \
            self.popup_y = \
            self.active_item = \
            self.origin_item = None

        sw = self.select_window = tk.Toplevel(self.root)
        sw.wait_visibility(self.root)
        sw.withdraw()
        sw.config(bg='#00aaff')
        sw.overrideredirect(True)
        sw.wm_attributes('-alpha', 0.3)
        sw.wm_attributes("-topmost", True)

        self.font = tkfont.nametofont('TkTextFont')
        self.style = parent.style
        self.config(selectmode="none")
        self.linespace = self.font.metrics('linespace') + 5

        popup = self.popup = tk.Menu(self.root, tearoff=0)
        popup.add_command(label="Cut", command=self.cut)
        popup.add_command(label="Copy", command=self.copy)
        popup.add_command(label="Paste", command=self.paste)
        popup.add_separator()
        popup.add_command(label="Delete", command=self.remove)
        popup.add_separator()
        popup.add_command(label="Rename", command=self.rename)

        self.bindings_set()

        parent.style.map("Treeview", foreground=self.fixed_map("foreground"), background=self.fixed_map("background"))

    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    def tag_add(self, tags, item):
        self.tags_update('add', tags, item)

    def tag_remove(self, tags, item=None):
        self.tags_update('remove', tags, item)

    def tag_replace(self, old, new, item=None):
        for item in (item,) if item else self.tag_has(old):
            if self.tag_has(old, item):
                self.tags_update('add', new, item)
                self.tags_update('remove', old, item)

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

    def button_press(self, event):
        self.origin_x, self.origin_y = event.x, event.y
        item = self.origin_item = self.active_item = self.identify('item', event.x, event.y)

        sw = self.select_window
        sw.geometry('0x0+0+0')
        sw.deiconify()

        self.bind('<Motion>', self.selected_set)

        if not item:
            if not event.state & 1 << 2:
                self.tags_reset()
            return

        if not event.state & 1 << 2:
            self.tags_reset()
            self.tag_add('selected', item)
            if self.tag_has('odd', item):
                self.tag_replace('odd', 'selected_odd', item)
            elif self.tag_has('even', item):
                self.tag_replace('even', 'selected_even', item)

    def button_release(self, _):
        self.select_window.withdraw()
        self.unbind('<Motion>')
        for item in self.selected_items:
            if self.tag_has('odd', item) or self.tag_has('even', item):
                self.tag_remove(('selected', '_selected'), item)
            else:
                self.tag_replace('_selected', 'selected', item)

    def selected_get(self, tag='selected'):
        return sorted(self.tag_has(f'{tag}_odd') + self.tag_has(f'{tag}_even'))

    def selected_set(self, event):
        def selected_items():
            items = []
            window_y = int(self.root.geometry().rsplit('+', 1)[-1])
            titlebar_height = self.root.winfo_rooty() - window_y
            sw = self.select_window
            start = sw.winfo_rooty() - titlebar_height - window_y
            end = start + sw.winfo_height()

            while start < end:
                start += 1
                node = self.identify('item', event.x, start)
                if not node or node in items:
                    continue
                items.append(node)

            return sorted(items)

        def set_row_colors():
            items = self.selected_items = selected_items()

            for item in items:
                if self.tag_has('selected', item):
                    if item == self.origin_item:
                        continue

                    if self.tag_has('selected_odd', item):
                        self.tag_replace('selected_odd', 'odd', item)
                    elif self.tag_has('selected_even', item):
                        self.tag_replace('selected_even', 'even', item)

                elif self.tag_has('odd', item):
                    self.tag_replace('odd', 'selected_odd', item)
                elif self.tag_has('even', item):
                    self.tag_replace('even', 'selected_even', item)

                self.tag_add('_selected', item)

            for item in self.tag_has('_selected'):
                if item not in items:
                    self.tag_remove('_selected', item)
                    if self.tag_has('odd', item):
                        self.tag_replace('odd', 'selected_odd', item)
                    elif self.tag_has('even', item):
                        self.tag_replace('even', 'selected_even', item)
                    elif self.tag_has('selected_odd', item):
                        self.tag_replace('selected_odd', 'odd', item)
                    elif self.tag_has('selected_even', item):
                        self.tag_replace('selected_even', 'even', item)

        root_x = self.root.winfo_rootx()
        if event.x < self.origin_x:
            width = self.origin_x - event.x
            coord_x = root_x + event.x
        else:
            width = event.x - self.origin_x
            coord_x = root_x + self.origin_x

        if coord_x+width > root_x+self.winfo_width():
            width -= (coord_x+width)-(root_x+self.winfo_width())
        elif self.winfo_pointerx() < root_x:
            width -= (root_x - self.winfo_pointerx())
            coord_x = root_x

        root_y = self.winfo_rooty()
        if event.y < self.origin_y:
            height = self.origin_y - event.y
            coord_y = root_y + event.y
        else:
            height = event.y - self.origin_y
            coord_y = root_y + self.origin_y

        if coord_y+height > root_y+self.winfo_height():
            height -= (coord_y+height)-(root_y+self.winfo_height())
        elif self.winfo_pointery() < root_y + self.linespace:
            height -= (root_y - self.winfo_pointery() + self.linespace)
            coord_y = root_y + self.linespace
            if height < 0:
                height = self.winfo_rooty() + self.origin_y

        set_row_colors()
        self.select_window.geometry(f'{width}x{height}+{coord_x}+{coord_y}')

    def bindings_set(self):
        bindings = {
            '<Escape>': self.tags_reset,
            '<ButtonPress-1>': self.button_press,
            '<ButtonRelease-1>': self.button_release,
            '<ButtonPress-3>': self.popup_menu,
            '<<TreeviewOpen>>': self.expand,
            '<<TreeviewClose>>': self.collapse,
        }
        for command, callback in bindings.items():
            self.bind(command, callback)

    def cut(self):
        for tag in ('copy', 'cut'):
            for item in self.tag_has(f'{tag}_odd'):
                self.tag_remove('selected', item)
                self.tag_replace(f'{tag}_odd', 'odd', item)
            for item in self.tag_has(f'{tag}_even'):
                self.tag_remove('selected', item)
                self.tag_replace(f'{tag}_even', 'even', item)

        self.tag_replace('selected_odd', 'cut_odd')
        self.tag_replace('selected_even', 'cut_even')

    def copy(self):
        for tag in ('copy', 'cut'):
            for item in self.tag_has(f'{tag}_odd'):
                self.tag_remove('selected', item)
                self.tag_replace(f'{tag}_odd', 'odd', item)
            for item in self.tag_has(f'{tag}_even'):
                self.tag_remove('selected', item)
                self.tag_replace(f'{tag}_even', 'even', item)

        self.tag_replace('selected_odd', 'copy_odd')
        self.tag_replace('selected_even', 'copy_even')

    def rename(self):
        def ok():
            text = dlg.entry.get().strip(' ')
            if text:
                self.item(item, text=text)
            dlg.destroy()

        def cancel():
            dlg.destroy()

        root = self.winfo_toplevel()
        for item in self.selected_get():
            dlg = Dialog(root)
            dlg.button_ok.config(command=ok)
            dlg.button_cancel.config(command=cancel)
            dlg.var.set(self.item(item, 'text'))
            dlg.entry.focus_set()
            dlg.entry.selection_range(0, tk.END)
            dlg.update_idletasks()
            if hasattr(self.popup, 'x') and hasattr(self.popup, 'y'):
                dlg.geometry(f'{dlg.geometry().split("+", 1)[0]}+{self.popup.x}+{self.popup.y}')
            root.wait_window(self)

    def paste(self):
        selected = list(self.tag_has('selected'))
        for item in selected.copy():
            tags = self.item(item, 'tags')
            for tag in tags:
                if 'selected_odd' in tag or 'selected_even' in tag:
                    selected.pop(selected.index(item))
        if not selected:
            return

        items = selected.copy()
        root = items[0]
        for item in items[1:]:
            if item.startswith(root):
                items.pop(items.index(item))
            else:
                root = item

        data = {}
        for item in items:
            data.update(self.get(item))

        for item in self.tag_has('copy_odd'):
            self.tag_replace('copy_odd', 'odd', item)
        for item in self.tag_has('copy_even'):
            self.tag_replace('copy_even', 'even', item)

        def walk(_parent, _data):
            iid = self.append(_parent, **_data)
            if not iid:
                return

            self.tag_remove(('cut_odd', 'cut_even'), iid)

            self.tag_remove('selected', iid)
            values = list(self.item(iid, 'values'))
            values[0] = iid
            self.item(iid, values=values)

            for value in _data.values():
                if not isinstance(value, dict):
                    continue
                walk(iid, value)

        for item, _data in data.items():
            if self.active_item.startswith(item):
                continue

            if self.active_item.startswith(item):
                if self.tag_has('selected_odd'):
                    self.tag_replace('selected_odd', 'odd')
                elif self.tag_has('selected_even'):
                    self.tag_replace('selected_even', 'even')

            walk(self.active_item, _data)

        if self.selected_get('cut'):
            self.remove('cut')
            self.selected_items = {}

        self.tags_reset('selected')

    def remove(self, tag='selected'):
        parent = ''

        items = self.selected_get(tag)
        if items:
            root = items[0]
            for item in items.copy():
                if item != root and item.startswith(root):
                    items.pop(items.index(item))
                else:
                    root = item

        for item in sorted(items, reverse=True):
            _parent = self.parent(item)
            if self.active_item.startswith(item):
                continue
            self.delete(item)
            if parent != _parent:
                parent = _parent
                self.reindex(parent)

        self.selected_items = {}
        self.tags_reset()
        self.reindex('')

    def insert(self, parent='', index=tk.END, **kwargs):
        def get_iid(_parent=''):
            nodes = self.get_children(_parent)

            idx = len(nodes)
            _iid = f'{_parent}_{idx}'

            while self.exists(_iid):
                idx += 1
                _iid = f'{_parent}_{idx}'
            return _iid

        kwargs.pop('iid', None)
        kwargs.pop('image', None)
        unique = kwargs.pop('unique', True)

        try:
            if unique:
                for child in self.get_children(parent):
                    if not kwargs['text'] or kwargs['text'] == self.item(child, 'text'):
                        raise NameError()

            iid = get_iid(parent)
            item = super(Treeview, self).insert(parent, index, iid=f'{iid}', **kwargs)
            return item

        except NameError:
            return False

    def append(self, parent, **kwargs):
        for key, value in kwargs.copy().items():
            if isinstance(value, dict):
                kwargs.pop(key)

        return self.insert(parent, **kwargs)

    def expand(self, _):
        def set_row_colors():
            self.tags_reset()
        self.after(1, set_row_colors)

    def collapse(self, _):
        def set_row_colors():
            self.tags_reset()
        self.after(1, set_row_colors)

    def populate(self, data, parent=''):
        def add_items(_parent, _item, _data):
            _parent = self.insert(_parent, **{
                'text': _data.get('text', ''),
                'image': _data.get('image', None),
                'values': _data.get('values', []),
                'open': _data.get('open', 0),
            })

            for k, v in _data.items():
                if isinstance(v, dict):
                    add_items(_parent, k, v)

        for item, value in data.items():
            if isinstance(value, dict):
                add_items(parent, item, value)

        self.tags_reset()

    def serialize(self):
        def get_data(_item, _data):
            for node in self.get_children(_item):
                _data[_item][node] = self.item(node)
                if self.get_children(node):
                    get_data(node, _data[_item])
        data = {}
        for item in self.get_children():
            data[item] = self.item(item)
            get_data(item, data)

        return data

    def get(self, iid=''):
        def get_data(_item, _data):
            _data[_item] = self.item(_item)
            for node in self.get_children(_item):
                get_data(node, _data[_item])

        data = {}
        get_data(iid, data)
        return data

    def reindex(self, parent):
        data = self.get(parent)
        data = filter_dict_only(data[parent])

        for item in self.get_children(parent):
            self.delete(item)

        def walk(_parent, _data):
            iid = self.append(_parent, **_data)
            values = list(_data['values'])
            values[0] = iid
            self.item(iid, values=values)

            for _k, _value in _data.items():
                if not isinstance(_value, dict):
                    continue
                walk(iid, _value)

        for k, value in data.items():
            if not isinstance(value, dict):
                continue
            walk(parent, value)

    def popup_menu(self, event):
        self.popup.x, self.popup.y = event.x_root, event.y_root
        item = self.active_item = self.identify('item', event.x, event.y)
        self.focus(item)
        self.focus_set()
        if self.selected_get():
            for _item in self.selected_get():
                if self.selected_get('copy') or self.selected_get('cut'):
                    if self.tag_has('selected_odd', _item):
                        self.tag_replace('selected_odd', 'odd', _item)
                    elif self.tag_has('selected_even', _item):
                        self.tag_replace('selected_even', 'even', _item)

        if self.tag_has('odd', item):
            self.tag_add('selected', item)
            self.tag_replace('odd', 'selected_odd', item)
        elif self.tag_has('even', item):
            self.tag_add('selected', item)
            self.tag_replace('even', 'selected_even', item)

        self.popup.tk_popup(event.x_root, event.y_root, 0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style()
        self.style.theme_use('clam')

        tv = self.treeview = Treeview(self)
        tv.heading('#0', text='Name')
        tv["columns"] = ("iid",)
        tv.column("iid", width=150, minwidth=150, stretch=tk.YES)
        tv.heading('#1', text='IID')

        tv.tag_configure('odd', background='#ffffff')
        tv.tag_configure('even', background='#aaaaaa')

        tv.tag_configure('cut_odd', background='#ffd4be')
        tv.tag_configure('cut_even', background='#ff5608')

        tv.tag_configure('copy_odd', background='#ceffff')
        tv.tag_configure('copy_even', background='#1ca0d8')

        tv.tag_configure('selected_odd', background='#b0eab2')
        tv.tag_configure('selected_even', background='#25a625')

        self.style.configure('TEntry', padding=(3, 2))

        self.title('Treeview Demo')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        tv.grid(sticky='NSEW', columnspan=990)

        self.app_data = {}
        self.init()

    def init(self):
        tv = self.treeview
        self.protocol('WM_DELETE_WINDOW', self.exit)

        file = path.join(ABS_PATH, 'app.json')
        if path.exists(file):
            with open(file) as f:
                self.app_data = json.load(f)
        else:
            self.app_data = {
                'geometry': self.geometry(),
            }

        self.geometry(self.app_data.get('geometry', ''))

        file = path.join(ABS_PATH, 'treeview.json')
        if path.exists(file):
            with open(file) as f:
                tv.populate(json.load(f))
        else:
            tag = 'odd'
            for idx in range(0, 4):
                # Populating the tree with test data.
                tag = 'even' if tag == 'odd' else 'odd'
                parent = tv.insert('', text=f'Menu {idx}', values=[f'_{idx}'], open=1, tags=(tag,))
                for _idx in range(0, 2):
                    tv.insert(parent, text=f'Item {_idx}', values=[f'{parent}_{_idx}'], tags=(tag,))
                _parent = tv.insert(parent, text='Sub menu', values=[f'{parent}_2'], open=1, tags=(tag,))

                for _idx in range(0, 2):
                    tv.insert(_parent, text=f'Sub item {_idx}', values=[f'{_parent}_{_idx}'], tags=(tag,))
                tv.insert(_parent, text='Sub sub menu', values=[f'{parent}_2_2'], open=1, tags=(tag,))
                for _idx in range(3, 5):
                    tv.insert(_parent, text=f'Sub item {_idx}', values=[f'{_parent}_{_idx}'], tags=(tag,))

                for _idx in range(3, 5):
                    tv.insert(parent, text=f'Item {_idx}', values=[f'{parent}_{_idx}'], tags=(tag,))

                tv.tags_reset()

    def exit(self):
        self.app_data.update({'geometry': self.geometry()})
        self.save()
        self.destroy()

    def save(self):
        file = path.join(ABS_PATH, 'treeview.json')
        if file:
            dirname = path.dirname(file)
            if not path.exists(dirname):
                makedirs(dirname)

            with open(file, 'w') as f:
                json.dump(self.treeview.serialize(), f, indent=3)

        file = path.join(ABS_PATH, 'app.json')
        if file:
            dirname = path.dirname(file)
            if not path.exists(dirname):
                makedirs(dirname)

            with open(file, 'w') as f:
                json.dump(self.app_data, f, indent=3)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
