import sys


try:
    input = raw_input  # Python2/3 version
except NameError:
    pass


def callback_interactive():
    raw_request = []
    print("Enter raw request (press ^D to finish or ^C to quit)")
    while True:
        try:
            raw_request.append(input().strip())
        except (EOFError, KeyboardInterrupt):
            break
    return '\n'.join(raw_request).strip()


def callback_file(filepath):
    raw_request = ''
    try:
        raw_request = open(filepath).read()
    except (OSError, IOError) as e:
        sys.stderr.write("error: Failed to open '%s'\n\n" % filepath)
        raise e
    return raw_request


def callback_inline(raw_request):
    return raw_request


def callback_stdin():
    raw_request = ''
    while True:
        try:
            raw_request += input() + '\n'
        except EOFError:
            break
    return raw_request[:-1]


handlers = {
    'interactive': callback_interactive,
    'file': callback_file,
    'inline': callback_inline,
    'stdin': callback_stdin
}
