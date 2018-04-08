import tkinter as tk

class ShoppingList():
  def __init__(self, items = None):
    if items != None:
      self.items = items
    else:
      self.items = []
      
  def add_item(self, item):
    """
    adds an item to the shopping list
    """
    self.items.append(item)

  def remove_item(self, item):
    """
    removes an item from the shopping list
    """
    if item in self.items:
      item.destroy()
      self.items.remove(item)
    
  def return_list(self):
    """
    returns the current shopping list
    """
    return (self.items)

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("myList v.1")
        self.geometry("300x390")

        self.state_variables = []
        self.canvas_height = 0

        self.button_area = tk.Frame(self)
        self.canvas_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.canvas_frame, height = 300, width = 300)
        self.task_frame = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window = self.task_frame, anchor = "nw", width = 300)
        self.text_area = tk.Frame(self)

        self.scroll = tk.Scrollbar(self.canvas_frame, orient = "vertical")
        self.scroll.configure(command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scroll.set)
        
        self.button_area.pack(side = tk.TOP, fill = tk.BOTH)
        self.canvas_frame.pack(side = tk.TOP, fill = tk.BOTH)
        self.scroll.pack(side = tk.RIGHT, fill = tk.Y)
        self.canvas.pack(side = tk.TOP, fill = tk.X)
        self.text_area.pack(side = tk.BOTTOM, fill = tk.X)

        self.select_button = tk.Button(self.button_area, text = "Select All", padx = 20, command = self.select_all)
        self.deselect_button = tk.Button(self.button_area, text = "Deselect All", padx = 20, command = self.deselect_all)
        self.delete_button = tk.Button(self.button_area, text = "Delete", padx = 20, command = self.item_remove)
        self.select_button.pack(side = tk.LEFT)
        self.deselect_button.pack(side = tk.LEFT)
        self.delete_button.pack(side = tk.RIGHT)

        self.text_box = tk.Text(self.text_area, height = 3, bg = "white", fg = "black")
        self.text_box.pack(side = tk.BOTTOM, fill = tk.X)
        self.text_box.focus_set()

        self.canvas.configure(scrollregion = (0, 0, 300, 0))

        self.myList = ShoppingList()

        self.directions = tk.Label(self.task_frame, text = "Type an item, press return. Easy as pie.", bg = "#000099", \
        fg = "white", pady = 10, padx = 5, wraplength = 200)
        self.directions.pack(side = tk.BOTTOM, fill = tk.X)
        self.first_launch = True

        self.bind("<Return>", self.new_item)

        self.color_scheme = ["#ff4d4d", "#ff9933", "#ffff66", "#33cc33", "#0099ff", "#6666ff", "#8000ff"]  

    def new_item(self, event = None):
        """
        takes a single string item. adds it to myList items and packs the label in the frame.
        """
        if len(self.text_box.get(1.0, tk.END).strip()) > 0:
          pos = len(self.myList.return_list())
          myColor = self.color_scheme[pos % 7]
          self.state_variables.append(pos)

          item_text = self.text_box.get(1.0, tk.END).strip()

          self.state_variables[pos] = tk.IntVar()
          item_to_add = tk.Checkbutton(self.task_frame, variable = self.state_variables[pos], text = "   " + item_text, \
          background = myColor, justify = tk.LEFT, pady = 10, font = ('Avant Garde', 20), wraplength = 300)

          print (item_to_add)
          self.myList.add_item(item_to_add)
          item_to_add.pack(side = tk.TOP, fill = tk.X)
          
          self.text_box.delete(1.0, tk.END)
          self.canvas_height += 47
          self.canvas.configure(scrollregion = (0, 0, 300, self.canvas_height))

          if self.first_launch:
            if len(self.myList.return_list()) == 1:
              self.directions["text"] = "Use the buttons above to automatically select, deselect, and delete list items."
            elif len(self.myList.return_list()) > 1:
              self.directions.destroy()
              self.first_launch = False

    def select_all(self, event = None):
      """
      sets the state variables of all checklist items to active (i.e. checked)
      also changes the button text
      """
      for item in self.state_variables:
        item.set(1)

    def deselect_all(self, event = None):
      """
      sets the state variables of all checklist items to deactive (i.e. unchecked)
      """
      for item in self.state_variables:
        item.set(0)

    def item_recolor(self):
      """
      when items are deleted from the list, ensures that the remaining items are properly
      recolored to maintain the color scheme.
      """
      i = 0
      for item in self.myList.return_list():
        item["background"] = self.color_scheme[i % 7]
        i += 1
    
    def item_remove(self, event = None):
      """
      event handler for the delete button. destroys the checklist widget, removes it from the
      shopping list class instance's list of items, and removes the variable containing the checklist state.
      calls the recolor method to maintain proper coloration of the list.
      """
      current_items = self.myList.return_list()[:]
      state_var_copy = self.state_variables[:]

      for pos in range(len(current_items)):
        if state_var_copy[pos].get() == 1:
          item_to_delete = current_items[pos]
          self.myList.remove_item(item_to_delete)
          self.state_variables.remove(state_var_copy[pos])

      if len(self.myList.return_list()) > 0:
        self.item_recolor()

    def window_resize(self):
      """
      """

if __name__ == "__main__":
    root = Root()
    root.mainloop()