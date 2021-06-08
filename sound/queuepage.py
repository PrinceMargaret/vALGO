import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import time
import footer
import voice_assistance
from tkinter.simpledialog import askstring

class queue_contents(object):
    def __init__(self,ancestorpage,parentframe,width,height):

        self.queue_l = []
        self.queue_canvas = []
        self.x = 20
        self.y = 40

        self.back = ttk.Button(master=parentframe, text="← Back", command=lambda: self.raise_frame(ancestorpage))
        self.back.pack(anchor="w", padx=40, pady=20)
        self.heading = ttk.Label(master=parentframe, text="Queue", font=('Helvetica', 14))
        self.heading.pack(fill=tk.X, padx=40, pady=10)

        self.definition = ttk.Label(master=parentframe, wraplength=width - 10, font=('Helvetica', 12), justify='left', text="A Queue is a linear structure which follows a particular order in which the operations are performed. The order is First In First Out (FIFO)")
        self.definition.pack(fill=tk.X, padx=40, pady=10)

        self.set_of_operations = tk.Frame(master=parentframe, padx=40, bg="#464646")

        self.node = ttk.Entry(master=self.set_of_operations)
        self.node.insert(0, "Enter node value")

        self.node.bind('<Button-1>',self.deletetext)

        
        self.output_frame = ttk.Frame(master=parentframe)

        self.output = tk.Canvas(master=self.output_frame, bg="#464646", bd=1, highlightthickness=1,
                            highlightbackground="#d8d8d8", relief=tk.FLAT, scrollregion=(0, 0, 100, 100))
        self.size = None

        self.enqueue_b = ttk.Button(master=self.set_of_operations, text="ENQUEUE", command=lambda: self.enqueue(self.output))
        self.dequeue_b = ttk.Button(master=self.set_of_operations, text="DEQUEUE", command=lambda: self.dequeue(self.output))

        self.top_b = ttk.Button(master=self.set_of_operations, text="PEEK", command=lambda: self.peek(self.output))
        self.size_b = ttk.Button(master=self.set_of_operations, text="SIZE", command=lambda: self.size_(self.output))

        self.instructor = voice_assistance.voice_assistant()
        self.allow_speaking=False
        self.voice_b = ttk.Button(master=self.set_of_operations,  text="🔊 Guide", command=lambda: self.guide(self.output))
        self.allow_execution=True

        self.node.pack(side=tk.LEFT, ipady=4, ipadx=4)
        self.enqueue_b.pack(side=tk.LEFT, padx=2)
        self.dequeue_b.pack(side=tk.LEFT, padx=2)
        self.top_b.pack(side=tk.LEFT, padx=2)
        self.size_b.pack(side=tk.LEFT, padx=2)

        self.voice_b.pack(side=tk.LEFT, padx=2)


        self.set_of_operations.pack(fill=tk.X)

        self.horscroll = tk.Scrollbar(master=self.output_frame, orient=tk.HORIZONTAL)
        self.horscroll.configure(command=self.output.xview)
        self.horscroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.output.configure(xscrollcommand=self.horscroll.set)

        self.output.pack(fill=tk.BOTH, expand=1)
        self.output_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=1)
        self.end = footer.footerlabel(parentframe)

    def deletetext(self,event):
        event.widget.delete(0,"end")
        return None
    def raise_frame(self,ancestorpage):
        ancestorpage.tkraise()

    def explain(self,sentence):
        if self.allow_speaking:
            self.instructor.speak(sentence)

    def guide(self,output):
        v = self.allow_speaking
        self.allow_speaking = (not v)
        if self.allow_speaking:
            self.voice_b.config(text="🔊 On")

        else:
            self.voice_b.config(text="🔊 Off")


    def enqueue(self,output):
        if not self.allow_execution:
            return
        self.allow_execution = not self.allow_execution
        while self.size is None:
            size = askstring("Queue size","Please enter queue size")
            try:
                self.size = int(size)
                break
            except:
                pass


        input = self.node.get()
        if input == "" or input == "Enter node value":
            msg.showwarning(title="No Input", message="Please enter input")
            return
        if len(self.queue_l)+1<=self.size:
            self.queue_l.append(input)

            self.explain("enqueuing {}".format(input))

            curr_rect = output.create_rectangle(self.x, self.y, self.x + 40, self.y + 40,fill='#3779D2')
            curr_text = output.create_text(self.x + 20, self.y + 20, text=input, fill="#d8d8d8")
            arrow = output.create_line(self.x+40,self.y+20,self.x+60,self.y+20,
                                          arrow=tk.LAST, capstyle=tk.BUTT, fill='black')
            output.update()
            time.sleep(0.28)
            output.itemconfig(curr_rect, fill="")

            self.queue_canvas.append([curr_rect,curr_text,arrow])


            self.x += 60


            sr = list(map(int, output.cget('scrollregion').split()))
            output['scrollregion'] = (sr[0], sr[1], sr[2] + 60, sr[3])
            output.xview_moveto((self.x + 60) / (sr[2] + 60))
            output.update()
            self.allow_execution = not self.allow_execution

        else:
            self.explain("{} cannot be inserted due to overflow".format(input))
            msg.showwarning(title="Overflow", message="Overflow!!")
            self.allow_execution = not self.allow_execution

            return

    def dequeue(self,output):
        if not self.allow_execution:
            return
        self.allow_execution = not self.allow_execution
        if len(self.queue_l)==0:
            self.explain("Underflow condition occurred")
            msg.showwarning(title="Underflow", message="Underflow!!")
            self.allow_execution = not self.allow_execution
            return

        removed = self.queue_l.pop(0)
        self.explain("dequeuing {}".format(removed))

        output.move(self.queue_canvas[0][0],0,40)
        output.move(self.queue_canvas[0][1],0,40)
        output.move(self.queue_canvas[0][2],0,40)
        output.update()
        output.itemconfig(self.queue_canvas[0][0], fill="#DC143C")
        output.update()

        time.sleep(0.09)
        output.itemconfig(self.queue_canvas[0][0], fill="#800000")
        output.update()

        time.sleep(0.1)
        output.itemconfig(self.queue_canvas[0][0], fill="#DC143C")
        output.update()

        time.sleep(0.09)
        output.update()

        output.delete(*self.queue_canvas[0])
        output.move(tk.ALL,-60,0)
        self.x -=60
        self.queue_canvas.pop(0)
        self.allow_execution = not self.allow_execution


    def peek(self,output):
        print(self.allow_execution)
        if not self.allow_execution:
            return
        self.allow_execution = not self.allow_execution
        self.explain("Top element is {}".format(self.queue_l[-1]))
        msg.showinfo(title="Top element",message="Top element is  "+self.queue_l[-1])
        self.allow_execution = not self.allow_execution



    def size_(self, output):
        if not self.allow_execution:
            return
        self.allow_execution = not self.allow_execution
        self.explain("Size of queue is {}".format(len(self.queue_l)))
        msg.showinfo(title="Top element", message="Size of queue is %d"%(len(self.queue_l)))
        self.allow_execution = not self.allow_execution




