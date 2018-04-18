#!/usr/bin/env python
# Author: Matt (Syph0n) Schmidt

# Description:
# This script decodes the F5 BigIP persistence cookie from its encoded form to is decimal representation
# F5 Persistance Cookie Info: http://support.f5.com/kb/en-us/solutions/public/6000/900/sol6917.html
# Mitigation Steps: http://support.f5.com/kb/en-us/solutions/public/7000/700/sol7784.html

# This project was inspired by:
# http://www.taddong.com/tools/BIG-IP_cookie_decoder.zip
# https://support.f5.com/csp/article/K6917


import struct
import sys
import click
from terminaltables import AsciiTable


if __name__ == '__main__':
    # Build Help Menu
    if len(sys.argv) != 2:
        click.secho(
            '\n-------- F5 BIG-IP Persistence Cookie Decoder -------', fg='green')
        click.echo('Author: Matt Schmidt\n')
	click.echo('Usage: %s persistence.cookie.value\n' % sys.argv[0])
        click.echo('Example: %s 1677787402.36895.0000\n' % sys.argv[0])
        sys.exit(1)

    # Define persistence cookie
    cookie = sys.argv[1]
    (host, port, padding) = cookie.split('.')

    # Convert Host to Hexadecimal
    (hex1, hex2, hex3, hex4) = [ord(i) for i in struct.pack('<I', int(host))]

    # Convert Port to Hexadecimal
    (v) = [ord(j) for j in struct.pack('<H', int(port))]
    p = '0x%02X%02X' % (v[0], v[1])

    # Print Terminal Table Output of Hex and Decimal Format
    click.secho(
        '\n-------- F5 BIG-IP Persistence Cookie Decoder --------\n', fg='green')
    click.secho('[*] Cookie to Decode: %s \n' % cookie, fg='green')
    table_data = [
        ['Type', 'Encoded Format', 'Hexadecimal', 'Decimal'],
        ['IP Address', '%s' % host,'0x%02X 0x%02X 0x%02X 0x%02X' %
            (hex1, hex2, hex3, hex4), '%s.%s.%s.%s' % (hex1, hex2, hex3, hex4)],
        ['Port', '%s' % port, '%s' % p, '%s' % (int(p, 16))],
    ]
    table = AsciiTable(table_data)
    table.title = 'Decoded Cookie Info'
    click.echo(table.table)
