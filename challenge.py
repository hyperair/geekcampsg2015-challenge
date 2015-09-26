#!/usr/bin/env python3

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

    s.close()

if __name__ == '__main__':
    main()
