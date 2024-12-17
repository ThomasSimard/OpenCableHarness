from typing import List, Dict, Tuple, Callable

import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.TableHelpers import swap_row_values

class ListEditCtrl:
    """
    Creates a ListEditCtrl widget.

    :param table_id: The ID for the table.
    :param grid: The input data source for the control.
    """

    def __init__(self, table_id, grid: DataGrid, editable=True, save_change=None, width=-1, height=-1):
        self.table_id = table_id
        self.grid = grid
        self.editable = editable

        self.save_change = save_change

        self.width = width
        self.height = height

        self.focus_index = -1
        self.show()

    def show(self):
        unsaved_grid_data = None

        def enable_editor():
            nonlocal unsaved_grid_data
            unsaved_grid_data = self.evaluate_grid().data

            dpg.disable_item(edit_button)

            dpg.enable_item(editing_buttons)
            dpg.enable_item(self.edit_buttons)

            dpg.enable_item(self.table)

            #for row in dpg.get_item_children(self.table_id, slot=1):
            #    for item in dpg.get_item_children(row, slot=1):
            #        dpg.enable_item(item)

        def disable_editor():
            dpg.enable_item(edit_button)

            dpg.disable_item(editing_buttons)
            dpg.disable_item(self.edit_buttons)

            dpg.disable_item(self.table)
            #for row in dpg.get_item_children(self.table_id, slot=1):
            #    for item in dpg.get_item_children(row, slot=1):
            #        dpg.disable_item(item)

        def cancel():
            nonlocal unsaved_grid_data

            self.set_grid_data(unsaved_grid_data)

            disable_editor()

        def save_change():
            self.save_change()

            disable_editor()

        with dpg.child_window(menubar=True, frame_style=False, width=self.width, height=self.height):
            with dpg.menu_bar():
                dpg.add_text(self.grid.title)

            # Edit, Cancel and Save buttons
            with dpg.group(horizontal=True, show=self.editable):
                with dpg.group() as edit_button:
                    dpg.add_button(label="Edit", callback=enable_editor)

                with dpg.group(horizontal=True, enabled=False) as editing_buttons:
                    dpg.add_button(label="Cancel", callback=cancel)
                    dpg.add_button(label="Save", callback=save_change)

            dpg.add_separator()

            with dpg.group(horizontal=True, show=self.editable, enabled=False) as self.edit_buttons:
                dpg.add_button(label="Add", tag=dpg.generate_uuid(), callback=lambda: self._add_row(use_defaults=True))
                dpg.add_button(label="Remove", tag=dpg.generate_uuid(), callback=self._delete_row)
                dpg.add_button(arrow=True, direction=dpg.mvDir_Up, callback=self._move_row_up)
                dpg.add_button(arrow=True, direction=dpg.mvDir_Down, callback=self._move_row_down)

            with dpg.group(enabled=False) as self.table:
                with dpg.table(tag=self.table_id, header_row=True,
                    policy=dpg.mvTable_SizingStretchProp):

                    dpg.add_table_column() # index column

                    for col in self.grid.columns:
                        dpg.add_table_column(parent=self.table_id,label=col)

                    self.set_grid_data(self.grid.data)

    def set_editable(self, editable):
        if editable:
            dpg.show_item(self.edit_buttons)
        else:
            dpg.hide_item(self.edit_buttons)

    def _subgrid_callback(self, col_idx, row_idx, new_grid: DataGrid):
        """
        Callback method for child grids to update their data in the parent grid.
        """
        self.grid.data[col_idx][row_idx] = new_grid

    def _add_row(self, use_defaults=True):
        """
        Adds a new row to the DataGrid.

        :param use_defaults: A boolean indicating whether to use default values for the new row.
            If False, it uses the data from the corresponding row in the underlying DataGrid.

        This function creates a new row in the DataGrid and populates it with widgets appropriate for each column's
        data type. The widgets are initialized with either default values (if use_defaults=True) or with the
        corresponding data from the underlying DataGrid (if use_defaults=False).

        It uses the _set_focus callback to update the selected row index when any widget in the new row is clicked.

        If a new row is added that exceeds the current number of rows in the underlying DataGrid,
        the DataGrid is expanded with a row of default values.

        TODO:
        1. Insertion of rows in the middle of the grid is currently not supported. Implement functionality to support
        insertion into arbitrary positions in the grid.
        2. The row index is not currently passed to the callback functions for the individual widgets. Modify the
        callbacks to accept the row index as an input. This will enable the callbacks to modify specific rows
        in the DataGrid based on user interaction.

        :raises ValueError: If a column has an unsupported data type.
        """

        row_idx = len(dpg.get_item_children(self.table_id)[1])

        # if the row_idx is greater than the grid length, then expand the grid
        if row_idx >= self.grid.shape[0]:
            self.grid.append(self.grid.defaults)

        # need to feed in the row index for the callbacks
        with dpg.table_row(parent = self.table_id) as row_id:

            dpg.add_table_cell()

            for col_idx in range(len(self.grid.columns)):
                row = self.grid.defaults if use_defaults else self.grid.get_row(row_idx) # TODO grid.defaults if row_idx==None or row_idx >= grid.shape[0]

                if self.grid.dtypes[col_idx] == DataGrid.CHECKBOX:
                    dpg.add_checkbox(callback=self._set_focus,
                                    default_value=row[col_idx],
                                    user_data=row_id)
                elif self.grid.dtypes[col_idx] == DataGrid.TXT_STRING:
                    id_input_text = dpg.generate_uuid()
                    dpg.add_input_text(tag=id_input_text,
                                    default_value=row[col_idx],
                                    hint="Enter text here", width=200, callback=self._set_focus, user_data=row_id)
                    self._register_widget_click(id_input_text, row_id)
                elif self.grid.dtypes[col_idx] == DataGrid.TXT_INT:
                    id_input_int_text = dpg.generate_uuid()
                    dpg.add_input_int(tag=id_input_int_text,
                                    default_value=row[col_idx], min_value=1, min_clamped=True,
                                    width=125, callback=self._set_focus, user_data=row_id)
                    self._register_widget_click(id_input_int_text, row_id)
                elif self.grid.dtypes[col_idx] == DataGrid.COMBO:
                    id_input_combo = dpg.generate_uuid()
                    dpg.add_combo(tag=id_input_combo,
                                items=self.grid.combo_lists[col_idx],
                                default_value=self.grid.combo_lists[col_idx][row[col_idx]],
                                no_preview=False, width=150, callback=self._set_focus, user_data=row_id)
                    self._register_widget_click(id_input_combo, row_id)
                elif self.grid.dtypes[col_idx] == DataGrid.COLOR:
                    id_color_pikr = dpg.generate_uuid()
                    dpg.add_color_edit(tag=id_color_pikr,
                                    default_value=row[col_idx],
                                    no_inputs=True, callback=self._set_focus, user_data=row_id)
                    self._register_widget_click(id_color_pikr, row_id)
                elif self.grid.dtypes[col_idx] == DataGrid.COLOR_CODE:
                    # Color preview
                    id_color_button = dpg.generate_uuid()
                    dpg.add_color_button(tag=id_color_button,
                                    default_value=(0, 0, 0, 255),
                                    callback=self._set_focus, user_data=row_id)
                    self._register_widget_click(id_color_button, row_id)
                else:
                    raise ValueError("unsupported data type")

            # close out the row
            dpg.add_selectable(height=20, span_columns=True, callback=self._set_focus, user_data=row_id)

    def set_focus_index(self, index, need_unhighlight=True):
        if self.focus_index >= 0 and need_unhighlight:
            dpg.unhighlight_table_row(self.table_id, self.focus_index)

        self.focus_index = index

        if self.focus_index >= 0:
            dpg.highlight_table_row(self.table_id, self.focus_index, [15,86,135])

    def _delete_row(self):
        if self.focus_index < 0:
            return

        # delete the row from DPG
        row_id = dpg.get_item_children(self.table_id)[1][self.focus_index]
        dpg.delete_item(row_id)

        # delete the row from the grid
        self.grid.drop(self.focus_index)

        # move the focus_index up if list length is less than focus_index
        self.set_focus_index(-1, False)

    def _move_row_up(self):
        row_ids = dpg.get_item_children(self.table_id, 1)
        if (self.focus_index == 0) or (len(row_ids) <= 1):
            return False

        swap_row_values(self.table_id, self.focus_index, self.focus_index-1)
        self.grid.swap_rows(self.focus_index, self.focus_index-1)

        self.set_focus_index(self.focus_index - 1)

        return True

    def _move_row_down(self):
        row_ids = dpg.get_item_children(self.table_id, 1)
        if (self.focus_index == len(row_ids)-1) or (len(row_ids) <= 1):
            return False

        swap_row_values(self.table_id, self.focus_index, self.focus_index+1)
        self.grid.swap_rows(self.focus_index, self.focus_index+1)

        self.set_focus_index(self.focus_index + 1)

        return True

    def _set_focus(self, sender, app_data, user_data): # TODO fix this method sig or rename `_set_focus_from_widget`
        if (dpg.get_item_type(sender) == "mvAppItemType::mvSelectable"):
            dpg.set_value(sender, False)

        table_children = dpg.get_item_children(self.table_id, 1)

        self.set_focus_index(table_children.index(user_data))

    def _on_widget_click(self, row_id):
            # this is slow but good enough for prototyping
            table_children = dpg.get_item_children(self.table_id, 1)

            self.set_focus_index(table_children.index(row_id))

    def _register_widget_click(self, sender, row_id):
        handler_tag = f"{row_id} handler"
        if not dpg.does_item_exist(handler_tag):
            with dpg.item_handler_registry(tag=handler_tag):
                dpg.add_item_clicked_handler(callback=lambda x: self._on_widget_click(row_id))

        dpg.bind_item_handler_registry(sender, handler_tag)

    def evaluate_grid(self):
        # create a new grid of the same structure
        new_grid = self.grid.empty_like()

        # populate the grid from the table
        for row_idx, row_id in enumerate(dpg.get_item_children(self.table_id)[1]):
            new_row = []
            cells = list(dpg.get_item_children(row_id)[1])
            for col_idx, col_id in enumerate(cells[1:-1]):  # Skip the first and last cell.
                if self.grid.dtypes[col_idx] == DataGrid.COMBO:
                    selection = dpg.get_value(col_id)
                    idx = self.grid.combo_lists[col_idx].index(selection)
                    new_row.append(idx)
                else:
                    # Get the value in the cell and append it to the new row.
                    new_row.append(dpg.get_value(col_id))
            # Add the new row to the data in the new grid.
            new_grid.append(new_row)

        return new_grid

    def set_grid_data(self, data):
        self.grid.data = data

        for row in dpg.get_item_children(self.table_id, slot=1):
            dpg.delete_item(row)

        for i in range(len(self.grid.data[0])):
            self._add_row(use_defaults=False)
