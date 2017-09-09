import re

pattern = r'(\d+)\.(\d*)'
str = 'a + 342.79+ b + 12.56 * 10'
r = re.compile(pattern)

m = r.match(str)   # brak dopasowania
#re.match(pattern, str [, pos [, endpos]])

m = r.search(str)  # dopasowuje pierwsza liczbe zmiennoprzecinkowa, tj. 342.79
#re.search(pattern, str [, pos [, endpos]])

#help (m)
if m:
    print "mgroup",(m.group(0)), m.group(1), m.group(2)


floats = [ x[0] for x in re.findall( r'((\d+)\.(\d*))', str) ]
#for 342.79 x returns (342.79, 342, 79)

print("floats=", floats)

for m in r.finditer(str):
    print "finditer", (m.group()),

print
list = [ m.group() for m in r.finditer(str) ]
print("list=", list)

terms = re.split("\s*[+*]\s*", str);
print(terms)

terms = re.split("(\s*[+*]\s*)", str);
print(terms)


newstr = r.sub("\\2.\\1", str);
print(str)
print(newstr)

print( r.subn(r"\2.\1", str) );

s = "http://python.org"
pattern = r'(http://[\w]+(.[\w]+)*(/[\w~]*)?)'
r = re.compile(pattern)
s2 = r.sub(r'<a href="\1">\1</a>', s)
print(s2)

#\d - dow. cyfra
#\s - dow. bialy znak
#\w - dow. znak lub cyfra


str = r'<TR><TD>Autor</TD><TD> <A HREF="/info/autor-info.html?autorID=1060">Wojciech Niemirycz</A>'
pattern = r'\DautorID=\d+">(\w+) (\w+)</A>'
name = re.search(pattern, str)
name

#m = re.findall(r' [a-zA-Z]{1,3}\.(?!$|\s*[A-Z])',b)
# abrvs
import re 
b = "Proces odkrycia we wszystkich dziedzinach jest ok. J. CZ. Taki sam.\n"
m = re.findall(r' [a-zA-Z]{1,3}\.(?!\s*[A-Z][a-zA-Z]{3,}|\s*\n)', b, re.UNICODE) 

#sentences
import re 
b = "To zadanko ssie. Proces odkrycia we wszystkich dziedzinach jest ok. J. CZ. Taki sam.\n"
c = re.sub('(\s[a-zA-Z]{1,3})\.',r'\1',b)
m = re.findall( r'(.+?(\.|\n))', c, re.UNICODE)

#dates
import re

b = "To zadanko ssie. 21-01-1995 Proces 21/01/1995 odkrycia we wszystkich dziedzinach jest ok. J. CZ. Taki sam.\n"
def findDate_dd_mm_rrrr():
	m = re.findall(r'\b0[1-9]-[0][1-9]-\d\d\d\d\b|\b0[1-9]-[1][0-2]-\d\d\d\d\b',b) #01-09.01-12.rrrr
	m += re.findall(r'\b1[0-9]-[0][1-9]-\d\d\d\d\b|\b1[0-9]-[1][0-2]-\d\d\d\d\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b2[0-9]-[0][1-9]-\d\d\d\d\b|\b2[0-9]-[1][0-2]-\d\d\d\d\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b(0[1-9]\.[0][1-9]\.\d\d\d\d\b)|\b0[1-9]\.[1][0-2]\.\d\d\d\d\b',b) #01-09.01-12.rrrr
	m += re.findall(r'\b1[0-9]\.[0][1-9]\.\d\d\d\d\b|\b1[0-9]\.[1][0-2]\.\d\d\d\d\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b2[0-9]\.[0][1-9]\.\d\d\d\d\b|\b2[0-9]\.[1][0-2]\.\d\d\d\d\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b(0[1-9]/[0][1-9]/\d\d\d\d\b)|\b0[1-9]/[1][0-2]/\d\d\d\d\b',b) #01-09.01-12.rrrr
	m += re.findall(r'\b1[0-9]/[0][1-9]/\d\d\d\d\b|\b1[0-9]/[1][0-2]/\d\d\d\d\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b2[0-9]/[0][1-9]/\d\d\d\d\b|\b2[0-9]/[1][0-2]/\d\d\d\d\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b30-(?!02|1[3-9])\d\d-\d\d\d\d\b|\b31-(?=(?:01|03|05|07|08|10|12))\d\d-\d\d\d\d\b',b) #szczegolny przypadek
	m += re.findall(r'\b30/(?!02|1[3-9])\d\d/\d\d\d\d\b|\b31/(?=(?:01|03|05|07|08|10|12))\d\d/\d\d\d\d\b',b) #szczegolny przypadek
	m += re.findall(r'\b30\.(?!02|1[3-9])\d\d\.\d\d\d\d\b|\b31\.(?=(?:01|03|05|07|08|10|12))\d\d\.\d\d\d\d\b',b) #szczegolny przypadek
	#m += re.findall(r'\b30\.(?!02\.\d\d\d\d\b)|\b31\.(?=(01|03|05|07|08|10|12)\.\d\d\d\d\b)',b) #szczegolny przypadek
	countUniqueDates(m)
	return m

def findDate_rrrr_dd_mm():
	m = re.findall(r'\b\d\d\d\d-0[1-9]-[0][1-9]\b|\b\d\d\d\d-0[1-9]-[1][0-2]\b',b) #rrrr.01-09.01-12
	m += re.findall(r'\b\d\d\d\d-1[0-9]-[0][1-9]\b|\b\d\d\d\d-1[0-9]-[1][0-2]\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d-2[0-9]-[0][1-9]\b|\b\d\d\d\d-2[0-9]-[1][0-2]\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d\.0[1-9]\.[0][1-9]\b|\b\d\d\d\d\.0[1-9]\.[1][0-2]\b',b) #01-09.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d\.1[0-9]\.[0][1-9]\b|\b\d\d\d\d\.1[0-9]\.[1][0-2]\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d\.2[0-9]\.[0][1-9]\b|\b\d\d\d\d\.2[0-9]\.[1][0-2]\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d/0[1-9]/[0][1-9]\b|\b\d\d\d\d/0[1-9]/[1][0-2]\b',b) #01-09.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d/1[0-9]/[0][1-9]\b|\b\d\d\d\d/1[0-9]/[1][0-2]\b',b) #10-19.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d/2[0-9]/[0][1-9]\b|\b\d\d\d\d/2[0-9]/[1][0-2]\b',b) #20-29.01-12.rrrr
	m += re.findall(r'\b\d\d\d\d-30-(?!02|1[3-9])\d\d\b|\b\d\d\d\d-31-(?=(?:01|03|05|07|08|10|12))\d\d\b',b) #szczegolny przypadek
	m += re.findall(r'\b\d\d\d\d/30/(?!02|1[3-9])\d\d\b|\b\d\d\d\d/31/(?=(?:01|03|05|07|08|10|12))\d\d\b',b) #szczegolny przypadek
	m += re.findall(r'\b\d\d\d\d\.30\.(?!02|1[3-9])\d\d\b|\b\d\d\d\d\.31\.(?=(?:01|03|05|07|08|10|12))\d\d\b',b) #szczegolny przypadek
	#dd-mm-rrrr; dd/mm/rrrr; dd.mm.rrrr
	#rrrr-dd-mm; rrrr/dd/mm; rrrr.dd.mm
	countUniqueDates(m)
	return m