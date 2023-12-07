# import tkinter as tk
# from tkinter import PhotoImage
# import Activate
# import Collect_Data
# import Train_Model

# # Color Palette
# color_palette = ["#33AEA9","#355C7D", "#725A7A", "#C56C86", "#FF7582"]


# # Create the main window
# window = tk.Tk()
# window.title("Beautiful Tkinter GUI")

# # Set background color
# window.configure(bg=color_palette[0])

# label_status = tk.Label(
#     window, text="", font=("Helvetica", 12), bg=color_palette[0], fg="white"
# )
# label_status.pack(pady=10)

# # Project Name Label
# label_project_name = tk.Label(
#     window,
#     text="My Project",
#     font=("Helvetica", 20, "bold"),
#     bg=color_palette[1],
#     fg="white",
# )
# label_project_name.pack(pady=10)

# # Collect Data Button
# collect_data_button = tk.Button(
#     window,
#     text="Collect Data",
#     font=("Helvetica", 12),
#     command=Collect_Data.Collect,
#     bg=color_palette[2],
#     fg="white",
#     bd=0,
#     padx=30,
#     pady=15,
#     relief=tk.RAISED,
#     image=PhotoImage(r"C:\\Users\susha\\OneDrive\\Desktop\\Eye Gaze\\logo\\Activate.png"),
#     cursor="hand2",
#     compound=tk.LEFT,
# )
# collect_data_button.pack(pady=10, padx=20)

# # Train Model Button
# train_model_button = tk.Button(
#     window,
#     text="Train Model",
#     font=("Helvetica", 12),
#     command=Train_Model.Train_Model,
#     bg=color_palette[3],
#     fg="white",
#     bd=0,
#     padx=30,
#     pady=15,
#     image=PhotoImage(r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\Activate.png"),
#     relief=tk.RAISED,
#     cursor="hand2",
#     compound=tk.LEFT,
# )
# train_model_button.pack(pady=10, padx=20)

# # Activate Button
# activate_button = tk.Button(
#     window,
#     text="Activate",
#     font=("Helvetica", 12),
#     command=Activate.activate,
#     bg=color_palette[3],
#     fg="white",
#     bd=0,
#     padx=30,
#     pady=15,
#     image=PhotoImage(r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\Activate.png"),
#     relief=tk.RAISED,
#     cursor="hand2",
#     compound=tk.LEFT,
# )
# activate_button.pack(pady=10, padx=20)

# # Quit Button
# quit_button = tk.Button(
#     window,
#     text="Quit",
#     font=("Helvetica", 12),
#     command=window.destroy,
#     bg=color_palette[4],
#     fg="white",
#     bd=0,
#     padx=30,
#     pady=15,
#     image=PhotoImage(r"C:\\Users\susha\\OneDrive\\Desktop\\Eye Gaze\\logo\\exit.png"),
#     relief=tk.RAISED,
#     cursor="hand2",
#     compound=tk.LEFT,
# )
# quit_button.pack(pady=10, padx=20)

# # Status Label


# # Run the Tkinter event loop
# window.mainloop()

# # Create buttons with icons
# # button_icons = [r'logo\DataCollection.png', r'logo\TrainModel.png', r'logo\Activate.png', r'logo\exit.png']
# # button_names = ['Collect_Data', 'Train_Model', 'Activate', 'Quit']
# # buttons = []
import tkinter as tk
from tkinter import PhotoImage
import Activate
import Collect_Data
import Train_Model

# Color Palette
color_palette = ["#33AEA9", "#355C7D", "#725A7A", "#C56C86", "#FF7582"]

# Create the main window
window = tk.Tk()
window.title("Beautiful Tkinter GUI")

# Set background color
window.configure(bg=color_palette[0],height=1000,width=350)

label_status = tk.Label(
    window, text="", font=("Helvetica", 12), bg=color_palette[0], fg="white"
)
label_status.pack(pady=10)

# Project Name Label
label_project_name = tk.Label(
    window,
    text="Eye Gaze Dectection",
    font=("Helvetica", 20, "bold"),
    bg=color_palette[1],
    fg="white",
)
label_project_name.pack(pady=10)

# Collect Data Button
collect_data_icon = PhotoImage(file=r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\DataCollection.png")
collect_data_icon = collect_data_icon.subsample(25)  # Adjust the subsample values as needed
collect_data_button = tk.Button(
    window,
    text="Collect Data",
    font=("Helvetica", 12),
    command=Collect_Data.Collect,
    bg=color_palette[2],
    fg="white",
    bd=0,
    padx=30,
    pady=15,
    relief=tk.RAISED,
    image=collect_data_icon,
    cursor="hand2",
    compound=tk.LEFT,
)
collect_data_button.pack(pady=10, padx=20)

# Train Model Button
train_model_icon = PhotoImage(file=r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\TrainModel.png")
train_model_icon = train_model_icon.subsample(20)
train_model_button = tk.Button(
    window,
    text="Train Model",
    font=("Helvetica", 12),
    command=Train_Model.Train_Model,
    bg=color_palette[3],
    fg="white",
    bd=0,
    padx=30,
    pady=15,
    image=train_model_icon,
    relief=tk.RAISED,
    cursor="hand2",
    compound=tk.LEFT,
)
train_model_button.pack(pady=10, padx=20)

# Activate Button
activate_icon = PhotoImage(file=r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\Activate.png")
activate_icon = activate_icon.subsample(20)
activate_button = tk.Button(
    window,
    text="Activate",
    font=("Helvetica", 12),
    command=Activate.activate,
    bg=color_palette[3],
    fg="white",
    bd=0,
    padx=30,
    pady=15,
    image=activate_icon,
    relief=tk.RAISED,
    cursor="hand2",
    compound=tk.LEFT,
)
activate_button.pack(pady=10, padx=20)

# Quit Button
quit_icon = PhotoImage(file=r"C:\Users\susha\OneDrive\Desktop\Eye Gaze\logo\exit.png")
quit_icon = quit_icon.subsample(20)
quit_button = tk.Button(
    window,
    text="Quit",
    font=("Helvetica", 12),
    command=window.destroy,
    bg=color_palette[4],
    fg="white",
    bd=0,
    padx=30,
    pady=15,
    image=quit_icon,
    relief=tk.RAISED,
    cursor="hand2",
    compound=tk.LEFT,
)
quit_button.pack(pady=10, padx=20)

# Run the Tkinter event loop
window.mainloop()
    