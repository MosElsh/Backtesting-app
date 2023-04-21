import tkinter as tk
import tkinter.messagebox as mb
from styles import Theme
from functions import perform_theme_change, change_image_theme, find_longest_value, get_ticker_list, process_backtest, strategy_list
from datalist import DataList
from strategy_parameters import StrategyParameters


IMAGES_THEME_COMBOS = []
SYMBOLS = get_ticker_list("SPX Ticker List.csv")
POSITIONS = ["Long", "Short"]
STRATEGIES = strategy_list()
width = find_longest_value(SYMBOLS + POSITIONS + STRATEGIES)
theme = Theme()


app = tk.Tk()
app.geometry("800x800")
app.config(background=theme.background)
app.title("Back-Test Your Strategies")
app.iconbitmap("Icons/icon.ico")


arrow_icon_default = tk.PhotoImage(file="Icons/arrow-" + ("dark" if theme.get_dark() else "light") + "-theme.png")
arrow_icon_alternate = tk.PhotoImage(file="Icons/arrow-" + ("dark" if not theme.get_dark() else "light") + "-theme.png")


# Frame that covers the window.
main_frame = tk.Frame(app, background=theme.background)
main_frame.pack(fill="x")




#####       Header Frame Start        #####


# Frame that covers the top (the "header") of the main frame.
header_frame = tk.Frame(main_frame, background=theme.background)
header_frame.pack(fill="x")
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)


# Logo Frame that covers the top left of the header.
logo_frame = tk.Frame(header_frame, background=theme.background)
logo_frame.grid(row=0, column=0, sticky="w", padx="5", pady="5")


# Logo Image
logo_image_default = tk.PhotoImage(file="Logo/logo-" + ("dark" if theme.get_dark() else "light") + "-theme.png").subsample(3, 3)
logo_image_alternate = tk.PhotoImage(file="Logo/logo-" + ("dark" if not theme.get_dark() else "light") + "-theme.png").subsample(3, 3)
logo = tk.Label(logo_frame, image=logo_image_default, background=theme.background, foreground=theme.foreground)
logo.pack()
IMAGES_THEME_COMBOS.append([logo_image_default, logo_image_alternate, logo])


# Title Frame that covers the center of the top of the header.
title_frame = tk.Frame(header_frame, background=theme.background)
title_frame.grid(row=0, column=1)

# Title Label
title_label = tk.Label(title_frame, text="Back-Test Your Strategies", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 20))
title_label.pack()





# Theme Switcher Frame that covers the top right of the header.
theme_switcher_frame = tk.Frame(header_frame, background=theme.background)
theme_switcher_frame.grid(row=0, column=2, sticky="e", padx="5", pady="5")


# Theme Switcher Icon
theme_switcher_icon_default = tk.PhotoImage(file="Icons/theme-switcher-" + ("dark" if theme.get_dark() else "light") + "-theme.png")
theme_switcher_icon_alternate = tk.PhotoImage(file="Icons/theme-switcher-" + ("dark" if not theme.get_dark() else "light" + "-theme.png"))
theme_switcher = tk.Label(theme_switcher_frame, image=theme_switcher_icon_default, background=theme.background, foreground=theme.foreground, cursor=theme.cursor)
theme_switcher.bind("<Button-1>", lambda event: [perform_theme_change(app, theme), [change_image_theme(IMAGES_THEME_COMBOS[x][2], theme, IMAGES_THEME_COMBOS[x]) for x in range(len(IMAGES_THEME_COMBOS))]])
theme_switcher.pack()
IMAGES_THEME_COMBOS.append([theme_switcher_icon_default, theme_switcher_icon_alternate, theme_switcher])



#####       Header Frame End        #####



# Create Space
space_frame = tk.Frame(main_frame, background=theme.background)
space_frame.pack(pady=20)


#####       Content Frame Start        #####


# Content Frame
content_frame = tk.Frame(main_frame, background=theme.background)
content_frame.pack()
content_frame.tkraise()


# Symbol Frame
symbol_frame = tk.Frame(content_frame, background=theme.background)
symbol_frame.pack()


# Symbol Label
symbol_label = tk.Label(symbol_frame, text="Symbol:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 16))
symbol_label.grid(row=0, column=0, sticky="n")


# Datalist Frame
symbol_datalist_frame = tk.Frame(symbol_frame, background=theme.background)
symbol_datalist_frame.grid(row=0, column=1, sticky="n")


# Symbol Datalist
symbol_datalist = DataList(symbol_datalist_frame, SYMBOLS, theme, width, arrow_icon_default)
IMAGES_THEME_COMBOS.append([arrow_icon_default, arrow_icon_alternate, symbol_datalist.return_arrow_label()])


# Info Icon
info_icon_default = tk.PhotoImage(file="Icons/info-" + ("dark" if theme.get_dark() else "light") + "-theme.png")
info_icon_alternate = tk.PhotoImage(file="Icons/info-" + ("dark" if not theme.get_dark() else "light" + "-theme.png"))
info_icon_label = tk.Label(symbol_frame, image=info_icon_default, background=theme.background, foreground=theme.foreground, cursor=theme.cursor)
info_icon_label.grid(row=0, column=2, sticky="n", padx=5)
info_icon_label.bind("<Button-1>", lambda event: mb.showinfo(title="Symbol Selection", message="Select a symbol to back-test your strategy on."))
IMAGES_THEME_COMBOS.append([info_icon_default, info_icon_alternate, info_icon_label])


# Create Space
space_frame = tk.Frame(content_frame, background=theme.background)
space_frame.pack(pady=10)


# Position Frame
position_frame = tk.Frame(content_frame, background=theme.background)
position_frame.pack()


# Position Label
position_label = tk.Label(position_frame, text="Position:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 16))
position_label.grid(row=0, column=0, sticky="n")


# Datalist Frame
position_datalist_frame = tk.Frame(position_frame, background=theme.background)
position_datalist_frame.grid(row=0, column=1, sticky="n")


# Position Datalist
position_datalist = DataList(position_datalist_frame, POSITIONS, theme, width, arrow_icon_default)
IMAGES_THEME_COMBOS.append([arrow_icon_default, arrow_icon_alternate, position_datalist.return_arrow_label()])


# Info Icon
info_icon_default = tk.PhotoImage(file="Icons/info-" + ("dark" if theme.get_dark() else "light") + "-theme.png")
info_icon_alternate = tk.PhotoImage(file="Icons/info-" + ("dark" if not theme.get_dark() else "light" + "-theme.png"))
info_icon_label = tk.Label(position_frame, image=info_icon_default, background=theme.background, foreground=theme.foreground, cursor=theme.cursor)
info_icon_label.grid(row=0, column=2, sticky="n", padx=5)
info_icon_label.bind("<Button-1>", lambda event: mb.showinfo(title="Select Position", message="Choose either long or short as your position entries for the back-test."))
IMAGES_THEME_COMBOS.append([info_icon_default, info_icon_alternate, info_icon_label])


# Create Space
space_frame = tk.Frame(content_frame, background=theme.background)
space_frame.pack(pady=10)


# Strategy Frame
strategy_frame = tk.Frame(content_frame, background=theme.background)
strategy_frame.pack()


# Strategy Label 
strategy_label = tk.Label(strategy_frame, text="Strategy: ", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 16))
strategy_label.grid(row=0, column=0, sticky="n")


# Datalist Frame
strategy_datalist_frame = tk.Frame(strategy_frame, background=theme.background)
strategy_datalist_frame.grid(row=0, column=1, sticky="n")



# Strategy Parameters Container (Not Displayed Yet)
strategy_params_container = tk.Frame(content_frame, background=theme.background)
strategy_params_container.pack(pady=10)
tk.Frame(strategy_params_container, background=theme.background).pack()     # Empty initial frame as no strategy is chosen yet.

# Strategy Datalist
strategy_datalist = DataList(strategy_datalist_frame, STRATEGIES, theme, width, arrow_icon_default)
IMAGES_THEME_COMBOS.append([arrow_icon_default, arrow_icon_alternate, strategy_datalist.return_arrow_label()])
parameters = StrategyParameters()
strategy_datalist.get_listbox().bind("<<ListboxSelect>>",
    lambda event: [
        strategy_params_container.winfo_children()[0].destroy(),
        strategy_datalist.insert_selected_data(),
        parameters.update_display(strategy_params_container, strategy_datalist.get_selected(), theme)
    ]
)

# Info Icon
info_icon_default = tk.PhotoImage(file="Icons/info-" + ("dark" if theme.get_dark() else "light") + "-theme.png")
info_icon_alternate = tk.PhotoImage(file="Icons/info-" + ("dark" if not theme.get_dark() else "light" + "-theme.png"))
info_icon_label = tk.Label(strategy_frame, image=info_icon_default, background=theme.background, foreground=theme.foreground, cursor=theme.cursor)
info_icon_label.grid(row=0, column=2, sticky="n", padx=5)
info_icon_label.bind("<Button-1>", lambda event: mb.showinfo(title="Choose A Strategy", message="Choose a strategy to back-test."))
IMAGES_THEME_COMBOS.append([info_icon_default, info_icon_alternate, info_icon_label])


#####       Content Frame End        #####



#####       Back-Test Results Frame Start        #####


backtest_results_container = tk.Frame(main_frame, background=theme.background)


button_frame = tk.Frame(content_frame, background=theme.background, highlightbackground=theme.foreground, highlightthickness=1)
button_frame.pack(pady=10)
button = tk.Button(
    button_frame,
    text="Submit",
    background=theme.background,
    foreground=theme.foreground,
    relief="flat",
    font=("tkDefaultFont", 14),
    activebackground=theme.foreground,
    activeforeground=theme.background,
    cursor=theme.cursor
)
button.bind("<Button-1>", lambda event: process_backtest(backtest_results_container, symbol_datalist.get_selected(), position_datalist.get_selected(), strategy_datalist.get_selected(), higher_value=parameters.get_higher_value(), lower_value=parameters.get_lower_value()))
button.pack()


backtest_results_container.pack()

#####       Back-Test Results Frame End        #####


app.mainloop()