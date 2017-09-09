import os
import sys
import re
import codecs

end_of_date = r'(?=\s|\.\s|\.$|\.+|\!+|\?+|(\.+\!*\?*)+|(\.*\?+\!*)+|(\.*\?*\!+)+)' # => [\.\?\!]+
end_of_abrv = r'(?=\s|\.\s|\.$|\.+|\!+|\?+|(\.+\!*\?*)+|(\.*\?+\!*)+|(\.*\?*\!+)+)'
end_of_number = r'(?=\s|$|\?+|\!+|(\?*\!+)+|(\?+\!*)+)'
end_of_email = r'(?=\s|$|\?+|\!+|(\?*\!+)+|(\?+\!*)+)'

def parseAuthor(content):
    pattern = r'<META NAME="AUTOR" CONTENT="(.+?)">'
    prog = re.compile(pattern,re.UNICODE | re.DOTALL)
    parsed_author = prog.search(content).group(1)
    print "autor:", parsed_author


def parseDepartament(content):
    pattern = r'<META NAME="DZIAL" CONTENT="(.+?)">'
    prog = re.compile(pattern,re.UNICODE)
    parsed_departament = prog.search(content).group(1)
    print "dzial:", parsed_departament

def parseKeyWords(content):
    pattern = r'<META NAME="KLUCZOWE_\d+" CONTENT="(.+?)">'
    prog = re.compile(pattern,re.UNICODE)
    parsed_keyWords = prog.findall(content)
    print "slowa kluczowe:", 
    for keyWord in parsed_keyWords:
        print keyWord + ";",
    print
    
unique_dates = {}
unique_mailes = {}
unique_floats = {}
unique_integers = {}
unique_abrvs = {}

def countUniqueFloats(floats_list):
    for real in floats_list:
        if not unique_floats.has_key(float(real)):
            unique_floats[float(real)] = []
        unique_floats[float(real)] += [real]

def countUniqueIntegers(integers_list):
    for integer in integers_list:
        if not unique_integers.has_key(int(integer)):
            unique_integers[int(integer)] = []
        unique_integers[int(integer)] += [integer]

def countUniqueMailes(mail_list):
    for mail in mail_list:
        unique_mailes[mail] = True

def countUniqueAbrvs(abrvs_list):
    for abrv in abrvs_list:
        unique_abrvs[abrv] = True

def countUniqueDates(list_of_dates):
    for date in list_of_dates:
        date = re.sub(r' ',r'', date)
        key = re.search(r'(\d\d\d\d)(?:-|/|\.)(\d\d)(?:-|/|\.)(\d\d)',date)
        if key: key = re.sub(r'(\d\d\d\d)(?:-|/|\.)(\d\d)(?:-|/|\.)(\d\d)',r'\2.\3.\1',date)
        else: 
            delimiter = re.search(r'\d\d(.)', date).group(1)
            key = re.sub( "\\" + delimiter, r'.', date)
        if not unique_dates.has_key(key): unique_dates[key] = []
        unique_dates[key] += [date]

def findFloats(text):
    m = [x[0] for x in re.findall(r'((?<=\s)([-]?(?P<before_dot>[1-9]\d*)?(?(before_dot)\.\d*|\.\d+)((e|E)(\+|-)?\d+)?)'+end_of_number+')', text)]
    countUniqueFloats(m)
    print("liczba liczb zmiennoprzecinkowych:"), unique_floats.keys().__len__()


def findIntegers(text):
    m = [x[1] for x in re.findall(r'((?<=\s)(?P<integer>[-]?([0-9]|[1-9][0-9]|'+\
    '[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-2][0-9][0-9][0-9][0-9]'+\
    '|3[0-1][0-9][0-9][0-9]|32[0-6][0-9][0-9]|327[0-5][0-9]|3276[0-7]|-32768))'+end_of_number+')', text)]
    countUniqueIntegers(m)
    print("liczba liczb calkowitych z zakresu int:"), unique_integers.keys().__len__()


def dd_mm_rrrr(b):
    m =  [x[0] for x in re.findall(r'((?<=\s)0[1-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d' + end_of_date +\
    '|(?<=\s)0[1-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #01-09.01-12.rrrr
    m += [x[0] for x in re.findall(r'((?<=\s)[1-2][0-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d' + end_of_date +\
    '|(?<=\s)[1-2][0-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #10-19.01-12.rrrr
    m += [x[0] for x in re.findall(r'((?<=\s)30(?P<delimiter>[\./-])(?!02|1[3-9]|00|[2-9][0-9])\d\d(?P=delimiter)\d\d\d\d' + end_of_date +\
    '|(?<=\s)31(?P<delimiter1>[\./-])(?=(?:01|03|05|07|08|10|12))\d\d(?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #30-31.01-12.rrrr
    countUniqueDates(m)

def rrrr_dd_mm(b):
    m =  [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])0[1-9](?P=delimiter)[0][1-9]'+end_of_date+\
    '|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])0[1-9](?P=delimiter1)[1][0-2]'+end_of_date+')',b)] #rrrr.01-09.01-12
    m += [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])[1-2][0-9](?P=delimiter)[0][1-9]'+end_of_date+\
    '|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])[1-2][0-9](?P=delimiter1)[1][0-2]'+end_of_date+')',b)] #rrrr.10-19.01-12
    m += [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])30(?P=delimiter)(?!02|1[3-9]|00|[2-9][0-9])\d\d'+end_of_date+\
    '|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])31(?P=delimiter1)(?=01|03|05|07|08|10|12)\d\d'+end_of_date+')',b)] #rrrr.30-31.01-12
    countUniqueDates(m)

def findDates(body):
    dd_mm_rrrr(body)
    rrrr_dd_mm(body)
    print("liczba dat:"), unique_dates.keys().__len__()

def findMailes(body):
    m = [x[0] for x in re.findall(r'((?<=\s)\w+(\.(\w+))*@\w+(?:\.\w+)+' + end_of_email+')', body)]
    countUniqueMailes(m)
    print "liczba maili:", unique_mailes.keys().__len__()

def parseAbrvs(body):
    naive_abrvs = {}
    abrvs = [x[0] for x in re.findall(r'((?<=\s)[a-zA-z]{1,3}\.' + end_of_abrv + ')', body, re.DOTALL | re.UNICODE)]
    for abrv in abrvs:
        if not naive_abrvs.has_key(abrv): naive_abrvs[abrv] = True
    print "liczba skrotow:",naive_abrvs.keys().__len__()
    for key in naive_abrvs.keys():print key,
    print

def findSentences(text):
    m = re.findall(r'((?<=\s)[a-zA-Z]{4,}[.!?]+)(?=$|\W)|([a-zA-Z]+(\s*<.*?>)*?\s*\n)', text, re.UNICODE | re.MULTILINE)
    #for s in m: print s[0]
    print "liczba zdan:", m.__len__()

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()
    fp.close()
    body = re.search(r'<P>(.+?)<META', content, re.DOTALL | re.UNICODE).group(1)
    print "nazwa pliku:", filepath
    parseAuthor(content)
    parseDepartament(content)
    parseKeyWords(content)
    parseAbrvs(body)
    findIntegers(body)
    findSentences(body)
    findFloats(body)
    findDates(body)
    findMailes(body)
    print("\n")
    global unique_floats, unique_dates, unique_abrvs, unique_integers, unique_mailes
    unique_dates = {}
    unique_mailes = {}
    unique_floats = {}
    unique_integers = {}
    unique_abrvs = {}
    #sys.stdin.read(1)

try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)