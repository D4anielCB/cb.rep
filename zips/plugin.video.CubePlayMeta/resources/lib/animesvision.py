# -*- coding: utf-8 -*-
import sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, math, html, xbmcvfs
from urllib.parse import urlparse, quote_plus
from urllib.request import urlopen, Request
from urllib.parse import urlparse, quote_plus, unquote
import urllib.request, urllib.parse, urllib.error
import urllib.parse

import common
import xx

AddonID = 'plugin.video.CubePlayMeta'
Addon = xbmcaddon.Addon(AddonID)
addon_data_dir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
addonDir = Addon.getAddonInfo('path')
icon = os.path.join(addonDir,"icon.png")
AddonName = Addon.getAddonInfo("name")

from metadatautils import MetadataUtils
mg = MetadataUtils()
mg.tmdb.api_key = 'bd6af17904b638d482df1a924f1eabb4'

MUlang = "pt-BR" if Addon.getSetting("MUlang") == "0" else "en"
MUcache = True if Addon.getSetting("MUcache") == "true" else False
MUcacheEpi = True if Addon.getSetting("MUcacheEpi") == "true" else False
MUfanArt = True if Addon.getSetting("MUfanArt") == "true" else False
Ctrakt = Addon.getSetting("Ctrakt") if Addon.getSetting("Ctrakt") != "" else None
crsession = Addon.getSetting("crsession") if Addon.getSetting("crsession") != "" else ""
	
# -----------------------------
params =  urllib.parse.parse_qs( sys.argv[2][1:] ) 
url = params.get('url',[None])[0]
logos = params.get('logos',[None])[0]
name = params.get('name',[None])[0]
iconimage = params.get('iconimage',[None])[0]
cache = int(params.get('cache', '0')[0]) if params.get('cache') else 0
index = int(params.get('index', '-1')[0]) if params.get('index') else -1
move = int(params.get('move', '0')[0]) if params.get('move') else 0
mode = int(params.get('mode', '0')[0]) if params.get('mode') else 0
info = params.get('info',[None])[0]
background = params.get('background',[None])[0]
DL = params.get('DL',[None])[0]
year = params.get('year',[None])[0]
metah = params.get('metah',[None])[0]
episode = params.get('episode',[None])[0]
playcount = params.get('playcount',[None])[0]
# -----------------------------
def animesfilme(): #510
	#mm = mg.get_tmdb_details(tmdb_id="", title="Pokemon", year="", media_type="movies", manual_select=False, ignore_cache=False)
	#mm = mg.get_tmdb_movie(title="digimon")
	#ST(mm)
	#return
	link = common.OpenURL("https://raw.githubusercontent.com/D4anielCB/folder/main/filmes")
	lista = re.compile("(.+);(.*)\s(.+)").findall(link)
	trak = xx.traktM()
	lista.sort()
	try:
		prog = 1
		progress = xbmcgui.DialogProgress()
		progress.create('Carregando...')
		progress.update(0, "Carregando...")
		for name2,id2,url2 in lista:
			progtotal = int(100*prog/len(lista))
			progress.update(progtotal, str(progtotal)+" %")
			prog+=1
			if (progress.iscanceled()): break
			dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in url2 else "[COLOR blue][L][/COLOR]"
			#mm = mg.get_tmdb_details(tmdb_id=id2, title=name2, year="", media_type="movies", manual_select=False, ignore_cache=True)
			mm = mg.get_tmdb_details(tmdb_id=id2, imdb_id="", tvdb_id="", title=name2, year="", media_type="movies", preftype="", manual_select=False, ignore_cache=False)
			pc = 1 if mm['imdbnumber'] in trak else None
			xx.AddDir(dubleg+" "+mm['title'] + " (" + str(mm['year'])+")", url2, 513, "", mm['tmdb_id'], isFolder=False, IsPlayable=True, background=name2, metah=mm, DL="", playcount=pc)
			#break
		progress.close()
	except:
		#ST(name2)
		pass
def updateanime(): #509
	try:
		import requests
		url = 'https://api.crunchyroll.com/start_session.1.json'
		myobj = {'device_id': '35yuv973-KODI-nh6i-69l8-81m0p580id2j', 'device_type': 'com.crunchyroll.windows.desktop', 'access_token': 'LNDJgOit5yaRIWN'}
		x = requests.post(url, data = myobj)
		j=json.loads(x.text)
		id = j['data']['session_id']
		url2 = OpenURL("https://cbplay.000webhostapp.com/cr/?id="+id)
		NF("Atualizando...")
		xbmc.sleep(3000)
		xbmc.executebuiltin('UpdateLibrary(video)')
	except:
		NF('deu ruim')
def playanimenextvis(): #504
	try:
		global url, episode, playcount
		#ST(url)
		trak = xx.traktS()
		link = common.OpenURL(url)
		url2 = re.compile('screen-item-thumbnail.+?\"([^\"]+)').findall(link)
		link2 = common.OpenURL(url2[0]).replace("\n","").replace("\r","")
		lista = re.compile("data-id\=\"\d+\".+?\"([^\"]+)").findall(link2)
		#ST(lista)
		#return
		lenepisodios = len(lista)
		E = 1
		S = 1
		i = re.compile('i\=(\d+)').findall(url)
		f = re.compile('f\=(\d+)').findall(url)
		s = re.compile('s\=(\d+)').findall(url)
		start = 0
		prog = 1
		if i:
			E = int(i[0])
		meta = eval(metah)
		#ST(meta)
		if s:
			start = int(s[0])
		if f:
			fim = int(f[0]) + start
		else:
			fim = lenepisodios
		#ST(str(start) +'  '+str(fim))
		#for l in lista[start::]:
		l = lista[0]
		#ST(start,"1")
		#ST(fim,"1")
		#return
		for x in range(start, fim):
			EE = x
			EE+= 1
			url2 = re.sub('/episodio\-(\d+)\/', '/episodio-'+xx.EPIz(str(EE))+'/', l )
			pc = None
			pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(int(E)) in trak else None
			if pc == None:
				totalepi = str( fim-start )
				playcount = pc
				episode = str(E)
				#epi = str(E)
				#metah = meta
				#background=str(meta['season_number'])
				url = l
				NF( "Epi. "+str(E)+"/"+ totalepi )
				playanimevis(url2,False)
				return
				sys.exit()
			#xx.AddDir2("" ,url2, 503, "", "",  isFolder=False, IsPlayable=True, background=str(meta['season_number']), metah=meta, episode=str(E), playcount=pc)
			E+= 1
		#ST(E,"1")
		#ST(EE,"1")
		if fim == EE:
			NF("Nenhum episódio novo")
	except:
		NF("Servidor offline")
def listanimevis(pastebin): #500
	#filmes = ["Mortal Kombat","Nobody","Run","Get out","The Flash"]
	#for f in filmes:
	#	mm = mg.get_tmdb_details(tmdb_id="", imdb_id="", tvdb_id="", title=f, year="", media_type="movies", preftype="", manual_select=False, ignore_cache=False)
		#ST(mm)
	#	if mm:
	#		xx.AddDir(mm['title'] + " (" + str(mm['year'])+")", "", 503, "", "", isFolder=False, IsPlayable=True, background="", metah=mm)
		#ST(mmm)
	#return
	#mm = mg.get_tmdb_details(imdb_id="", tvdb_id="", title="The Flash", year="", media_type="tvshows", manual_select=False, ignore_cache=True)
	#f = str(mm).encode('utf-8')
	#f = re.sub('^b', "", str( f ) )
	#f = "{'tmdb_id': 85937, 'rating': 8.9, 'originaltitle': 'Tanjir\xc5\x8d resolves'}"
	#ST( eval(f) )
	#ST(mm)
	#AddDir2("", "", 501, iconimage, iconimage, info=pastebin, isFolder=True, background=background, metah=mm[-1])
	#return
	#mmm = mg.get_tmdb_details(tmdb_id="10228", imdb_id="", tvdb_id="", title="", year="", media_type="movies", preftype="", manual_select=False, ignore_cache=True)
	#ST(mmm)
	#return
	try:
		link = common.OpenURL("https://raw.githubusercontent.com/D4anielCB/folder/main/"+pastebin).replace("\n","+")+"*"
		lista = re.compile("\*?(.+?);(\d+)?;\+(.+?)\*").findall(link)
		animes=[]
		prog = 1
		progress = xbmcgui.DialogProgress()
		progress.create('Carregando...')
		progress.update(0, "Carregando...")
		for name2,id2,cont in lista:
			try:
				progtotal = int(100*prog/len(lista))
				progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
				prog+=1
				if (progress.iscanceled()): break
				mmm = mg.get_tvshow_details(title=name2,tmdb_id=id2, ignore_cache=MUcache, lang=MUlang)
				dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in cont else "[COLOR blue][L][/COLOR]"
				animes.append([mmm[-1]['TVShowTitle'],name2,mmm[-1],dubleg])
			except:
				pass
		animes = sorted(animes, key=lambda animes: animes[0])
		for title,name2,met,dubleg in animes:
			#try:
			xx.AddDir2(dubleg+" "+title, name2, 501, iconimage, iconimage, info=pastebin, isFolder=True, background=background, metah=met)
			#except:
				#pass
		progress.close()
	except:
		pass
def addanimefav(): #507
	data = {"url": url, "tmdb": str(info), "season" : str(background) }
	sf = common.SaveFile(data, "url",  "animebiz", "")
	if sf:
		xbmc.executebuiltin('reloadskin')
def listseavis(): #501
	link = common.OpenURL("https://raw.githubusercontent.com/D4anielCB/folder/main/"+info).replace("\n","+")+"+*"
	lista = re.compile("\*?(.+?);(\d+)?;\+(.+?)\*").findall(link)
	cont1 = ""
	for name2,id2,cont2 in lista:
		if name2 == url:
			cont1 = cont2
	lista = re.compile("(\d+)?;?(.+?)\+").findall(cont1)
	meta = eval(metah)
	for season,url2 in lista:
		try:
			mmm = mg.get_tvshow_details(title="",tmdb_id=meta['tmdb_id'], ignore_cache=MUcache, lang=MUlang)
			season = "1" if season == "" else season
			metasea=xx.mergedicts(meta,mmm[int(season)])
			dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in url2 else "[COLOR blue][L][/COLOR]"
			plus = "+" if "i=" in url2 else ""
			xx.AddDir2(dubleg+"["+season+"]"+plus+" "+metasea["name"], url2, 502, iconimage, iconimage, info=metasea["tmdb_id"], isFolder=True, background=season, metah=metasea)
			if "dublado" in url2 and not "noleg=1" in url2:
				xx.AddDir2("[COLOR blue][L][/COLOR]["+season+"]"+plus+" "+metasea["name"], url2.replace("-dublado",""), 502, iconimage, iconimage, info=metasea["tmdb_id"], isFolder=True, background=season, metah=metasea)
		except:
			pass
	if Ctrakt == None:
		return
	#AddDir("Reload" , "", 507, isFolder=False)
	xx.AddDir("---------- Autoplay ----------" , "", 40, isFolder=False)
	for season,url2 in lista:
		try:
			mmm = mg.get_tvshow_details(title="",tmdb_id=meta['tmdb_id'], ignore_cache=MUcache, lang=MUlang)
			season = "1" if season == "" else season
			metasea=xx.mergedicts(meta,mmm[int(season)])
			metasea['mediatype'] = "episode"
			dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in url2 else "[COLOR blue][L][/COLOR]"
			plus = "+" if "i=" in url2 else ""
			xx.AddDir2(dubleg+"["+season+"]"+plus+" "+metasea["TVShowTitle"], url2, 504, "", "", info=metasea["tmdb_id"], isFolder=False, IsPlayable=True, background=season, metah=metasea)
			if "dublado" in url2 and not "noleg=1" in url2:
				xx.AddDir2("[COLOR blue][L][/COLOR]["+season+"]"+plus+" "+metasea["TVShowTitle"], url2.replace("-dublado",""), 504, "", "", info=metasea["tmdb_id"], isFolder=False, IsPlayable=True, background=season, metah=metasea)
		except:
			pass
def animeepisvis(): #502
	try:
		#global url
		#url = "http://animesvision.biz/animes/pokemon-2019?page=5"
		trak = xx.traktS()
		link = common.OpenURL(url)
		url2 = re.compile('screen-item-thumbnail.+?\"([^\"]+)').findall(link)
		link2 = common.OpenURL(url2[0]).replace("\n","").replace("\r","")
		lista = re.compile("data-id\=\"\d+\".+?\"([^\"]+)").findall(link2)
		#ST(lista)
		#return
		lenepisodios = len(lista)
		#lenepisodios = int(lenepisodios[0])
		#ST(lenepisodios)
		E = 1
		S = 1
		i = re.compile('i\=(\d+)').findall(url)
		f = re.compile('f\=(\d+)').findall(url)
		s = re.compile('s\=(\d+)').findall(url)
		start = 0
		prog = 1
		progress = xbmcgui.DialogProgress()
		progress.create('Carregando...')
		progress.update(0, "Carregando...")
		if i:
			E = int(i[0])
		meta = eval(metah)
		if s:
			start = int(s[0])
		if f:
			fim = int(f[0]) + start
		else:
			fim = lenepisodios
		#ST(str(start) +'  '+str(fim))
		#for l in lista[start::]:
		#ST(fim)
		l = lista[0]
		for x in range(start, fim):
			EE = x
			EE+= 1
			url2 = re.sub('episodio\-(\d+)\/', 'episodio-'+xx.EPIz(str(EE))+'/', l )
			progtotal = int( 100*prog/(fim-start) )
			progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
			prog+=1
			if (progress.iscanceled()): break
			pc = None
			if meta['imdbnumber']:
				pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(int(E)) in trak else None
			xx.AddDir2("" ,url2, 503, "", "",  isFolder=False, IsPlayable=True, background=str(meta['season_number']), metah=meta, episode=str(E), playcount=pc)
			#xx.AddDir2(url2 ,url2, 503, "", "",  isFolder=False, IsPlayable=True)
			E+= 1
		progress.close()
	except:
		pass
		
def testviision(x):
	req = Request(url)
	#req.add_header('Content-Type', 'video/mp4')
	#req.add_header('Accept-Ranges', 'bytes')
	req.add_header('Range', 'bytes=0-1000')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/248.65')
	resp = urlopen(req)
	length = str(resp.headers)
	return length
def RetLinks(elo,direct=False):
	from math import floor
	link = common.OpenURL(elo)
	epi = re.compile('episodio-(\d{0,3})').findall(elo)
	epi = epi[0]
	res = re.compile("gerarDownload\('(.{1,8})'\)").findall(link)
	resolution = {}
	for entry in res:
		if "vip_fhd" in entry: resolution["1080p"] = ""
		if direct==False:
			if "vip_hd" in entry: resolution["720p"] = ""
			if "vip_sd" in entry: resolution["480p"] = ""
	url2 = re.sub('\/episodio\-.+', '', url )
	page = re.compile('\.0$').findall( str( int(epi) / 16) )
	if page:
		page = str(  floor( int(epi) / 16) )
	else:
		page = str(  floor( int(epi) / 16) +1 )
	link2 = common.OpenURL(url2+"?page="+page).replace("\/","/")
	vid = re.compile('https?.{30,95}'+epi+'\.mp4').findall(link2)
	if not vid:
		link2 = common.OpenURL(url2).replace("\/","/")
		vid = re.compile('https?.{30,95}\.mp4').findall(link2)
	if vid:
		for entry in resolution:
			mp4 = re.sub('\/\d{3,4}p\/', "/"+entry+"/", vid[0] )
			mp4 = re.sub('\d{0,4}.mp4$', epi+".mp4", mp4 )
			resolution[entry] = mp4
	else:
		resolution["erro"] = ""
	return resolution
def RetLinksMovie(elo,direct=False):
	link = common.OpenURL(elo)
	#epi = re.compile('episodio-(\d{0,3})').findall(elo)
	#epi = epi[0]
	res = re.compile("gerarDownload\('(.{1,8})'\)").findall(link)
	resolution = {}
	for entry in res:
		if "vip_fhd" in entry: resolution["1080p"] = ""
		if direct==False:
			if "vip_hd" in entry: resolution["720p"] = ""
			if "vip_sd" in entry: resolution["480p"] = ""
	url2 = re.sub('(https?:\/\/[^\/]+\/[^\/]+\/[^\/]+)(.+)', r'\1', url )
	link2 = common.OpenURL(url2).replace("\/","/")
	vid = re.compile('https?.{10,105}\.mp4').findall(link2)
	if vid:
		for entry in resolution:
			mp4 = re.sub('\/\d{3,4}p\/', "/"+entry+"/", vid[0] )
			#mp4 = re.sub('\d{0,4}.mp4$', epi+".mp4", mp4 )
			resolution[entry] = mp4
	else:
		resolution["erro"] = ""
	return resolution
	#return res
def playanimevis(elo="",choice=True,type="Episodes"): #503
	if not elo:
		return
	if not "/download" in elo:
		elo = elo+"/download"
	openvideo = common.OpenURL(elo).replace("\\","").replace("&quot;",'"').replace("&amp;",'&')
	videos = re.compile("https:\/\/ouo\.io\/.+?\?s=([^\"]+)").findall(openvideo)
	videos.reverse()
	qual1 = []
	qual2 = []
	for video in videos:
		qual = re.compile("(https?.+?(\d{3,4}p).+)").findall(video)
		qual1.append(qual[0][0])
		qual2.append(qual[0][1])
	if xbmc.Player().isPlaying() or choice == False:
		d = 0
	else:
		d = xbmcgui.Dialog().select("Escolha a qualidade:", qual2)
	if d > -1:
		xx.PlayUrl("", qual1[d] + "|referer=https://ouo.io/&User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0", iconimage, epi=episode)
def opcoes(): #514
	sel = xbmcgui.Dialog().yesno('CubePlay', 'O que fazer?','Play','Abir episódios',5000)
	if sel == False: #play
		playanimenextvis()
	else:
		RP = '{0}?mode=502&url={1}&background={2}&metah={3}'.format(sys.argv[0], quote_plus(url), quote_plus(background), quote_plus(metah))
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
def listfavanivisPlay(): #508
	#AddDir("Reload" , "", 40, isFolder=False)
	#try:
	if not Ctrakt:
		return
	try:
		file = os.path.join(addon_data_dir, "animebiz.txt")
		favList = common.ReadList(file)
		i = 0
		for ids in favList:
			mmm = mg.get_tvshow_details(title="",tmdb_id=str(ids['tmdb']), ignore_cache=MUcache, lang=MUlang)
			metasea=xx.mergedicts(mmm[-1],mmm[int(ids['season'])])
			metasea['mediatype'] = "episode"
			dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in ids['url'] else "[COLOR blue][L][/COLOR]"
			#xx.AddDir2(dubleg+"["+ids['season']+"] "+mmm[-1]['TVShowTitle'], ids['url'], 504, "", "animebiz", info="", isFolder=False, IsPlayable=True, background=ids['season'], metah=metasea, index=i)
			xx.AddDir2(mmm[-1]['TVShowTitle'], ids['url'], 514, "", "animebiz", info="", isFolder=False, IsPlayable=True, background=ids['season'], metah=metasea, index=i)
			i+=1
	except:
		pass
def listfavanivis(): #512
	try:
		file = os.path.join(addon_data_dir, "animebiz.txt")
		favList = common.ReadList(file)
		for ids in favList:
			mmm = mg.get_tvshow_details(title="",tmdb_id=str(ids['tmdb']), ignore_cache=MUcache, lang=MUlang)
			metasea=xx.mergedicts(mmm[-1],mmm[int(ids['season'])])
			dubleg="[COLOR yellow][D][/COLOR]" if "dublado" in ids['url'] else "[COLOR blue][L][/COLOR]"
			xx.AddDir2(mmm[-1]['TVShowTitle'], ids['url'], 502, "", "", info="", isFolder=True, background=ids['season'], metah=metasea)
	except:
		pass
#----------------------------------------
def ST(x="", o="w"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		y = str(str(x).encode("utf-8"))
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, o)
	file.write(y+"\n"+str(type(x)))
	file.close()
#----------------------------------------	
def NF(x, t=5000):
	xbmc.executebuiltin("Notification({0}, {1}, {3}, {2})".format(AddonName, str(x), icon, t))
