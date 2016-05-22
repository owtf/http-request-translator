class NoRequestProvided(Exception):
    def __init__(self):
        message = "Input a valid raw request and try again.\nOr use Interactive mode instead"
        super(NoRequestProvided, self).__init__(message)
