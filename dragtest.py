import tkinter as tk

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag and Drop Vector")

        self.vector = [["" for _ in range(8)] for _ in range(8)]  # Initialize the 8x8 double vector

        self.labels = [[None for _ in range(8)] for _ in range(8)]  # Store label widgets
        
        self._create_labels()
        
    def _create_labels(self):
        for row in range(8):
            for col in range(8):
                label = tk.Label(self.root, text=self.vector[row][col], relief=tk.RAISED)
                label.grid(row=row, column=col, padx=5, pady=5)
                label.bind("<Button-1>", lambda event, r=row, c=col: self._start_drag(event, r, c))
                self.labels[row][col] = label
    
    def _start_drag(self, event, row, col):
        self.dragged_item = (row, col)
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        # Bind motion and release events
        self.root.bind("<Motion>", self._drag_motion)
        self.root.bind("<ButtonRelease-1>", self._end_drag)
        
    def _drag_motion(self, event):
        delta_x = event.x - self.drag_start_x
        delta_y = event.y - self.drag_start_y
        
        row, col = self.dragged_item
        label = self.labels[row][col]
        label.place(x=label.winfo_x() + delta_x, y=label.winfo_y() + delta_y)
        
    def _end_drag(self, event):
        row, col = self.dragged_item
        label = self.labels[row][col]
        
        # Calculate new position
        new_row = event.y // label.winfo_height()
        new_col = event.x // label.winfo_width()
        
        # Update vector and labels
        self.vector[row][col], self.vector[new_row][new_col] = self.vector[new_row][new_col], self.vector[row][col]
        label.config(text=self.vector[row][col])
        self.labels[new_row][new_col].config(text=self.vector[new_row][new_col])
        
        label.place(x=new_col * label.winfo_width(), y=new_row * label.winfo_height())
        
        # Unbind events
        self.root.unbind("<Motion>")
        self.root.unbind("<ButtonRelease-1>")
        
        self.dragged_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DragDropApp(root)
    root.mainloop()
