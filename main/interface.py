import threading
import customtkinter
from PIL import Image
from settings.settings import OUT_BOX_TEXT, HEIGHT, WIDTH, X, Y, ICON_PATH
from chatGPT_conversation import ConversationGPT

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')


class ChatGPTFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.out_box = customtkinter.CTkTextbox(self, height=610, corner_radius=10, text_color='#97999c',
                                                state='normal',  font=customtkinter.CTkFont(size=14), wrap='word',
                                                fg_color='#292828')
        self.out_box.grid(row=0, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.out_box.insert('end', f'{OUT_BOX_TEXT}')

        self.input_box = customtkinter.CTkTextbox(self, height=125, corner_radius=10, text_color='#97999c',
                                                  font=customtkinter.CTkFont(size=15), wrap='word', fg_color='#2b2b2b')
        self.input_box.grid(row=1, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.input_box.insert('end', 'Введите текст для общения')

    def handle_key(self, event):
        ctrl = (event.state & 0x4) != 0
        if event.keysym == "Return":
            if event.state != 1:
                input_text = self.input_box.get('1.0', 'end')
                threading.Thread(target=self.process_request, args=(input_text,)).start()
                out_box_text = self.out_box.get('1.0', 'end').replace('\n', '')
                if out_box_text in OUT_BOX_TEXT or out_box_text == '':
                    self.out_box.delete('1.0', 'end')
                    self.out_box.configure(text_color='#eeeee4')
                self.out_box.insert('end', '- ' + input_text + '...' + '\n\n')
                return "break"
        if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            self.input_box.tag_add('sel', '1.0', 'end')

    def handle_event(self, event):
        ctrl = (event.state & 0x4) != 0
        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

        if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            self.out_box.tag_add('sel', '1.0', 'end')

    def on_focus_in(self, event):
        if self.input_box.get('1.0', 'end').replace('\n', '') == "Введите текст для общения":
            self.input_box.delete('1.0', 'end')
            self.input_box.configure(text_color='#d9cfce')
            self.input_box.configure(font=(customtkinter.CTkFont(size=14)))

    def on_focus_out(self, event):
        if self.input_box.get('1.0', 'end').replace('\n', '') == "":
            self.input_box.delete('1.0', 'end')
            self.input_box.insert('end', 'Введите текст для общения')
            self.input_box.configure(font=customtkinter.CTkFont(size=15))
            self.input_box.configure(text_color='#97999c')

    def process_request(self, input_text):
        answer_text = ''
        chat = ConversationGPT(input_text)
        answer_text += str(chat.post_text_gpt())
        self.out_box.insert('end', answer_text + '\n\n')
        self.out_box.see("end")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('ChatGPT')
        self.logo = customtkinter.CTkImage(Image.open(ICON_PATH))
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = ChatGPTFrame(master=self, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(sticky="nsew")
        self.my_frame.input_box.bind("<Key>", self.my_frame.handle_key)
        self.my_frame.input_box.bind("<Key>", self.my_frame.handle_event)
        self.my_frame.out_box.bind("<Key>", self.my_frame.handle_event)
        self.my_frame.input_box.bind('<FocusIn>', self.my_frame.on_focus_in)
        self.my_frame.input_box.bind('<FocusOut>', self.my_frame.on_focus_out)


if __name__ == '__main__':
    app = App()
    app.iconbitmap(ICON_PATH)
    app.geometry(f"{WIDTH}x{HEIGHT}+{X}+{Y}")
    app.resizable(False, False)
    app.mainloop()
