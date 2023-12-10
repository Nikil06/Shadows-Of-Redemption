class ConsoleSizeError(Exception):
    def __init__(self, current_size, buffer_size):
        self.current_size = current_size
        self.buffer_size = buffer_size

        self.error_message  = "\n\n[!] Console Size Error :-\n"
        self.error_message += "\tThe current size of the console is too small to display the buffer.\n"
        self.error_message += f"\tWindow size : {current_size}\n"
        self.error_message += f"\tBuffer size : {buffer_size}"

        super().__init__(self.error_message)
