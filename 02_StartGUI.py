from tkinter import *
from tracemalloc import start


class Start:
    def __init__(self, parent):
        
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game")
        self.mystery_box_label.grid(row=1)

        self.start_amount_entry = Entry(self.start_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=2)

        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=3, pady=10)

        self.lowstakes_button = Button(self.stakes_frame, text="Low(5$)", command=lambda: self.to_game(1))
        self.lowstakes_button.grid(row=0, column=0)

        self.mediumstakes_button = Button(self.stakes_frame, text="medium(10$)", command=lambda: self.to_game(2))
        self.mediumstakes_button.grid(row=0, column=1)

        self.highstakes_button = Button(self.stakes_frame, text="high(15$)", command=lambda: self.to_game(3))
        self.highstakes_button.grid(row=0, column=2)

        self.help_button = Button(self.start_frame, text="help/Rules")
        self.help_button.grid(row=4, pady=10)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()
        Game(self, stakes, starting_balance)


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        self.balance = IntVar()

        self.balance.set(starting_balance)

        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        self.heading_label = Label(self.game_frame, text="Heading",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.balance_label = Label(self.game_frame, text="Balance...")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain", padx=10,
                                  pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        current_balance = self.balance.get()
        current_balance += 2

        self.balance.set(current_balance)

        self.balance_label.configure(text="Balance: {}".format(current_balance))


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Boxes")
    something = Start(root)
    root.mainloop()