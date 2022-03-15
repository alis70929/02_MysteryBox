from tkinter import *
from functools import partial
import random


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
        root.withdraw()
        Game(self, stakes, self.starting_funds.get())
        

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        self.balance = IntVar()

        self.balance.set(starting_balance)

        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        self.game_box = Toplevel()

        self.game_box.protocol('WM_DELETE_WINDOW', self.close_game)
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        self.heading_label = Label(self.game_frame, text="Play",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        box_txt = "Arial 16 bold"
        box_back = "#b9ea96"
        box_width = 5

        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)

        self.prize1_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize2_label.grid(row=0, column=1)

        self.prize3_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize3_label.grid(row=0, column=2)

        self.play_button = Button(self.game_frame, text="Open Boxes", bg="#FFFF33", font="Arial 15 bold",
                                  padx=10, pady=10, width=20, command=self.reveal_boxes)
        self.play_button.grid(row=3)

        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())

        start_text = "Game Cost: ${} \n""\n How Much will you win ".format(stakes * 5)

        self.balance_label = Label(self.game_frame, wrap=250, text="Game Cost :${}\nBalance: ${}".format(5 * self.multiplier.get(), starting_balance))
        self.balance_label.grid(row=4)

        self.help_export_frame = Frame(self.game_frame, pady=10)
        self.help_export_frame.grid(row=5)

        self.help_button = Button(self.help_export_frame, text="Instructions", bg="#FFFF33", font="Arial 12 bold")
        self.help_button.grid(row=0, column=0, padx=2)

        self.export_button = Button(self.help_export_frame, text="Export/Stats", bg="#FFFF33", font="Arial 12 bold")
                                    
        self.export_button.grid(row=0, column=1, padx=2)

        self.quit_button = Button(self.game_frame, text="Quit", bg="#FFFF33", font="Arial 15 bold",
                                  padx=10, pady=10, command=self.close_game)
        self.quit_button.grid(row=6)

    def reveal_boxes(self):
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winning = 0
        prize_list = []
        backgrounds = []
        for thing in range(0, 3):

            prize_num = random.randint(1, 100)

            if 0 < prize_num <= 5:
                prize = "Gold\n (${})".format(5 * stakes_multiplier)
                back_colour = "#CEA935"
                round_winning += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver\n (${})".format(2 * stakes_multiplier)
                back_colour = "#B7B7B5"
                round_winning += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = "Copper\n (${})".format(1 * stakes_multiplier)
                back_colour = "#BC7f61"
                round_winning += 1 * stakes_multiplier
            else:
                back_colour = "#595E71"
                prize = "Lead\n ($0)"

            prize_list.append(prize)
            backgrounds.append(back_colour)

        self.prize1_label.config(text=prize_list[0], bg=backgrounds[0])
        self.prize2_label.config(text=prize_list[1], bg=backgrounds[1])
        self.prize3_label.config(text=prize_list[2], bg=backgrounds[2])

        current_balance -= 5 * stakes_multiplier

        current_balance += round_winning

        self.balance.set(current_balance)
        balance_statement = "Game Cost: ${}\nPayback: ${}\nCurrent balance: ${}".format(5 * stakes_multiplier,
                                                                                        round_winning,
                                                                                        current_balance)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\n"\
                                "You balance is too low."\
                                " You can only quit or view your stats".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold")

        self.balance_label.configure(text=balance_statement)

    def close_game(self):
        root.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Boxes")
    something = Start(root)
    root.mainloop()
