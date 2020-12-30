import exceptions
import board
import submarine
import user_input
import message
import network

NUMBER_OF_ROWS = 10
NUMBER_OF_COLUMNS = 10


class Player:
    def __init__(self, network_output, init_board=[]):
        self.board = board.Board(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, init_board)
        self.network_output = network_output
        self.operate_based_on_response_type = {0: self.game_request_response,
                                               1: self.game_reply_response,
                                               2: self.order_response,
                                               3: self.guess_response,
                                               4: self.result_response,
                                               5: self.acknowledge_response,
                                               6: self.error_response}
        self.is_first = False

    def initiate_game(self):
        """
        this is a  function to be called only if the player decided to be the one initiating the game.
        this function handles the request for battle and the first turn.
        """
        self.is_first = True

    def play_turn(self):
        opponent_message = self.network_output.receive_message()
        self.operate_based_on_response_type[opponent_message.type](opponent_message)

    def game_request_response(self, opponent_message):
        is_player_ready = input("wanna play? (y/n)")
        if is_player_ready == 'n':
            response = 0
        elif is_player_ready == 'y':
            response = 1
        else:
            raise exceptions.WrongInputException
        self.network_output.send_message(message.GameReply(response))

    def game_reply_response(self, opponent_message: message.GameReply):
        if opponent_message.response == 0:
            print("opponent don't want to play")
        if opponent_message.response == 1:
            self.board = user_input.get_guess_from_user()
            self.network_output.send_message(message.Order())

    def order_response(self, opponent_message: message.Order):
        if self.is_first:
            guessed_coordinates = user_input.get_guess_from_user()
            self.network_output.send_message(message.Guess(guessed_coordinates[0], guessed_coordinates[1]))
        else:
            return

    def guess_response(self, opponent_message: message.Guess):
        opponent_guess_coordinates = opponent_message.row_index, opponent_message.column_index
        print(f"opponent hit on {opponent_guess_coordinates}")
        if self.board.is_submarine_there(opponent_message.row_index, opponent_message.column_index):  # hit
            sinking_submarine = self.board.sink_submarine(opponent_guess_coordinates)
            print(f"You lost a ship of size {sinking_submarine.get_ship_size()}.")
            if len(self.board.submarines) > 0:  # didn't lose
                self.network_output.send_message(message.Result(2, sinking_submarine.get_ship_size()))
            else:  # lost - all ships sank
                self.network_output.send_message(message.Result(3, sinking_submarine.get_ship_size()))
                print("You lost")
                raise SystemExit
        else:  # miss
            self.network_output.send_message(message.Result(0))

    def result_response(self, opponent_message: message.Result):
        result_code = opponent_message.result_code
        if result_code == 0:
            print("you missed")
            self.network_output.send_message(message.Acknowledge(0))
        if result_code == 1:    # actually have no idea what this is.
            print(f"You have uncovered a submarine. its length is {opponent_message.sub_length}")
        if result_code == 2:
            print(f"You have drowned a submarine, its length is {opponent_message.sub_length}")
            guessed_coordinates = user_input.get_guess_from_user()
            self.network_output.send_message(message.Guess(guessed_coordinates[0], guessed_coordinates[1]))
        if result_code == 3:
            print(f"You have drowned a submarine. its length is {opponent_message.sub_length}")
            print("You won!")

    def acknowledge_response(self, opponent_message: message.Acknowledge):
        if opponent_message.result_code == 0:   # this is the only result that sends an ack
            return
        else:
            self.network_output.send_message(message.Error(0))

    def error_response(self, opponent_message):
        print("an error occurred.")
        self.network_output.send_message(message.Error(0))
        raise SystemError

