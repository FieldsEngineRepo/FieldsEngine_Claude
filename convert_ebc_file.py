from globaldata import *
import ebcdic
import codecs
import io
# with open("EBCDIC.txt", "rb") as ebcdic:
#    ascii_txt = codecs.decode(ebcdic, "cp500")
#    print(ascii_txt)

EBCDIC_CONVERT = {
    '00': '^NUL^',
    '01': '^SOH^',
    '02': '^STX^',
    '03': '^ETX^',
    '04': '^PF^',
    '05': '^HT^',
    '06': '^LC^',
    '07': '^DEL^',
    '08': '',
    '09': '',
    '0A': '^SMM^',
    '0B': '^VT^',
    '0C': '^FF^',
    '0D': '^CR^',
    '0E': '^SO^',
    '0F': '^SI^',
    '10': '^DLE^',
    '11': '^DC1^',
    '12': '^DC2^',
    '13': '^TM^',
    '14': '^RES^',
    '15': '^NL^',
    '16': '^BS^',
    '17': '^IL^',
    '18': '^CAN^',
    '19': '^EM^',
    '1A': '^CC^',
    '1B': '^CU1^',
    '1C': '^IFS^',
    '1D': '^IGS^',
    '1E': '^IRS^',
    '1F': '^IUS^',
    '20': '^DS^',
    '21': '^SOS^',
    '22': '^FS^',
    '23': '',
    '24': '^BYP^',
    '25': '^LF^',
    '26': '^ETB^',
    '27': '^ESC^',
    '28': '',
    '29': '',
    '2A': '^SM^',
    '2B': '^CU2^',
    '2C': '^',
    '2D': '^ENQ^',
    '2E': '^ACK^',
    '2F': '^BEL^',
    '30': '',
    '31': '',
    '32': '^SYN^',
    '33': '^^',
    '34': '^PN^',
    '35': '^RS^',
    '36': '^UC^',
    '37': '^EOT^',
    '38': '',
    '39': '',
    '3A': '',
    '3B': '^CU3^',
    '3C': '^DC4^',
    '3D': '^NAK^',
    '3E': '',
    '3F': '^SUB^',
    '40': ' ',
    '41': '',
    '42': '',
    '43': '',
    '44': '',
    '45': '',
    '46': '',
    '47': '',
    '48': '',
    '49': '',
    '4A': '^CENT^',
    '4B': '.',
    '4C': '<',
    '4D': '(',
    '4E': '+',
    '4F': '|',
    '50': '&',
    '51': '',
    '52': '',
    '53': '',
    '54': '',
    '55': '',
    '56': '',
    '57': '',
    '58': '',
    '59': '',
    '5A': '!',
    '5B': '$',
    '5C': '*',
    '5D': ')',
    '5E': ';',
    '5F': '',
    '60': '-',
    '61': '/',
    '62': '',
    '63': '',
    '64': '',
    '65': '',
    '66': '',
    '67': '',
    '68': '',
    '69': '',
    '6A': '',
    '6B': ',',
    '6C': '%',
    '6D': '_',
    '6E': '>',
    '6F': '?',
    '70': '',
    '71': '',
    '72': '',
    '73': '',
    '74': '',
    '75': '',
    '76': '',
    '77': '',
    '78': '',
    '79': '',
    '7A': ':',
    '7B': '#',
    '7C': '@',
    '7D': '`',
    '7E': '=',
    '7F': '"',
    '80': '',
    '81': 'a',
    '82': 'b',
    '83': 'c',
    '84': 'd',
    '85': 'e',
    '86': 'f',
    '87': 'g',
    '88': 'h',
    '89': 'i',
    '8A': '',
    '8B': '',
    '8C': '',
    '8D': '',
    '8E': '',
    '8F': '',
    '90': '',
    '91': 'j',
    '92': 'k',
    '93': 'l',
    '94': 'm',
    '95': 'n',
    '96': 'o',
    '97': 'p',
    '98': 'q',
    '99': 'r',
    '9A': '',
    '9B': '',
    '9C': '',
    '9D': '',
    '9E': '',
    '9F': '',
    'A0': '',
    'A1': '',
    'A2': 's',
    'A3': 't',
    'A4': 'u',
    'A5': 'v',
    'A6': 'w',
    'A7': 'x',
    'A8': 'y',
    'A9': 'z',
    'AA': '',
    'AB': '',
    'AC': '',
    'AD': '[',
    'AE': '',
    'AF': '',
    'B0': '',
    'B1': '',
    'B2': '',
    'B3': '',
    'B4': '',
    'B5': '',
    'B6': '',
    'B7': '',
    'B8': '',
    'B9': '',
    'BA': '',
    'BB': '',
    'BC': '',
    'BD': ']',
    'BE': '',
    'BF': '',
    'C0': '{',
    'C1': 'A',
    'C2': 'B',
    'C3': 'C',
    'C4': 'D',
    'C5': 'E',
    'C6': 'F',
    'C7': 'G',
    'C8': 'H',
    'C9': 'I',
    'CA': '',
    'CB': '',
    'CC': '',
    'CD': '',
    'CE': '',
    'CF': '',
    'D0': '}',
    'D1': 'J',
    'D2': 'K',
    'D3': 'L',
    'D4': 'M',
    'D5': 'N',
    'D6': 'O',
    'D7': 'P',
    'D8': 'Q',
    'D9': 'R',
    'DA': '',
    'DB': '',
    'DC': '',
    'DD': '',
    'DE': '',
    'DF': '',
    'E0': '',
    'E1': '',
    'E2': 'S',
    'E3': 'T',
    'E4': 'U',
    'E5': 'V',
    'E6': 'W',
    'E7': 'X',
    'E8': 'Y',
    'E9': 'Z',
    'EA': '',
    'EB': '',
    'EC': '',
    'ED': '',
    'EE': '',
    'EF': '',
    'F0': '0',
    'F1': '1',
    'F2': '2',
    'F3': '3',
    'F4': '4',
    'F5': '5',
    'F6': '6',
    'F7': '7',
    'F8': '8',
    'F9': '9',
    'FA': '',
    'FB': '',
    'FC': '',
    'FD': '',
    'FE': '',
    'FF': ''
}
INPUT_DIR = 'D:\\GlobalData\\Data\\well_data\\tx_oil_data_hex\\'
INPUT_FILE = 'tx_oil_data_01.txt'


def convert_ebc_line(ebc_line):
    # output_line = ebc_line.decode('cp1140').encode('utf-8')
    output_line = codecs.decode(ebc_line, "cp500").encode('utf-8')
    # ebc_chars = ebc_line.split(' '.encode('hex'))
    # for ebc_char in ebc_chars:
    #    output_line += EBCDIC_CONVERT[ebc_char.upper()]
    # print output_line
    return output_line


'''
with io.open('myfile.txt', 'r', encoding="cp500") as fh:
  for line in fh:
'''

def convert_file(input_dir, input_file):
    with io.open(input_dir + input_file, 'r', encoding="cp037") as ebc_file:
        for fileline in ebc_file:
            print 0,fileline
            repr(codecs.encode(fileline, 'latin-1'))

def convert_ebc_file(input_dir, input_file):
    output_text = ''
    input_filename = input_file[:-4]
    column_hex = {col: [] for col in range(228)}
    with open(input_dir + input_file, 'r') as ebc_file:
        fileline_num = 1
        output_doc_num = 1
        while fileline_num < 10000:
            fileline = ebc_file.read(228)
            linedata = repr(codecs.encode(fileline, "hex"))[1:]
            for col in range(228):
                start_indx = col*2
                end_indx   = (col+1)*2
                hex_val = linedata[start_indx:end_indx]
                if hex_val in ['00', '0c']:
                    hex_val = 'f0'
                column_hex[col].append(hex_val)
            fileline_num += 1
    for col in range(228):
        print 'col {}: {}'.format(col, column_hex[col])


def convert_ebc_text(text_str):
    output_text = ''
    text_str = text_str.upper()
    for i in range(len(text_str)):
        if i % 2 == 0:
            ebc_char = text_str[i:i + 2]
            try:
                output_text += EBCDIC_CONVERT[ebc_char]
            except:
                pass
    print output_text


if __name__ == '__main__':
    convert_ebc_file(INPUT_DIR, INPUT_FILE)
    # convert_ebc_text(test_str)
