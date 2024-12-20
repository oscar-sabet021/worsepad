import tkinter as tk
from tkinter import filedialog, ttk, font, messagebox
import qr
# import platform
# import PIL
from PIL import Image, ImageTk

colors = {
    'Black': '#000000',
    'White': '#FFFFFF',
    'Red': '#FF0000',
    'Lime':	'#00FF00',
    'Blue':	'#0000FF',
    'Yellow': '#FFFF00',
    'Cyan': '#00FFFF',
    'Magenta': '#FF00FF',
    'Silver': '#C0C0C0',
    'Gray':	'#808080',
    'Maroon': '#800000',
    'Olive': '#808000',
    'Green': '#008000',
    'Purple': '#800080',
    'Teal':	'#008080',
    'Navy':	'#000080',
}
color_keys = ['Black', 'White', 'Red', 'Lime', 'Blue', 'Yellow', 'Cyan', 'Magenta', 'Silver', 'Gray', 'Maroon', 'Olive', 'Green', 'Purple', 'Teal', 'Navy']

WorsePad = tk.Tk()
WorsePad.wm_geometry('800x600+0+0')
# WorsePad.iconbitmap(r'kwrite.gif')

#used for timing temp file
timer = 0

# used for find and replace func
index_start = '1.0'
index_end = '1.0'

selected_fg = tk.StringVar()
selected_fg.set('Black')
selected_bg = tk.StringVar()
selected_bg.set('White')

font_size = tk.IntVar()
font_size.set(14)

# vars for font type
selected_font = tk.StringVar()
selected_font.set('Calibri')

# vars for font weight
# font_weights = ('normal', 'bold')
selected_weight = tk.StringVar()
selected_weight.set('normal')

#Used for menu sepArator
separators = []

#Current working file
current_filename = 'Untitled.txt'
WorsePad.wm_title(f'Worsepad - {current_filename}')

def increment_timer():
    global timer
    timer += 1
    # print(timer)
    if timer >= 500:
        temp_update()
        timer = 0
    
    WorsePad.after(500, increment_timer)
    
def convert_icon():
    # my_os = platform.system()
    # if my_os == 'windows':
        # pass
    # elif my_os == 'Linux':
    try:
        image_open = Image.open('WorsePad.png')
    except:
        image_open = Image.open(r'/home/user/python/Programming/projects/worsepad/WorsePad.png')
    image = ImageTk.PhotoImage(image_open)
    WorsePad.iconphoto(True, image)
    # elif my_os == 'Darwin':
        # pass
    
def msgbox(msg):
    messagebox.showwarning('Warning', msg)

def new_qr_code(text):
    print(len(text))
    if len(text) == 1:
        msgbox('No text in document found')
    elif len(text) > 2340:
        msgbox('Text exceeds character limit')
    else:
        qr.gen_qr_code(text)
        

def update_current_filename(filename):
    global current_filename
    if '/' in filename:
        cwf = filename.split('/')
        update_current_filename(cwf[-1])
        WorsePad.wm_title(f'Worsepad - {cwf}')
        current_filename = cwf[-1]
    elif '\\' in filename:
        cwf = filename.split('\\')
        print(cwf)        
        current_filename = cwf[-1]
        WorsePad.wm_title(f'Worsepad - {cwf}')
    else:
        WorsePad.wm_title(f'Worsepad - {filename}')
        current_filename = filename
    
def add_separator():
    """Adds separator to global list"""
    global separators
    
    separators.append(ttk.Separator(menu_frame, orient='vertical'))
    separators[-1].pack(padx=5, side=tk.LEFT, fill=tk.Y)
    
def temp_update():
    filename = current_filename.split('.')
    # print(filename)
    file = text_area.get('1.0', 'end')
    
    f = open(f'{filename[0]}.tmp', 'w+')
    f.write(file)
    f.close()
    
def new_file():
    """Saves to a new file
    """
    global text_area
    try:
        save_file()
    except:
        pass
    text_area.delete(1.0, 'end')


def save_file():
    """Saves current file
    """
    global text_area
    text = text_area.get("1.0", "end-1c")
    location = filedialog.asksaveasfilename(
        initialfile='Untitled.txt',
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )
    file = open(location, "w+")
    file.write(text)
    update_current_filename(location)
    file.close()


def open_file():
    """Open new file
    """
    global text_area
    temp = ''

    location = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )

    file = open(location, 'r', encoding='utf-8-sig')
    for line in file:
        temp += line

    text_area.delete(1.0, 'end')
    text_area.insert(1.0, temp)
    fn = location.split('/')
    update_current_filename(fn[-1])

# def save_temp():
    
    # print('save_temp')

def set_font():

    fs = font_size.get()
    sf = selected_font.get()
    fw = selected_weight.get()

    new_font = font.Font(family=sf, size=fs, weight=fw)
    text_area.configure(font=new_font)

def zoom_font(choice):

    if choice == 'in':
        font_size.set(font_size.get() + 2)
    elif choice == 'out':
        font_size.set(font_size.get() - 2)
    fs = font_size.get()
    sf = selected_font.get()
    fw = selected_weight.get()

    new_font = font.Font(family=sf, size=fs, weight=fw)
    text_area.configure(font=new_font)

def word_wrap(choice):
    global text_area

    if choice == 'none':
        text_area.configure(wrap='none')
    elif choice == 'char':
        text_area.configure(wrap='char')
    elif choice == 'word':
        text_area.configure(wrap='word')
        
def font_window():      
    font_separators = []
    
    def add_separator_font():
        font_separators.append(ttk.Separator(Font_Window, orient='vertical'))
        font_separators[-1].pack(padx=5, side=tk.LEFT, fill=tk.Y)

    fonts = font.families()
    
    font_sizes = []
    for x in range(2, 72, 2):
        font_sizes.append(x)
    
    font_weights = ('normal', 'bold')
    
    Font_Window = tk.Toplevel()
    Font_Window.wm_title('Set Font')
    
    font_label = ttk.Label(Font_Window, text='Font:')
    font_label.pack(side=tk.LEFT)

    select_font = ttk.Combobox(
        Font_Window,
        textvariable=selected_font,
        values=fonts,
        state='READONLY',
    )
    select_font.bind('<<ComboboxSelected>>', lambda x: set_font())
    select_font.pack(side=tk.LEFT, anchor=tk.W, padx=5)

    add_separator_font()

    font_size_label = ttk.Label(Font_Window, text='Size: ')
    font_size_label.pack(side=tk.LEFT)

    font_sizes = ttk.Combobox(
        Font_Window,
        textvariable=font_size,
        values=font_sizes,
        width=3,
        state='READONLY'
    )
    font_sizes.bind('<<ComboboxSelected>>', lambda x: set_font())
    font_sizes.pack(side=tk.LEFT, padx=5)

    add_separator_font()

    font_weight_label = ttk.Label(Font_Window, text='Weight: ')
    font_weight_label.pack(side=tk.LEFT)

    font_weight = ttk.Combobox(
        Font_Window,
        textvariable=selected_weight,
        values=font_weights,
        width=7,
        state='READONLY',
    )
    font_weight.bind('<<ComboboxSelected>>', lambda x: set_font())
    font_weight.pack(side=tk.LEFT, padx=5, pady=5)
    
    Font_Window.mainloop()

def dark_mode(mode):

    if mode == 'dark':
        text_area.configure(bg='black', fg='white')
    elif mode == 'light':
        text_area.configure(bg='white', fg='black')


def background_color():
    color = selected_bg.get()
    fg = selected_fg.get()

    text_area.configure(bg=colors[color], fg=colors[fg])


def text_color():
    color = selected_fg.get()

    text_area.configure(fg=colors[color])


def find_and_replace():
    global index_start
    global index_end
    
    def on_closing():
        global index_start
        global index_end
        index_start = '1.0'
        index_end = '1.0'

        text_area.tag_delete('start', 'end')
        search_str.set('')
        search_window.destroy()

    def search_for_term(search_term, start_index):
        global index_start
        global index_end

        start_index = text_area.search(search_term, start_index)
        try:
            row_num, col_num = map(int, start_index.split('.'))
            end_index = f'{row_num}.{col_num+len(search_term)}'
            index_start = start_index
            index_end = end_index
            return (start_index, end_index)
        except:
            print('Error: func; search_for_term; Invalid Search index')

    def add_highlight(highlight_index):
        if highlight_index[0] != -1:
            text_area.tag_delete('start', 'end')
            text_area.tag_add("start", highlight_index[0], highlight_index[1])
            text_area.tag_config(
                "start", background="blue", foreground="white")
        return highlight_index

    def replace_text(replace_term, string_index):
        if replace_term == '':
            return False
        else:
            text_area.replace(string_index[0], string_index[1], replace_term)
            x, y = map(int, string_index[0].split('.'))
            end_index = f'{x}.{y+len(replace_term)}'
            add_highlight((string_index[0], end_index))
            return True

    def replace_all(input_term, replace_term, string_index):
        global index_start
        not_finished = True
        while not_finished:
            idx = search_for_term(input_term, index_start)
            if idx[0] == '1.-1':
                not_finished = False
            else:
                not_finished = replace_text(replace_term, idx)

    search_window = tk.Toplevel()
    search_window.wm_title('Find & Replace')

    search_str = tk.StringVar()
    replace_str = tk.StringVar()

    Find_term_label = ttk.Label(search_window, text='Find Term:')
    Find_term_label.grid(
        padx=5, pady=5,
        row=0, column=0
    )
    input_term = ttk.Entry(search_window, textvariable=search_str, width=37)
    input_term.grid(
        padx=5, pady=5,
        row=0, column=1
    )
    search_button = ttk.Button(search_window, text='Search Next', command=lambda: add_highlight(
        search_for_term(input_term.get(), index_end)))
    search_button.grid(
        padx=5, pady=5,
        row=0, column=2
    )
    replace_term_label = ttk.Label(search_window, text='Replace Term:')
    replace_term_label.grid(
        padx=5, pady=5,
        row=1, column=0
    )
    replace_term = ttk.Entry(search_window, textvariable=replace_str, width=37)
    replace_term.grid(
        padx=5, pady=5,
        row=1, column=1
    )
    replace_button = ttk.Button(search_window, text='Replace', command=lambda: replace_text(
        replace_term.get(), search_for_term(input_term.get(), index_start)))
    replace_button.grid(
        padx=5, pady=5,
        row=1, column=2
    )
    replace_all_button = ttk.Button(search_window, text='Replace All',
                                    command=lambda: replace_all(input_term.get(), replace_term.get(), search_for_term(
                                        input_term.get(), index_start)))
    replace_all_button.grid(
        padx=5, pady=5,
        row=1, column=3
    )
    
    search_window.protocol("WM_DELETE_WINDOW", on_closing)
    search_window.mainloop()

def right_click_menu(event):
    try:
        text_area_rcm.tk_popup(event.x_root, event.y_root)
    finally:
        text_area_rcm.grab_release()
        
def find_term(term):
    global text_area

    text = text_area.get("1.0", "end-1c")

    start_index = text.find(term)
    end_index = start_index + len(term)
    return (start_index, end_index)


def replace_term(index, replace):
    global text_area
    text = text_area.get("1.0", "end-1c")

    if replace != 'none':
        new_text = text[:index[0]] + replace + text[index[1]:]
        text_area.delete('1.0', 'end')
        text_area.insert('1.0', new_text)

def popup_unfocus(event=None):
        text_area_rcm.unpost()

def select_all(event):
    text_area.tag_add(tk.SEL, "1.0", tk.END)
    text_area.mark_set(tk.INSERT, "1.0")
    text_area.see(tk.INSERT)
    return 'break'

# Clipboard functions
def update_clipboard(text):
    text_area.clipboard_clear()
    text_area.clipboard_append(text)
    
def copy_highlight():
    try:
        temp = text_area.selection_get()
    except:
        print('ERROR: No text highlighted')
    if len(temp) > 0:
        update_clipboard(temp)
    return 

def cut_highlight():
    temp = ''
    try:
        temp = text_area.selection_get()
    except:
        print('ERROR: No text highlighted')
        
    if len(temp) > 0:
        temp = text_area.selection_get()
        update_clipboard(temp)
        text_area.delete("sel.first", "sel.last")
    return

def paste_string():
    text_area.insert('insert', text_area.clipboard_get())

def about_msgbox():
    messagebox.showinfo('WorsePad V0.1a', 'WorsePad V0.1a')
    
def help_page():
    messagebox.showinfo('Help', "It's here in spirit")
    
control = 'CTRL + '
menu_frame = tk.Frame(WorsePad, ) #bg='white')

menu_frame.pack(side=tk.TOP, anchor=tk.NW)
menu_bar = tk.Menu(WorsePad, tearoff=0,) #bg='white')

file_menu = tk.Menu(menu_bar, tearoff=0,)# bg='#efefef')
file_menu.add_command(label=f'New, {control:>}N', command=new_file)
file_menu.add_command(label=f'Open, {control:>}O', command=open_file)
file_menu.add_command(label=f'Save, {control:>}S', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=WorsePad.quit)
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
control = 'CTRL + '

edit_menu.add_command(label=f'Find & Replace, {control:>}F', command=lambda: find_and_replace())
edit_menu.add_separator()
edit_menu.add_command(label=f'Cut, {control:>7}X', command=cut_highlight)
edit_menu.add_command(label=f'Copy, {control}C', command=copy_highlight)
edit_menu.add_command(label=f'Paste, {control}V', command=paste_string)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

#The view menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label=f'Set Font, {control:>}U', command=font_window)
view_menu.add_separator()
view_menu.add_command(label='Dark Mode', command=lambda: dark_mode('dark'))
view_menu.add_command(label='Light Mode', command=lambda: dark_mode('light'))

word_wrap_menu = tk.Menu(view_menu, tearoff=0)
word_wrap_menu.add_command(label='none', command=lambda: word_wrap('none'))
word_wrap_menu.add_command(label='char', command=lambda: word_wrap('char'))
word_wrap_menu.add_command(label='word', command=lambda: word_wrap('word'))
view_menu.add_cascade(label='Word Wrap', menu=word_wrap_menu)

menu_bar.add_cascade(label='View', menu=view_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label='Handbook (F1)', command=help_page)
help_menu.add_command(label='About WorsePad', command=about_msgbox)
menu_bar.add_cascade(label='Help', menu=help_menu)
# help_menu.add_command(label=''

add_separator()

bg_label = ttk.Label(menu_frame, text='bg:',)
bg_label.pack(side=tk.LEFT)

bg_color = ttk.Combobox(
    menu_frame,
    textvariable=selected_bg,
    values=color_keys,
    state='READONLY',
    width=8
)
bg_color.pack(side=tk.LEFT)

add_separator()

fg_label = ttk.Label(menu_frame, text='fg: ',)
fg_label.pack(side=tk.LEFT)
fg_color = ttk.Combobox(
    menu_frame,
    textvariable=selected_fg,
    values=color_keys,
    width=8,
    state='READONLY',
)
fg_color.pack(side=tk.LEFT)

add_separator()

fg_label = ttk.Label(menu_frame, text='Zoom: ')
fg_label.pack(side=tk.LEFT)

zoom_in = ttk.Button(
    menu_frame,
    command=lambda: zoom_font('in'),
    text='+',
    width=2
)
zoom_in.pack(side=tk.LEFT)

zoom_out = ttk.Button(
    menu_frame,
    text='-',
    command=lambda: zoom_font('out'),
    width=2
)
zoom_out.pack(side=tk.LEFT)

add_separator()

qr_code = ttk.Button(menu_frame, text='QR-Code', command=lambda: new_qr_code(text_area.get('1.0', 'end')))
qr_code.pack(side=tk.LEFT)
WorsePad.config(menu=menu_bar)

text_canvas = tk.Canvas(
    WorsePad,
)
text_canvas.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

text_frame = tk.Frame(
    text_canvas,
)
text_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
text_frame.grid_propagate(False)

text_area = tk.Text(text_frame, relief='sunken')
text_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=2, pady=2)
# text_area.bind("<Control-Key-a>", select_all)
# text_area.bind("<Control-Key-A>", select_all)

#Right click popup menu
text_area_rcm = tk.Menu(text_frame, tearoff=0)
text_area_rcm.add_command(label="Cut",   command=cut_highlight)
text_area_rcm.add_command(label="Copy",  command=copy_highlight)
text_area_rcm.add_command(label="Paste", command=paste_string)
text_area_rcm.add_command(label="QR from selected text", command=lambda: new_qr_code(text_area.selection_get()))
# text_area_rcm.bind("<FocusOut>",popup_unfocus)

text_scrollbar = ttk.Scrollbar(text_area, command=text_area.yview)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
text_scrollbar.config(command=text_area.yview)

horizontal_scrollbar = ttk.Scrollbar(text_area, orient='horizontal', command=text_area.xview)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
horizontal_scrollbar.config(command=text_area.xview)


bg_color.bind('<<ComboboxSelected>>', lambda x: background_color())
fg_color.bind('<<ComboboxSelected>>', lambda x: background_color())
text_area.bind("<Control-Key-a>", lambda x:select_all())
text_area.bind("<Control-Key-A>", lambda x:select_all())
text_area.bind("<Control-Key-f>", lambda x:find_and_replace())
text_area.bind("<Control-Key-F>", lambda x:find_and_replace())
text_area.bind("<Control-Key-u>", lambda x:font_window())
text_area.bind("<Control-Key-U>", lambda x:font_window())
text_area.bind("<Control-Key-n>", lambda x:new_file())
text_area.bind("<Control-Key-N>", lambda x:new_file())
text_area.bind("<Control-Key-o>", lambda x:open_file())
text_area.bind("<Control-Key-O>", lambda x:open_file())
text_area.bind("<Control-Key-s>", lambda x:save_file())
text_area.bind("<Control-Key-S>", lambda x:save_file())
text_area_rcm.bind("<FocusOut>",popup_unfocus)
text_area.bind("<Button-3>", right_click_menu)
text_area.configure(xscrollcommand=horizontal_scrollbar.set,
                    yscrollcommand=text_scrollbar.set)

convert_icon()
set_font()


if __name__ == "__main__":
    increment_timer()
    # WorsePad.after(50, save_temp) 
    WorsePad.mainloop()
# WorsePad.mainloop()
