import threading
import customtkinter
from PIL import Image

from main.chatGPT_conversation import ConversationGPT

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')


class ChatGPTFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.out_box = customtkinter.CTkTextbox(self, height=500, corner_radius=10, text_color='#ffffff',
                                                state='normal')
        self.out_box.grid(row=1, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")

        self.input_box = customtkinter.CTkTextbox(self, height=115, corner_radius=10, text_color='#eeeee4')
        self.input_box.grid(row=2, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")

    def handle_key(self, event):
        ctrl = (event.state & 0x4) != 0
        if event.keysym == "Return":
            if event.state != 1:
                input_text = self.input_box.get('1.0', 'end')
                threading.Thread(target=self.process_request, args=(input_text,)).start()  # Запуск запроса в отдельном потоке
                self.out_box.insert('end', '- ' + input_text + '...' + '\n\n')
                return "break"

        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

        if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            self.input_box.tag_add('sel', '1.0', 'end')

    def process_request(self, input_text):
        # Выполнение запроса на сервер
        chat = ConversationGPT(input_text)
        answer_text = chat.post_text_gpt()
        # Обновление GUI в главном потоке
        self.out_box.insert('end', answer_text + '\n\n')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('ChatGTP')
        self.logo = customtkinter.CTkImage(Image.open('../icon/2.ico'))
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = ChatGPTFrame(master=self, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")
        self.my_frame.input_box.bind("<Key>", self.my_frame.handle_key)
        self.my_frame.out_box.bind("<Key>", self.my_frame.handle_key)


if __name__ == '__main__':
    width = 500
    height = 630
    x = 700
    y = 150
    app = App()
    app.iconbitmap('../icon/2.ico')
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.resizable(False, False)
    app.mainloop()
