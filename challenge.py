#!/usr/bin/env python3

import re
import socket
import sys

def test(f, s):
    print(s)
    f.write(s + '\n')
    f.flush()

    return f.readline().strip()

def guess_char(f, prefix):
    begin = ord('a') - 1
    end = ord('z') + 1
    found = False

    def handle_lt():
        nonlocal begin
        begin = current

    def handle_gt():
        nonlocal end
        end = current

    def handle_eq():
        nonlocal found
        found = True

    lookup = {'<': handle_lt,
              '>': handle_gt,
              '=': handle_eq}

    while end - begin > 1 and not found:
        current = int((begin + end) / 2)
        result = test(f, prefix + chr(current))

        lookup[result]()

    return (prefix + chr(begin), found)

def main():
    whitelist_pattern = re.compile(r'^[a-zA-Z]+$')
    dictionary = [
        w for w in
        (l.strip() for l in open("/usr/share/dict/words").readlines())
        if whitelist_pattern.match(w)
    ]
    threshold = 4

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('challenge.geekcamp.sg', 5000))
    f = s.makefile('rw')

    # swallow the first line which asks for twitter username
    f.readline()
    f.write('{username}\n'.format(username=sys.argv[1]))
    f.flush()

    # start guessing
    f.readline()

    found = False
    prefix = ''
    while not found:
        prefix, found = guess_char(f, prefix)

        if not found:
            matched_words = [w for w in dictionary if w.startswith(prefix)]
            if len(matched_words) <= threshold:
                print(matched_words)

                for word in matched_words:
                    found = (test(f, word) == '=')

                    if found:
                        break

    s.close()

if __name__ == '__main__':
    main()
