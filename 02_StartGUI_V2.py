from tkinter import *
from functools import partial


class Start:
    def __init__(self, parent):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.starting_funds = IntVar()

        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game")
        self.mystery_box_label.grid(row=1)

        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 19 bold", width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame, font="Arial 14 bold", text="Add Funds",
                                       command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, font="Arial 10 bold", fg="#ffafaf",
                                        wrap=275, justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=4, pady=10)

        button_font = "Arial 12 bold"

        self.lowstakes_button = Button(self.stakes_frame, text="Low(5$)", command=lambda: self.to_game(1),
                                       font=button_font, bg="#FF9933")
        self.lowstakes_button.grid(row=0, column=0)

        self.mediumstakes_button = Button(self.stakes_frame, text="medium(10$)",
                                          command=lambda: self.to_game(2), font=button_font, bg="#FFFF33")
        self.mediumstakes_button.grid(row=0, column=1)

        self.highstakes_button = Button(self.stakes_frame, text="high(15$)", command=lambda: self.to_game(3),
                                        font=button_font, bg="#99FF33")
        self.highstakes_button.grid(row=0, column=2, pady=10)

        self.lowstakes_button.config(state=DISABLED)
        self.mediumstakes_button.config(state=DISABLED)
        self.highstakes_button.config(state=DISABLED)

        self.help_button = Button(self.start_frame, text="help/Rules")
        self.help_button.grid(row=5, pady=10)

    def check_funds(self):

        starting_balance = self.start_amount_entry.get()

        error_back = "#ffafaf"
        has_errors = "no"

        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        self.lowstakes_button.config(state=DISABLED)
        self.mediumstakes_button.config(state=DISABLED)
        self.highstakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)
            print(starting_balance)
            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Too Low! The least you can pllay with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too High! Max you can play with is $50"
            elif starting_balance >= 15:
                self.lowstakes_button.config(state=NORMAL)
                self.mediumstakes_button.config(state=NORMAL)
                self.highstakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                self.lowstakes_button.config(state=NORMAL)
                self.mediumstakes_button.config(state=NORMAL)
            else:
                self.lowstakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (No text, symbols or decimals)"
        
        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)
        else:
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()

        error_back = "#ffafaf"
        has_errors = "no"

        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Too Low! The least you can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too High! Max you can play with is $50"
            elif starting_balance < 10 and (stakes == 2 or stakes == 3):
                has_errors = "yes"
                error_feedback = "Sorry you can only afford to play a low stakes game"
            elif starting_balance < 15 and stakes == 3:
                has_errors = "yes"
                error_feedback = " Sorry you can only afford to play a low or medium stakes game"
        
        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (No text, symbols or decimals)"
        
        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)
        else:
            Game(self, stakes, starting_balance)
            root.withdraw()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        self.balance = IntVar()

        self.balance.set(starting_balance)

        self.game_box = Toplevel()

        self.game_box.protocol('WM_DELETE_WINDOW', partial(self.close_game, partner))
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        self.heading_label = Label(self.game_frame, text="Heading",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.balance_label = Label(self.game_frame, text="Balance: {}".format(self.balance.get()))
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain", padx=10,
                                  pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        current_balance = self.balance.get()
        current_balance += 2

        self.balance.set(current_balance)

        self.balance_label.configure(text="Balance: {}".format(current_balance))
    
    def close_game(self, partner):
        partner.check_funds()
        self.game_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Boxes")
    something = Start(root)
    root.mainloop()