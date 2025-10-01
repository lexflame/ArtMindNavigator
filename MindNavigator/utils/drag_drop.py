def make_draggable(widget, refresh_callback):
    drag_data = {"widget": None, "y": 0}

    def on_start(event):
        drag_data["widget"] = event.widget
        drag_data["y"] = event.y_root

    def on_motion(event):
        widget = drag_data["widget"]
        dy = event.y_root - drag_data["y"]
        widget.place(y=widget.winfo_y() + dy)
        drag_data["y"] = event.y_root

    def on_release(event):
        widget = drag_data["widget"]
        widget.place_forget()
        refresh_callback()
        drag_data["widget"] = None

    widget.bind("<Button-1>", on_start)
    widget.bind("<B1-Motion>", on_motion)
    widget.bind("<ButtonRelease-1>", on_release)
