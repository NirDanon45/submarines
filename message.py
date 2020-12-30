MAGIC = 'bs1p'
TYPES = [0, 1, 2, 3, 4, 5, 6]


class Message:
    def encode_message(self):
        """
        this is a message encoding method each message class has to implement.
        :return: a message in byte format to be sent.
        """
        pass


class GameRequest:
    def __init__(self):
        self.type = TYPES[0]
        self.magic = MAGIC

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        return magic_bytes + type_bytes


class GameReply:
    def __init__(self, response):
        self.type = TYPES[1]
        self.magic = MAGIC
        self.response = response

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        response_int = int(self.response)
        response_bytes = response_int.to_bytes(1, byteorder='big')
        return magic_bytes + type_bytes + response_bytes


class Order:
    def __init__(self):
        self.type = TYPES[2]
        self.magic = MAGIC

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        return magic_bytes + type_bytes


class Guess:
    def __init__(self, row_index, column_index):
        self.type = TYPES[3]
        self.magic = MAGIC
        self.row_index = row_index
        self.column_index = column_index

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        row_index_integer = int(self.row_index)
        row_index_bytes = row_index_integer.to_bytes(4, byteorder='big')
        column_index_integer = int(self.column_index)
        column_index_bytes = column_index_integer.to_bytes(4, byteorder='big')
        return magic_bytes + type_bytes + row_index_bytes + column_index_bytes


class Result:
    def __init__(self, msg_type, sub_length=0):
        self.type = TYPES[4]
        self.magic = MAGIC
        self.result_code = msg_type
        self.sub_length = sub_length

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        sub_length_int = int(self.sub_length)
        sub_length_bytes = sub_length_int.to_bytes(1, byteorder='big')
        msg_type_int = int(self.result_code)
        msg_type_bytes = msg_type_int.to_bytes(1, byteorder='big')
        if self.result_code == 0:
            return magic_bytes + type_bytes + msg_type_bytes
        else:
            return magic_bytes + type_bytes + msg_type_bytes + sub_length_bytes


class Acknowledge:
    def __init__(self, result_code):
        self.type = TYPES[5]
        self.magic = MAGIC
        self.result_code = result_code
        result_code_int = int(result_code)
        self.result_code = result_code_int.to_bytes(1, byteorder='big')

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        result_code_int = int(self.result_code)
        result_code_bytes = result_code_int.to_bytes(1, byteorder='big')

        return magic_bytes + type_bytes + result_code_bytes


class Error:
    def __init__(self, error_code):
        self.type = TYPES[6]
        self.magic = MAGIC
        self.error_code = error_code

    def encode_message(self):
        type_bytes = bytes(self.type)
        magic_bytes = bytes(self.magic, 'ascii')
        error_code_int = int(self.error_code)
        error_code_bytes = error_code_int.to_bytes(1, byteorder='big')
        return magic_bytes + type_bytes + error_code_bytes

