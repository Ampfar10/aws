import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
player = "X"
game_on = False

def start(bot, update):
    global game_on
    game_on = True
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to Tic-Tac-Toe! You are player X. To make a move, send the number of the cell where you want to place your marker. The cells are numbered from left to right, top to bottom.")
    display_board(bot, update)

def display_board(bot, update):
    global board
    message = "```\n" + board[0] + " | " + board[1] + " | " + board[2] + "\n---------\n" + \
              board[3] + " | " + board[4] + " | " + board[5] + "\n---------\n" + \
              board[6] + " | " + board[7] + " | " + board[8] + "\n```"
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

def check_win(player):
    global board
    # Check rows
    if board[0] == player and board[1] == player and board[2] == player:
        return True
    if board[3] == player and board[4] == player and board[5] == player:
        return True
    if board[6] == player and board[7] == player and board[8] == player:
        return True
    # Check columns
    if board[0] == player and board[3] == player and board[6] == player:
        return True
    if board[1] == player and board[4] == player and board[7] == player:
        return True
    if board[2] == player and board[5] == player and board[8] == player:
        return True
    # Check diagonals
    if board[0] == player and board[4] == player and board[8] == player:
        return True
    if board[2] == player and board[4] == player and board[6] == player:
        return True
    return False

def make_move(bot, update, cell):
    global board, player, game_on
    if game_on and board[cell] == " ":
        board[cell] = player
        if check_win(player):
            bot.send_message(chat_id=update.message.chat_id, text="Player " + player + " wins!")
            game_on = False
        else:
            if player == "X":
                player = "O"
            else:
                player = "X"
            display_board(bot, update)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Invalid move or game is not currently running. Send /start to begin a new game.")

def move(bot, update):
    try:
        cell = int(update.message.text) - 1
        if cell < 0 or cell > 8:
            raise ValueError
        make_move(bot, update, cell)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text="Invalid move. Please enter a number between 1 and 9.")

# Create the Updater and pass it the bot's token
updater = Updater(token="5433855776:AAH5RAL6rrKla3hxygyYhjAwSjVmudbDNUw")

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Add a handler for the "start" command
dp.add_handler(CommandHandler("start", start))

# Add a handler for text messages
dp.add_handler(MessageHandler(Filters.text, move))

# Start the bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
