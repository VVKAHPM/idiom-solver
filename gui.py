import json
import re
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
from pypinyin import pinyin, Style
from solver.filter import prune

ChineseFont = "楷体"
EnglishFont = "'Times New Roman'"

class ColorBox(tk.Label):

    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, width=6, height=3, font=(ChineseFont, 16), relief="raised", **kwargs)
        self.state = 2
        self.text = text
        self.bind("<Button-1>", self.toggle_color)
        self.update_color()

    def toggle_color(self, event=None):
        self.state = (self.state + 1) % 3
        self.update_color()

    def update_color(self):
        colors = {0: "#1D9C9C", 1: "#DE7525", 2: "#9CA3AF"}
        self.config(bg=colors[self.state])
    
    def get_state(self):
        if self.text == '-': 
            return -1
        return self.state

    def set_text(self, new_text):
        self.config(text=new_text)
        self.text = new_text


class IdiomCell(tk.Frame):

    def __init__(self, master, parent):
        super().__init__(master, bd=1, relief="solid", padx=5, pady=5)
        
        self.master = master
        self.parent = parent
        self.entry = tk.Entry(self, width=3, font=(ChineseFont, 36), justify="center")
        self.entry.grid(row=0, column=0, columnspan=4, padx=8, pady=8, ipadx=8, ipady=15)
        self.entry.bind("<KeyRelease>", lambda event: (self.update_pinyin(event), self.parent.update_all_pinyin(event)))

        self.char_box = ColorBox(self, "字")
        self.initial_box = ColorBox(self, "声")
        self.final_box = ColorBox(self, "韵")
        self.tone_box = ColorBox(self, "调")

        self.char_box.grid(row=1, column=0)
        self.initial_box.grid(row=1, column=1)
        self.final_box.grid(row=1, column=2)
        self.tone_box.grid(row=1, column=3)

    def update_pinyin(self, event=None):
        word = self.entry.get().strip()
        if len(word) == 1:
            try:
                initial = pinyin(word, style=Style.INITIALS, strict=False)[0][0]
                final = pinyin(word, style=Style.FINALS, strict=False)[0][0]
                tone = pinyin(word, style=Style.TONE3, strict=False)[0][0]
                tone_number = ''.join(filter(str.isdigit, tone)) or '0'

                self.char_box.set_text(word)
                self.initial_box.set_text(initial or "-")
                self.initial_box.config(font=(EnglishFont, 16))
                self.final_box.set_text(final or "-")
                self.final_box.config(font=(EnglishFont, 16))
                self.tone_box.set_text(tone_number)
                self.tone_box.config(font=(EnglishFont, 16))

            except Exception as e:
                print("拼音解析出错:", e)
        else:
            self.char_box.set_text("字")
            self.initial_box.set_text("声")
            self.final_box.set_text("韵")
            self.tone_box.set_text("调")
            self.char_box.config(font=(ChineseFont, 16))
            self.initial_box.config(font=(ChineseFont, 16))
            self.final_box.config(font=(ChineseFont, 16))
            self.tone_box.config(font=(ChineseFont, 16))
    def reset(self):
        self.entry.delete(0, tk.END)
        self.char_box.config(text="字", font=(ChineseFont, 16))
        self.char_box.state = 2
        self.char_box.update_color()

        self.initial_box.config(text="声", font=(ChineseFont, 16))
        self.initial_box.state = 2
        self.initial_box.update_color()

        self.final_box.config(text="韵", font=(ChineseFont, 16))
        self.final_box.state = 2
        self.final_box.update_color()

        self.tone_box.config(text="调", font=(ChineseFont, 16))
        self.tone_box.state = 2
        self.tone_box.update_color()

class IdiomSolverApp:
    def __init__(self, master):
        self.master = master
        
        self.guess_input = [] 
        self.candidates = []  
        self.idioms = []
        self.idiomdict = {}
        self.load_candidates()  
        
        self.create_widgets()
        self.update_candidate_list()

    def load_candidates(self):
        with open("data/processed_idioms.json", "r", encoding="utf-8") as f:
            self.idioms = json.load(f)
        self.idiomdict = {item["word"] : [list(item["word"]), item["initials"], item["finals"], item["tones"]] for item in self.idioms}
        self.candidates = [item["word"] for item in self.idioms]

    def create_widgets(self):

        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack(pady=20)
        self.cells = []
        for i in range(4):
            cell = IdiomCell(self.entry_frame, self)
            cell.grid(row=0, column=i, padx=5)
            self.cells.append(cell)
        
        self.submit_button = tk.Button(self.master, text="提交", command=self.on_submit, font=("黑体", 14))
        self.submit_button.pack(pady=10)
        reset_button = tk.Button(self.master, text="重新开始", command=self.reset, font=("黑体", 14))
        reset_button.pack(pady=5)

        self.candidate_frame = tk.Frame(self.master)
        self.candidate_frame.pack(side="left", padx=20, pady=10)
        self.candidate_label = tk.Label(self.candidate_frame, text="候选词列表", font=("黑体", 14))
        self.candidate_label.pack()
        self.candidate_listbox = tk.Listbox(self.candidate_frame, width=30, height=10, font=("黑体", 12))
        self.candidate_listbox.pack()
    def update_all_pinyin(self, event=None):
        word = "".join([cell.entry.get().strip() for cell in self.cells])
        
        if len(word) != 4 or not all('\u4e00' <= ch <= '\u9fff' for ch in word):
            return

        try:
            item = next((item for item in self.idioms if item["word"] == word), None)
            initials = item["initials"]
            finals = item["finals"]
            tones = item["tones"]

            for i, cell in enumerate(self.cells):
                ch = word[i]
                ini = initials[i] or "-"
                fin = finals[i] or "-"
                tone_number = ''.join(filter(str.isdigit, tones[i])) or '0'

                cell.char_box.set_text(ch)
                cell.initial_box.set_text(ini)
                cell.initial_box.config(font=(EnglishFont, 16))
                cell.final_box.set_text(fin)
                cell.final_box.config(font=(EnglishFont, 16))
                cell.tone_box.set_text(tone_number)
                cell.tone_box.config(font=(EnglishFont, 16))

        except Exception as e:
            print("拼音解析出错:", e)
    def on_submit(self):
        # 获取用户输入并更新候选词
        guess = "".join([cell.entry.get().strip() for cell in self.cells])
        flag = True
        for cell in self.cells:
            if len(cell.entry.get().strip()) != 1:
                tk.messagebox.showerror("输入错误", "请在每个格内输入一个汉字！")
                flag = False
                break
        if flag:
            if bool(re.fullmatch(r'^[\u4e00-\u9fff]{4}$', guess)):
                feedback = self.get_user_feedback()  # 获取用户反馈
                self.candidates = prune(guess, feedback, self.candidates, self.idiomdict)  

                self.update_candidate_list()
            else:
                tk.messagebox.showerror("输入错误", "请输入四个汉字！")
        for cell in self.cells:
            cell.reset()


    def get_user_feedback(self):
        feedback = []

        feedback.append([cell.char_box.get_state() for cell in self.cells])
        feedback.append([cell.initial_box.get_state() for cell in self.cells])
        feedback.append([cell.final_box.get_state() for cell in self.cells])
        feedback.append([cell.tone_box.get_state() for cell in self.cells])
        print(feedback)
        return feedback

    def update_candidate_list(self):
        self.candidate_listbox.delete(0, tk.END)
        for cand in self.candidates[:10]:
            self.candidate_listbox.insert(tk.END, cand)
    
    def reset(self):
        self.candidate_listbox.delete(0, tk.END)
        self.load_candidates()
        self.update_candidate_list()
        for cell in self.cells:
            cell.reset()