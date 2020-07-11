import toga
from ..libs import Gtk
from .base import Widget
from .internal.sourcetreemodel import SourceTreeModel


class Tree(Widget):
    def create(self):
        # Tree is reused for table, where it's a ListSource, not a tree
        # so check here if the actual widget is a Tree or a Table.
        # It can't be based on the source, since it determines flags
        # and GtkTreeModel.flags is not allowed to change after creation
        is_tree = isinstance(self.interface, toga.Tree)
        self.store = SourceTreeModel([{'type': str, 'attr': a} for a in self.interface._accessors], is_tree=is_tree)

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(model=self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i + 1)
            column.set_cell_data_func(renderer, self.strip_icon, self.interface._accessors[i])
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

    @staticmethod
    def strip_icon(tree_colum, cell, tree_model, iter_, attr):
        # FIXME: I can do icons
        item = tree_model.do_get_value(iter_, 0)
        val = getattr(item, attr)
        if isinstance(val, tuple):
            return str(val[1])
        return str(val)

    def gtk_on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            self.interface._selection = node
            self.interface.on_select(self.interface, node=node)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.change_source(source)

        def append_children(data, parent=None):
            if data.can_have_children():
                for i, node in enumerate(data):
                    self.insert(parent, i, node)
                    append_children(node, parent=node)

        # XXX: I don't understand why it was self.interface.data instead of source
        append_children(source, parent=None)

        self.treeview.set_model(self.store)

    def insert(self, parent, index, item, **kwargs):
        self.store.insert(item)

    def change(self, item):
        self.store.change(item)

    def remove(self, item, index, parent):
        self.store.remove(item, index=index, parent=parent)

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        # No special handling required
        pass

    def scroll_to_node(self, node):
        path = self.store.path_to_node(node)
        self.treeview.scroll_to_cell(path)
