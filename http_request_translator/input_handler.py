import os
import sys


try:
    input = raw_input  # Python2/3 version
except NameError:
    pass


class Input(object):
    def __init__(self, raw_request=""):
        self.raw_request = raw_request

    def take_input(self):
        raise NotImplementedError

    def get_request(self):
        return self.raw_request


class InteractiveInput(Input):
    __type__ = 'interactive'

    def __init__(self, *args, **kwargs):
        super(InteractiveInput, self).__init__(*args, **kwargs)

    def take_input(self):
        raw_request = []
        print("Enter raw request - ")
        while True:
            try:
                raw_request.append(input().strip())
            except (EOFError, KeyboardInterrupt):
                break
        self.raw_request = '\n'.join(raw_request).strip()


class FileInput(Input):
    __type__ = 'file'

    def __init__(self, *args, **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)

    def take_input(self, filepath):
        try:
            self.raw_request = open(filepath).read()
        except (OSError, IOError) as e:
            sys.stderr.write("error: Failed to open '%s'\n\n" % filepath)
            raise e


class InlineInput(Input):
    __type__ = 'inline'

    def __init__(self, *args, **kwargs):
        super(InlineInput, self).__init__(*args, **kwargs)

    def take_input(self, raw_request):
        if not raw_request:
            raise Exception("No raw request provided.")
        self.raw_request = raw_request


class StdinInput(Input):
    __type__ = 'stdin'

    def __init__(self, *args, **kwargs):
        super(StdinInput, self).__init__(*args, **kwargs)

    def take_input(self):
        while True:
            try:
                self.raw_request += input()+'\n'
            except EOFError:
                break

        self.raw_request = self.raw_request[:-1]
