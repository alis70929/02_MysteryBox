import re
from tkinter import *
from functools import partial
import random

from numpy import pad


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

        self.help_button = Button(self.start_frame, text="help/Rules", command=self.help)
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
    def help(self):
        get_help = Help(self)
        

class Game:

    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        self.balance = IntVar()

        self.balance.set(starting_balance)

        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        self.round_stats_list = []
        self.game_stats_lists = [starting_balance, starting_balance]

        self.game_box = Toplevel()

        self.game_box.protocol('WM_DELETE_WINDOW', self.close_game)
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        self.heading_label = Label(self.game_frame, text="Play",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        box_txt = "Arial 16 bold"
        box_back = "#b9ea96"
        box_width = 6
        box_height = 3

        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)

        self.prize1_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, height=box_height, wraplength= 80)
        self.prize1_label.grid(row=0, column=0, padx=10)

        self.prize2_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, height=box_height, wraplength= 80)
        self.prize2_label.grid(row=0, column=1, padx=10)

        self.prize3_label = Label(self.box_frame, text="?\n", font=box_txt,
                                  bg=box_back, width=box_width, height=box_height, wraplength= 80)
        self.prize3_label.grid(row=0, column=2,  padx=10)

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

        self.help_button = Button(self.help_export_frame, text="Instructions", bg="#FFFF33",
                                  font="Arial 12 bold", command=self.help)
        self.help_button.grid(row=0, column=0, padx=2)

        self.export_button = Button(self.help_export_frame, text="Export/Stats", bg="#FFFF33",
                                    font="Arial 12 bold", command=lambda: self.to_stats(self.round_stats_list, self.game_stats_lists))
                                    
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
                prize = "Gold (${})".format(5 * stakes_multiplier)
                back_colour = "#CEA935"
                round_winning += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver (${})".format(2 * stakes_multiplier)
                back_colour = "#B7B7B5"
                round_winning += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = "Copper (${})".format(1 * stakes_multiplier)
                back_colour = "#BC7f61"
                round_winning += 1 * stakes_multiplier
            else:
                back_colour = "#595E71"
                prize = "Lead ($0)"

            prize_list.append(prize)
            backgrounds.append(back_colour)

        self.prize1_label.config(text=prize_list[0], bg=backgrounds[0])
        self.prize2_label.config(text=prize_list[1], bg=backgrounds[1])
        self.prize3_label.config(text=prize_list[2], bg=backgrounds[2])

        current_balance -= 5 * stakes_multiplier

        current_balance += round_winning

        self.balance.set(current_balance)
        
        self.game_stats_lists[1] = current_balance
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

        round_summary = "{} | {} | {} - Cost: ${} | Payback: ${} | " \
                        "Current Balance: ${}".format(prize_list[0], prize_list[1], prize_list[2],
                                                      5 * stakes_multiplier, round_winning, current_balance)
        self.round_stats_list.append(round_summary)

                        

    def close_game(self):
        root.destroy()
    def help(self):
        get_help = Help(self)
    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)
    
class GameStats():
    def __init__(self, partner, game_history, game_stats):

        partner.export_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        self.stats_box = Toplevel()

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame= Frame(self.stats_box)
        self.stats_frame.grid()
        
        self.stats_heading_label = Label(self.stats_frame, text="Game Statisitics",
                                         font="Arial 19 bold")
        self.stats_heading_label.grid(row=0)

        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=1)

        self.start_balance_label = Label(self.details_frame, text="Starting Balance:", font=heading,
                                         anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content, 
                                               text="${}".format(game_stats[0]))
        self.start_balance_value_label.grid(row=0,column=1,padx=0)

        self.current_balance_label = Label(self.details_frame, text="Current Balance:", font=heading,
                                           anchor="e")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label =  Label(self.details_frame, font=content, 
                                                  text="${}".format(game_stats[1]))
        self.current_balance_value_label.grid(row=1,column=1,padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"
        
        self.win_loss_label = Label(self.details_frame, text=win_loss, font=heading, anchor="e")
        self.win_loss_label.grid(row=2, column=0, padx=0)

        self.win_loss_value_label = Label(self.details_frame, font=content, text="${}".format(amount),
                                          fg=win_loss_fg, anchor="w")
        self.win_loss_value_label.grid(row=2, column=1, padx=0)
        
        self.games_played_label = Label(self.details_frame, text="Rounds Played:", font=heading,
                                        anchor="w")
        self.games_played_label.grid(row=4, column=0,padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content, text=len(game_history),
                                              anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

        self.export_button = Button(self.stats_frame, text="Export To File", bg="#FFFF33",
                                    font="Arial 12 bold", command=lambda: self.to_export(game_history, game_stats))
                                    
        self.export_button.grid(row=2, padx=2)

    def close_stats(self,partner):
        partner.export_button.config(state=NORMAL)
        self.stats_box.destroy()
    
    def to_export(self, game_history, game_stats):
        GameExport(self, game_history, game_stats)


class GameExport():
    def __init__(self, partner, game_history, game_stats):
        partner.export_button.config(state=DISABLED)
        background = "medium purple"

        # dsiable help button
        partner.export_button.config(state=DISABLED)

        self.export_box = Toplevel()

        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        self.export_frame = Frame(self.export_box, bg=background)
        self.export_frame.grid()

        # Heading
        self.export_heading = Label(self.export_frame, text="export / instructions",
                                    font="arial 10 bold", bg=background)
        self.export_heading.grid(row=0)
        # Text
        self.export_text = Label(self.export_frame, text="Enter a filename below "
                                                         "and press save to save your history "
                                                         "to a text file",
                                 justify=LEFT, width=40, bg=background, wrap=250)
        self.export_text.grid(row=1)

        self.filename_entry = Entry(self.export_frame, width=20,
                                    font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        self.save_error_label = Label(self.export_frame, text="", fg="maroon",
                                      bg=background)
        self.save_error_label.grid(row=4)

        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        self.save_button = Button(self.save_cancel_frame, text="Save",
                                  width=10, bg=background, font="arial 10 bold",
                                  command=partial(lambda: self.save_history(partner, game_history, game_stats)))
        self.save_button.grid(row=0, column=0)

        # Cancel Button
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel",
                                    width=10, bg=background, font="arial 10 bold",
                                    command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

    def close_export(self, partner):
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()

    def save_history(self, partner, game_history, game_stats):

        has_error = "no"
        filename = self.filename_entry.get()

        valid_char = "[A-za-z0-9_]"
        for letter in filename:
            if re.match(valid_char, filename):
                continue

            elif letter == " ":
                problem = "no spaces allowed"
            else:
                problem = "no {}'s allowed".format(letter)
            has_error = "yes"
        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            self.filename_entry.config(bg="#ffafaf")
        else:
            filename = filename + ".txt"

            f = open(filename, "w+")

            f.write("\nGame Statistics\n\n")
            f.write("Balance Started: {} \n".format(game_stats[0]))
            f.write("End Balance: {} \n".format(game_stats[1]))
            if game_stats[1] > game_stats[0]:
                win_loss = "Amount Won:"
                amount = game_stats[1] - game_stats[0]
                win_loss_fg = "green"
            else:
                win_loss = "Amount Lost:"
                amount = game_stats[0] - game_stats[1]
                win_loss_fg = "#660000"
            f.write("{} : {} \n".format(win_loss,amount))
            f.write("Rounds Played: {} \n".format(len(game_stats)))

            f.write("\n Round Details \n\n")

            for item in game_history:
                f.write(item + "\n\n")
            f.close()

            self.close_export(partner)



        
class Help:
    def __init__(self, partner):
        background = "medium purple"

        # dsiable help button
        partner.help_button.config(state=DISABLED)

        self.help_box = Toplevel()

        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        # Heading
        self.help_heading = Label(self.help_frame, text="help / instructions",
                                  font="arial 10 bold", bg=background)
        self.help_heading.grid(row=0)
        # Text
        self.help_text = Label(self.help_frame, text="example text",
                               justify=LEFT, width=40, bg=background, wrap=250)
        self.help_text.grid(row=1)

        # DismissButton
        self.help_dismiss = Button(self.help_frame, text="dismiss",
                                   width=10, bg=background, font="arial 10 bold",
                                   command=partial(self.close_help, partner))
        self.help_dismiss.grid(row=2, pady=10)

    def close_help(self, partner):
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Boxes")
    something = Start(root)
    root.mainloop()
