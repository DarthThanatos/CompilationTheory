import re

b = "To 1.2e+3 1. 01/03/1994.?!?!? 32687!? -319 -1  -1. -1. 10.1 -1.0 1.0 .5" +\
" -.5e+3 2013-12-03 zadanie wymaga uwagi. " +\
"Email : robert.bielas.alfaomega95@interia.pl " +\
"robert.bielas.alfaomega95@interia.pl " +\
"robert.bielas.alfaomega95@interia.p1l " +\
"19-05-1995..??!. Proces 19/05/1995 odkrycia we 31-99-0000 0000-30-02" +\
" wszystkich dziedzinach jest ok. 12.03.2013 " +\
"30.13.2000 J. CZ. taki sam. 2010-20-03 2010.20.01 " +\
"2010/29/03 2010/30/03 01.01.0010...?!!?<font size = 1>\n"+\
"Mam nadzieje ze nie. A ja tak.\n"

end_of_token = r'(?=\s|\.\s)'
end_of_date = r'(?=\s|\.\s|\.$|\.+|\!+|\?+|(\.+\!*\?*)+|(\.*\?+\!*)+|(\.*\?*\!+)+)'
end_of_abrv = r'(?=\s|\.\s|\.$|\.+|\!+|\?+|(\.+\!*\?*)+|(\.*\?+\!*)+|(\.*\?*\!+)+)'
end_of_number = r'(?=\s|$|\?+|\!+|(\?*\!+)+|(\?+\!*)+)'
end_of_email = r'(?=\s|$|\?+|\!+|(\?*\!+)+|(\?+\!*)+)'

unique_dates = {}
unique_mailes = {}
unique_floats = {}
unique_integers = {}
unique_abrvs = {}

#\d\d\d\d\.\d\d\.\d\d
#\d\d\.\d\d\.\d\d\d\d

def countUniqueFloats(floats_list):
	for real in floats_list:
		print "uf:",real
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

def parseAbrvs(body):
	naive_abrvs = {}
	print "liczba skrotow:",
	abrvs = re.findall(r'((?<=\s)[a-zA-z]{1,3}\.' + end_of_abrv + ')', body, re.DOTALL | re.UNICODE)
	print "\nNaive abrvs amount:",naive_abrvs.keys().__len__()
	#nie, lat
	return abrvs

def findAbrvs_compicated():
	#this regex assumes that after a dot there is not a white space 
	#with a capital letter starting a new sentence
	m = [x[0] for x in re.findall(r'((?<=\s)[a-zA-z]{1,3}\.(?!\n|(((\.*\?*\!*)+)?\s[A-Z0-9]([a-zA-Z0-9]{3,}|\s))))', b)] 
	countUniqueAbrvs(m)
	return m

def findSentences(text):
	date_parts = r'\d\d\.\d\d\.\d\d\d\d|\d\d\d\d\.\d\d\.\d\d'
	float_parts = r'((?<=\s)([-]?(?P<before_dot>[1-9]\d*)?(?(before_dot)\.\d*|\.\d+)((e|E)(\+|-)?\d+)?)(?=\s))'
	sentence_pattern = r'(([a-zA-Z]{4,}[.!?]+)(?=$|\W)|([a-zA-Z]+(\s*<[\S\s]*?>)*\s*\n))'
	dots_in_mails = re.findall(r'(\w+(?P<first_dot>\.(\w+))*@\w+(?P<second_dot>\.\w+)+' + end_of_email +')',text)
	print dots_in_mails
	sentence_pattern = r'(?<!\s\d\d)\.|(?<!\s\d\d\d\d)\.|(?<!\s[a-zA-Z])\.|(?<!\s[a-zA-Z][a-zA-Z])\.|(?<!\s[a-zA-Z][a-zA-Z][a-zA-Z])\.'
	# ^data | abrv | float | email
	m = re.findall(sentence_pattern,text)
	return m

def findFloats(text):
	m = [x[0] for x in re.findall(r'((?<=\s)([-]?(?P<before_dot>[1-9]\d*)?(?(before_dot)\.\d*|\.\d+)((e|E)(\+|-)?\d+)?)(?=' +end_of_number + '))', text)]
	countUniqueFloats(m)
	return m

def findIntegers(text):
	m = [x[1] for x in re.findall(r'((?<=\s)(?P<integer>[-]?([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-2][0-9][0-9][0-9][0-9]|3[0-1][0-9][0-9][0-9]|32[0-6][0-9][0-9]|327[0-5][0-9]|3276[0-7]|-32768))(?='+ end_of_number + '))', text)]
	countUniqueIntegers(m)
	return m


def dd_mm_rrrr():
	m =  [x[0] for x in re.findall(r'((?<=\s)0[1-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d' + end_of_date +'|(?<=\s)0[1-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #01-09.01-12.rrrr
	m += [x[0] for x in re.findall(r'((?<=\s)[1-2][0-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d' + end_of_date + '|(?<=\s)[1-2][0-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #10-19.01-12.rrrr
	m += [x[0] for x in re.findall(r'((?<=\s)30(?P<delimiter>[\./-])(?!02|1[3-9]|00|[2-9][0-9])\d\d(?P=delimiter)\d\d\d\d' + end_of_date + '|(?<=\s)31(?P<delimiter1>[\./-])(?=(?:01|03|05|07|08|10|12))\d\d(?P=delimiter1)\d\d\d\d'+end_of_date+')',b)] #30-31.01-12.rrrr
	countUniqueDates(m)
	return m

def rrrr_dd_mm():
	m =  [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])0[1-9](?P=delimiter)[0][1-9]'+end_of_date+'|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])0[1-9](?P=delimiter1)[1][0-2]'+end_of_date+')',b)] #rrrr.01-09.01-12
	m += [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])[1-2][0-9](?P=delimiter)[0][1-9]'+end_of_date+'|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])[1-2][0-9](?P=delimiter1)[1][0-2]'+end_of_date+')',b)] #rrrr.10-19.01-12
	m += [x[0] for x in re.findall(r'((?<=\s)\d\d\d\d(?P<delimiter>[\./-])30(?P=delimiter)(?!02|1[3-9]|00|[2-9][0-9])\d\d'+end_of_date+'|(?=\s|\.\s)\d\d\d\d(?P<delimiter1>[\./-])31(?P=delimiter1)(?=01|03|05|07|08|10|12)\d\d'+end_of_date+')',b)] #rrrr.30-31.01-12
	countUniqueDates(m)
	return m

def findMailes():
	m = [x[0] for x in re.findall(r'((?<=\s)\w+(\.(\w+))*@\w+(?:\.\w+)+'+end_of_email+')', b)]
	mail_list = [re.sub(r' ',r'', x) for x in m]
	countUniqueMailes(mail_list)
	return mail_list

"""
def findFloats(text):
	m = [x[0] for x in re.findall(r'((?<=\s)([-]?(?P<before_dot>[1-9]\d*)?(?(before_dot)\.\d*|\.\d+)((e|E)(\+|-)?\d+)?)(?=\s))', text)]
	countUniqueFloats(m)
	print("liczba liczb zmiennoprzecinkowych:"), unique_floats.keys().__len__()
	return m

def findIntegers(text):
	m = [x[1] for x in re.findall(r'((?<=\s)(?P<integer>[-]?([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-2][0-9][0-9][0-9][0-9]|3[0-1][0-9][0-9][0-9]|32[0-6][0-9][0-9]|327[0-5][0-9]|3276[0-7]|-32768))(?=\s))', text)]
	countUniqueIntegers(m)
	print("liczba liczb calkowitych z zakresu int:"), unique_integers.keys().__len__()
	return m

def dd_mm_rrrr(body):
	m =  [x[0] for x in re.findall(r'(\s0[1-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d\b|\b0[1-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d\s)',body)] #01-09.01-12.rrrr
	m += [x[0] for x in re.findall(r'(\s1[0-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d\b|\b1[0-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d\s)',body)] #10-19.01-12.rrrr
	m += [x[0] for x in re.findall(r'(\s2[0-9](?P<delimiter>[\./-])[0][1-9](?P=delimiter)\d\d\d\d\b|\b2[0-9](?P<delimiter1>[\./-])[1][0-2](?P=delimiter1)\d\d\d\d\s)',body)] #20-29.01-12.rrrr
	m += [x[0] for x in re.findall(r'(\s30(?P<delimiter>[\./-])(?!02|1[3-9])\d\d(?P=delimiter)\d\d\d\d\s|\s31(?P<delimiter1>[\./-])(?=(?:01|03|05|07|08|10|12))\d\d(?P=delimiter1)\d\d\d\d\s)',body)] #30-31.01-12.rrrr
	countUniqueDates(m)
	return m

def rrrr_dd_mm(body):
	m =  [x[0] for x in re.findall(r'(\s\d\d\d\d(?P<delimiter>[\./-])0[1-9](?P=delimiter)[0][1-9]\s|\s\d\d\d\d(?P<delimiter1>[\./-])0[1-9](?P=delimiter1)[1][0-2]\s)',body)] #rrrr.01-09.01-12
	m += [x[0] for x in re.findall(r'(\s\d\d\d\d(?P<delimiter>[\./-])1[0-9](?P=delimiter)[0][1-9]\s|\s\d\d\d\d(?P<delimiter1>[\./-])1[0-9](?P=delimiter1)[1][0-2]\s)',body)] #rrrr.10-19.01-12
	m += [x[0] for x in re.findall(r'(\s\d\d\d\d(?P<delimiter>[\./-])2[0-9](?P=delimiter)[0][1-9]|\s\d\d\d\d(?P<delimiter1>[\./-])2[0-9](?P=delimiter1)[1][0-2])',body)] #rrrr.20-29.01-12
	m += [x[0] for x in re.findall(r'(\s\d\d\d\d(?P<delimiter>[\./-])30(?!02|1[3-9])(?P=delimiter)\d\d\s|\s\d\d\d\d(?P<delimiter1>[\./-])31(?=01|03|05|07|08|10|12)(?P=delimiter1)\d\d)',body)] #rrrr.30-31.01-12
	countUniqueDates(m)
	return m
	
def findDates(body):
	dd_mm_rrrr(body)
	rrrr_dd_mm(body)
	print("liczba dat:"), unique_dates.keys().__len__()

def findMailes(body):
	m = [x[0] for x in re.findall(r'(\w+(\.(\w+))*@\w+(?:\.\w+)+\s+)', body)]
	mail_list = [re.sub(r' ',r'', x) for x in m]
	countUniqueMailes(mail_list)
	return mail_list
"""

print dd_mm_rrrr()
print rrrr_dd_mm()
print findMailes(), unique_mailes.keys().__len__()
print 'unique_dates:',unique_dates.keys().__len__()
for key,item in unique_dates.items():
	print item
text = b

print findFloats(text), unique_floats.keys().__len__()
print findIntegers(text), unique_integers.keys().__len__()
parseAbrvs(text)

#text = re.sub(r'\.(?!(\n|(((\.*\?*\!*)+)?\s[A-Z0-9]([a-zA-Z0-9]{3,}|\s))))', '', text)
print "\n===\n",text,"\n===\n"
for sentence in findSentences(text):
	pass #print sentence