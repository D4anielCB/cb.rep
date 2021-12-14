import sys, json, re, os, requests

def RT(arquivo="_anime.txt"):
	file = open(arquivo, "r")
	return file.read()
	
def ST(x="", o="w", tipo=True, arquivo="study.txt"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]) or type(x) == type(set([''])):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		try:
			y = str(x)
		except:
			y = str(str(x).encode("utf-8"))
	file = open(arquivo, o)
	if tipo:
		file.write(y+"\n"+str(type(x)))
	else:
		file.write(y)
	file.close()

log = RT("../kodi.log")
#log2 = re.sub('\r', '\r\n', log)
logre = re.compile("cBlack\".+?(http.+)").findall(log)


ST(logre, tipo=False, arquivo="_anime.txt")
print(logre)