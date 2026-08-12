import tkinter as tk
from tkinter import ttk
import psutil
import platform

try:
    import wmi
    w = wmi.WMI()
except:
    w = None


# =====================================
# گرفتن اطلاعات ثابت
# =====================================

def get_cpu():
    if not w:
        return "Unknown"

    try:
        cpu = w.Win32_Processor()[0]

        return {
            "name": cpu.Name,
            "manufacturer": cpu.Manufacturer,
            "cores": cpu.NumberOfCores,
            "threads": cpu.NumberOfLogicalProcessors,
            "max_clock": cpu.MaxClockSpeed,
            "socket": cpu.SocketDesignation,
            "architecture": cpu.AddressWidth
        }

    except:
        return {
            "name": "Unknown",
            "manufacturer": "Unknown",
            "cores": "Unknown",
            "threads": "Unknown",
            "max_clock": "Unknown",
            "socket": "Unknown",
            "architecture": "Unknown"
        }


def get_motherboard():
    if not w:
        return "Unknown"

    try:
        board = w.Win32_BaseBoard()[0]

        return (
            f"Manufacturer: {board.Manufacturer}\n"
            f"Model:        {board.Product}\n"
            f"Serial:       {board.SerialNumber}"
        )

    except:
        return "Unknown"


def get_gpu():
    if not w:
        return "Unknown"

    try:
        gpus = w.Win32_VideoController()

        result = []

        for gpu in gpus:

            if gpu.Name:

                if gpu.AdapterRAM:
                    try:
                        vram = f"{gpu.AdapterRAM / (1024 ** 3):.2f} GB"
                    except:
                        vram = "Unknown"
                else:
                    vram = "Unknown"

                result.append(
                    f"Name:        {gpu.Name}\n"
                    f"VRAM:        {vram}\n"
                    f"Driver:      {gpu.DriverVersion}\n"
                )

        return "\n".join(result)

    except:
        return "Unknown"


def get_ram_info():

    ram = psutil.virtual_memory()

    total = ram.total / (1024 ** 3)

    return f"{total:.2f} GB"


def get_disks():

    result = []

    try:
        for disk in psutil.disk_partitions():

            try:

                usage = psutil.disk_usage(
                    disk.mountpoint
                )

                total = usage.total / (1024 ** 3)
                used = usage.used / (1024 ** 3)
                free = usage.free / (1024 ** 3)

                result.append(
                    f"{disk.device}\n"
                    f"Total: {total:.1f} GB\n"
                    f"Used:  {used:.1f} GB\n"
                    f"Free:  {free:.1f} GB\n"
                )

            except:
                pass

    except:
        pass

    return "\n".join(result)


# =====================================
# اطلاعات ثابت
# =====================================

CPU = get_cpu()
MOTHERBOARD = get_motherboard()
GPU = get_gpu()
RAM = get_ram_info()
DISKS = get_disks()


# =====================================
# پنجره
# =====================================

root = tk.Tk()

root.title("My CPU-Z")
root.geometry("750x520")

root.minsize(
    650,
    450
)


# =====================================
# ظاهر
# =====================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "TNotebook.Tab",
    padding=(18, 8),
    font=("Segoe UI", 10)
)


# =====================================
# Header
# =====================================

header = ttk.Frame(root)

header.pack(
    fill="x",
    padx=15,
    pady=10
)


title = ttk.Label(
    header,
    text="My CPU-Z",
    font=("Segoe UI", 22, "bold")
)

title.pack(side="left")


subtitle = ttk.Label(
    header,
    text="Hardware Information"
)

subtitle.pack(side="right")


# =====================================
# Tabs
# =====================================

notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)


cpu_tab = ttk.Frame(notebook)
mainboard_tab = ttk.Frame(notebook)
memory_tab = ttk.Frame(notebook)
graphics_tab = ttk.Frame(notebook)
storage_tab = ttk.Frame(notebook)
system_tab = ttk.Frame(notebook)


notebook.add(
    cpu_tab,
    text="CPU"
)

notebook.add(
    mainboard_tab,
    text="Mainboard"
)

notebook.add(
    memory_tab,
    text="Memory"
)

notebook.add(
    graphics_tab,
    text="Graphics"
)

notebook.add(
    storage_tab,
    text="Storage"
)

notebook.add(
    system_tab,
    text="System"
)


# =====================================
# ساخت TextBox
# =====================================

def create_box(parent):

    text = tk.Text(
        parent,
        font=("Consolas", 11),
        bg="#f4f4f4",
        fg="#111111",
        relief="flat",
        padx=15,
        pady=15
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    return text


cpu_box = create_box(cpu_tab)
mainboard_box = create_box(mainboard_tab)
memory_box = create_box(memory_tab)
graphics_box = create_box(graphics_tab)
storage_box = create_box(storage_tab)
system_box = create_box(system_tab)


# =====================================
# CPU
# =====================================

cpu_box.insert(
    "1.0",

    f"CPU INFORMATION\n"
    f"==============================\n\n"

    f"Name:          {CPU['name']}\n"
    f"Manufacturer:  {CPU['manufacturer']}\n"
    f"Cores:         {CPU['cores']}\n"
    f"Threads:       {CPU['threads']}\n"
    f"Max Clock:     {CPU['max_clock']} MHz\n"
    f"Socket:        {CPU['socket']}\n"
    f"Architecture:  {CPU['architecture']}-bit\n\n"

    f"CPU Usage:     0 %\n"
)


# =====================================
# Mainboard
# =====================================

mainboard_box.insert(
    "1.0",

    f"MAINBOARD\n"
    f"==============================\n\n"
    f"{MOTHERBOARD}"
)


# =====================================
# Memory
# =====================================

memory_box.insert(
    "1.0",

    f"MEMORY\n"
    f"==============================\n\n"
    f"Total RAM: {RAM}\n\n"
    f"Usage: calculating..."
)


# =====================================
# Graphics
# =====================================

graphics_box.insert(
    "1.0",

    f"GRAPHICS\n"
    f"==============================\n\n"
    f"{GPU}"
)


# =====================================
# Storage
# =====================================

storage_box.insert(
    "1.0",

    f"STORAGE\n"
    f"==============================\n\n"
    f"{DISKS}"
)


# =====================================
# System
# =====================================

system_box.insert(
    "1.0",

    f"SYSTEM\n"
    f"==============================\n\n"

    f"OS:          {platform.system()}\n"
    f"Version:     {platform.release()}\n"
    f"Build:       {platform.version()}\n"
    f"Machine:     {platform.machine()}\n"
    f"Python:      {platform.python_version()}\n"
)


# =====================================
# بروزرسانی فقط اطلاعات لحظه‌ای
# =====================================

def update_live():

    cpu_usage = psutil.cpu_percent(
        interval=None
    )

    ram = psutil.virtual_memory()

    cpu_box.delete(
        "14.0",
        tk.END
    )

    cpu_box.insert(
        tk.END,
        f"\nCPU Usage:     {cpu_usage:.1f} %"
    )

    memory_box.delete(
        "5.0",
        tk.END
    )

    memory_box.insert(
        tk.END,
        f"Usage: {ram.percent:.1f} %\n"
        f"Used:  {ram.used / (1024 ** 3):.2f} GB\n"
        f"Free:  {ram.available / (1024 ** 3):.2f} GB"
    )

    root.after(
        1000,
        update_live
    )


# =====================================
# شروع
# =====================================

update_live()

root.mainloop()