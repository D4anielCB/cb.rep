import sys, json, re, os, requests

fullpath = sys.argv[1]
file = fullpath.split('\\')
fileold = file[len(file)-1]
folder = re.sub(fileold, '', fullpath, flags=re.IGNORECASE)

arr = os.listdir(folder)

print(fullpath)
print(arr)
print(arr)
print(fullpath)
print("----------")

#season = "1"
season = input('Digite a season: ')

for entry in arr:
	if not re.compile("s\d+e\d+", re.IGNORECASE).findall(entry):
		epi = re.compile("(\d+)(\..{3})", re.IGNORECASE).findall(entry)
		#print(epi[0][0])
		inicio = os.path.join(folder,entry)
		fim = os.path.join(folder,"S"+season+"E"+epi[0][0]+epi[0][1])
		print(fim)
		os.rename(inicio, fim)