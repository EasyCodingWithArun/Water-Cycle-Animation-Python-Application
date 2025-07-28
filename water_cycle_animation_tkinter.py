import tkinter as tk
import random

# Main window setup
root = tk.Tk()
root.title("Water Cycle Animation")
root.geometry("600x500")
root.resizable(False, False)

# Canvas setup
canvas = tk.Canvas(root, width=600, height=500, bg="skyblue")
canvas.pack()

# --- Sun ---
sun_radius = 50
canvas.create_oval(600 - sun_radius*2 - 10, 10,
                   600 - 10, 10 + sun_radius*2,
                   fill="#FFD700", outline="")
canvas.create_text(600 - sun_radius - 10, 10 + sun_radius*2 + 10,
                   text="Sun", fill="orange", font=("Arial", 10, "bold"))

# --- Ground & Water ---
canvas.create_rectangle(0, 400, 600, 500, fill="forest green", outline="")
canvas.create_oval(150, 370, 450, 420, fill="blue", outline="")

# --- Weather Clouds (realistic overlapping shapes) ---
cloud_parts = []
# Main cloud cluster
cloud_parts = [
canvas.create_oval(250, 60, 310, 100, fill="white", outline=""),
canvas.create_oval(280, 50, 360, 110, fill="white", outline=""),

canvas.create_oval(320, 60, 390, 100, fill="white", outline=""),
]
# Additional ambient clouds
cloud_parts.append(canvas.create_oval(80, 90, 160, 140, fill="white", outline=""))
cloud_parts.append(canvas.create_oval(420, 80, 510, 135, fill="white", outline=""))

# --- Labels ---
evaporation_label = canvas.create_text(500, 200, text="Evaporation", fill="orange", 
                                       font=("Arial", 10, "bold"), state=tk.HIDDEN)
condensation_label = canvas.create_text(320, 40, text="Condensation (Cloud Filling)", fill="black", 
                                        font=("Arial", 10, "bold"), state=tk.HIDDEN)
precipitation_label = canvas.create_text(500, 250, text="Precipitation (Rain)", fill="blue", 
                                         font=("Arial", 10, "bold"), state=tk.HIDDEN)
collection_label = canvas.create_text(300, 460, text="Collection in Water Body", fill="white", 
                                      font=("Arial", 11, "bold"))

# --- Vapor Lines (static arrows) ---
vapor_lines = []
for i in range(8):  # 8 static arrows
    x = 260 + i*15
    vapor_lines.append(canvas.create_line(x, 345, x, 315, fill="white", arrow=tk.LAST, width=2))

# --- Vapor Drops (moving) ---
vapors = []
for i in range(8):
    x = 260 + i*15
    vapors.append(canvas.create_oval(x-3, 345, x+3, 350, fill="white", outline="", state=tk.HIDDEN))
vapor_text = canvas.create_text(320, 300, text="Water Vapor Rising", fill="white", 
                                font=("Arial", 9, "bold"), state=tk.HIDDEN)

# --- Rain Drops ---
rain_drops = []
for i in range(7):
    x = 250 + i*20
    rain_drops.append(canvas.create_oval(x, 140, x+5, 150, fill="blue", outline="", state=tk.HIDDEN))

# --- Animation Control ---
cycle_step = 0  # 0=evaporation,1=condensation,2=rain,3=reset
frame_counter = 0

# Durations
EVAP_FRAMES = 100
COND_FRAMES = 50
RAIN_FRAMES = 100

# Cloud darkening
cloud_colors = ["white", "#f0f0f0", "#e0e0e0", "#d0d0d0", "#c0c0c0",
                 "#b0b0b0", "#a0a0a0", "#909090"]
cloud_idx = 0

# --- Animation Function ---
def animate():
    global cycle_step, frame_counter, cloud_idx
    # Hide dynamic labels
    canvas.itemconfig(evaporation_label, state=tk.HIDDEN)
    canvas.itemconfig(condensation_label, state=tk.HIDDEN)
    canvas.itemconfig(precipitation_label, state=tk.HIDDEN)
    canvas.itemconfig(vapor_text, state=tk.HIDDEN)
    # Hide vapors and rain
    for drop in vapors:
        canvas.itemconfig(drop, state=tk.HIDDEN)
    for drop in rain_drops:
        canvas.itemconfig(drop, state=tk.HIDDEN)

    if cycle_step == 0:
        # Evaporation phase
        canvas.itemconfig(evaporation_label, state=tk.NORMAL)
        canvas.itemconfig(vapor_text, state=tk.NORMAL)
        for drop in vapors:
            canvas.itemconfig(drop, state=tk.NORMAL)
            canvas.move(drop, 0, -2)
            x1, y1, x2, y2 = canvas.coords(drop)
            if y2 <= 100:
                canvas.coords(drop, x1, 345, x2, 350)
        frame_counter += 1
        if frame_counter >= EVAP_FRAMES:
            cycle_step = 1
            frame_counter = 0
            cloud_idx = 0

    elif cycle_step == 1:
        # Condensation phase
        canvas.itemconfig(condensation_label, state=tk.NORMAL)
        # Darken cloud gradually
        if frame_counter % (COND_FRAMES // len(cloud_colors)) == 0 and cloud_idx < len(cloud_colors):
            for part in cloud_parts:
                canvas.itemconfig(part, fill=cloud_colors[cloud_idx])
            cloud_idx += 1
        frame_counter += 1
        if frame_counter >= COND_FRAMES:
            cycle_step = 2
            frame_counter = 0

    elif cycle_step == 2:
        # Rain phase
        canvas.itemconfig(precipitation_label, state=tk.NORMAL)
        for drop in rain_drops:
            canvas.itemconfig(drop, state=tk.NORMAL)
            canvas.move(drop, 0, 6)
            x1, y1, x2, y2 = canvas.coords(drop)
            if y2 > 370:
                canvas.coords(drop, x1, 140, x2, 150)
        frame_counter += 1
        if frame_counter >= RAIN_FRAMES:
            cycle_step = 3
            frame_counter = 0

    else:
        # Reset cycle
        for part in cloud_parts:
            canvas.itemconfig(part, fill="white")
        for drop in vapors:
            canvas.coords(drop, canvas.coords(drop)[0]-0, 345, canvas.coords(drop)[2]+0, 350)
        for drop in rain_drops:
            orig_x = 250 + rain_drops.index(drop)*20
            canvas.coords(drop, orig_x, 140, orig_x+5, 150)
        cycle_step = 0
        frame_counter = 0

    canvas.after(50, animate)

# Start animation
animate()
root.mainloop()