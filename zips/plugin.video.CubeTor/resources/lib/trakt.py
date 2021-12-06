# -*- coding: utf-8 -*-
import xbmc
import sys, xbmcplugin, xbmcgui, xbmcaddon, os, json, hashlib, re, unicodedata, math, xbmcvfs
import shutil
from urllib.parse import urlparse, quote_plus, unquote
from urllib.request import urlopen, Request
import urllib.request, urllib.parse, urllib.error
import urllib.parse

from metadatautils import MetadataUtils
mg = MetadataUtils()
mg.tmdb.api_key = 'bd6af17904b638d482df1a924f1eabb4'

AddonID = 'plugin.video.CubeTor'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
addonDir = Addon.getAddonInfo('path')
icon = os.path.join(addonDir,"icon.png")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import xx

MUlang = "pt-BR" if Addon.getSetting("MUlang") == "1" else "en"
MUlangM = "pt-BR" if Addon.getSetting("MUlangM") == "1" else "en"
MUcache = True if Addon.getSetting("MUcache") == "true" else False
MUcacheEpi = True if Addon.getSetting("MUcacheEpi") == "true" else False
MUfanArt = True if Addon.getSetting("MUfanArt") == "true" else False

CexternalUrl = True if Addon.getSetting("CexternalUrl") == "true" else False

Ctrakt = Addon.getSetting("Ctrakt") if Addon.getSetting("Ctrakt") != "" else ""
CtraktAuth = Addon.getSetting("CtraktAuth") if Addon.getSetting("CtraktAuth") != "" else ""
CTraktResume = True if Addon.getSetting("CTraktResume") == "true" else False
CTraktPercent = int(Addon.getSetting("CTraktPercent")) if Addon.getSetting("CTraktPercent") != "" else 5

Cproxy = "https://cbplay.000webhostapp.com/nc/nc.php?u=" if Addon.getSetting("Cproxy") else ""

cDirtrtvDown = Addon.getSetting("cDirtrtvDown") if Addon.getSetting("cDirtrtvDown") != "" else ""

addon_data_dir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
cacheDir = os.path.join(addon_data_dir, "cache")
#-----------------------------------------
params = urllib.parse.parse_qs(sys.argv[2][1:])
name = params.get('name',[None])[0]
url = params.get('url',[None])[0]
mode = params.get('mode',[None])[0]
iconimage = params.get('iconimage',[None])[0]
logos = params.get('logos',[None])[0]
info = params.get('info',[None])[0]
dados = params.get('dados',[{}])[0]
#-----------------------------------------
def Auth():
	try:
		values = """
		  {
			"client_id": "ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882"
		  }
		"""
		headers = {'Content-Type': 'application/json'}
		req = Request("https://api.trakt.tv/oauth/device/code", data=values.encode('utf-8'), headers=headers)
		response_body = urlopen(req).read().decode("utf-8")
		#ST(response_body)
		#return
		entries=json.loads(response_body)
		device_code = entries["device_code"]
		Addon.setSetting("CtraktDC", device_code )
		xbmcgui.Dialog().ok(entries["user_code"], "Entre em https://trakt.tv/activate e digite o código: "+entries["user_code"]+"\nSó clique em ok após autorizar no site!!!")
		
		values = """
		  {
			"code": "%s",
			"client_id": "ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882",
			"client_secret": "afa248c068b84b0d86a0f52e6bd4b9db9b14a4429e7a741097e97b6137ab2d4f"
		  }
		"""
		values2 = values % (device_code)
		#ST(values2)
		headers = {'Content-Type': 'application/json'}
		req = Request("https://api.trakt.tv/oauth/device/token", data=values2.encode('utf-8'), headers=headers)
		response_body = urlopen(req).read().decode("utf-8")
		entries=json.loads(response_body)
		token = entries["access_token"]
		Addon.setSetting("CtraktAuth", token )
		xx.NF("Trakt configurado!")
	except:
		xx.NF("Erro, refaça a configuração")
	try:
		setuser(token)
		#setuser("f50ecf8ae20e70de9882b75d574d4f2ce96ba971d1b50867159b214cd18b8380")
	except:
		pass
	#ST(entries)
#-----------------------------------------
def setuser(token):
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
		request = Request('https://api.trakt.tv/users/settings', headers=headers)
		response_body = urlopen(request).read()
		entries=json.loads(response_body)
		username = entries["user"]["username"]
		#ST(entries["user"]["username"])
		d = xbmcgui.Dialog().yesno("CubeTor", "Configurar como "+username)
		if not d: return
		Addon.setSetting("Ctrakt", username )
	except:
		pass
#-----------------------------------------
def TraktResumeM(dados="",type="movie"):
	import time
	dados2 = eval(dados)
	id = dados2["mmeta"]["tmdb_id"]
	RS = 0
	#ST(dados2)
	if not CtraktAuth:
		return RS
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
		request = Request('https://api.trakt.tv/sync/playback/'+type, headers=headers)
		response_body = urlopen(request).read()
		entries=json.loads(response_body)
		for entry in entries:
			try:
				if entry["type"] == "movie":
					if entry["movie"]["ids"]["tmdb"] == id:
						RS = entry["progress"]
						break
			except:
				pass
	except:
		RS = -1
	try:
		total = dados2["mmeta"]["Runtime"]*int(RS)/100
		#total = str(time.gmtime(total))
		total = str(time.strftime("%H:%M:%S", time.gmtime(total*60)))
	except:
		total = str(RS)+"%"
	return [int(RS),str(RS),total]
def TraktResumeS(dados="",type="episodes"):
	import time
	dados2 = eval(dados)
	id = int(dados2["meta"]["tmdb_id"])
	season = int(dados2["season"])
	episode = int(dados2["episode"])
	RS = 0
	if not CtraktAuth:
		return RS
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
		request = Request('https://api.trakt.tv/sync/playback/'+type, headers=headers)
		response_body = urlopen(request).read()
		entries=json.loads(response_body)
		for entry in entries:
			try:
				if entry["type"] == "episode":
					if entry["episode"]["season"] == season and entry["episode"]["number"] == episode:
					#if id == entry["movie"]["ids"]["tmdb"]:
						RS = entry["progress"]
					break
			except:
				pass
	except:
		RS = -1
	try:
		total = dados2["meta"]["duration"]*int(RS)/100
		#total = str(time.gmtime(total))
		total = str(time.strftime("%H:%M:%S", time.gmtime(total*60)))
	except:
		total = str(RS)+"%"
	return [int(RS),str(RS),total]
#-----------------------------------------
def MoviesStarted():
	trak = xx.traktM()
	headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
	request = Request('https://api.trakt.tv/sync/playback/movie', headers=headers)
	response_body = urlopen(request).read()
	entries=json.loads(response_body)
	progtotal = 0
	for entry in entries:
		if entry["type"] == "movie":
			if entry["progress"] > CTraktPercent:
				progtotal+=1
	prog = 1
	progress = eval("xbmcgui.DialogProgress()")
	progress.create('Carregando... '+str(progtotal)+" Filmes")
	progress.update(0, "Carregando...")
	for entry in entries:
		if entry["type"] == "movie":
			if (progress.iscanceled()): break
			if entry["progress"] > CTraktPercent:
				progtotal2 = int( 100*prog/progtotal )
				progress.update(progtotal2, "Só o primeiro acesso que demora\n"+str(prog)+"/"+str(progtotal)+"\n"+str(progtotal2)+" %")
				prog+=1
				try:
					mm = mg.get_tmdb_details(tmdb_id=str(entry["movie"]["ids"]["tmdb"]), imdb_id="", tvdb_id="", title="", year="", media_type="movies", preftype="", manual_select=False, ignore_cache=False, lang=MUlangM)
					pc = 1 if str(mm["tmdb_id"]) in trak else None
					xx.AddDir("", str(entry["movie"]["ids"]["tmdb"]), "tmdb.Opcoes", isFolder=False, IsPlayable=True, dados={'mmeta': mm, 'pc': pc})
				except:
					pass
#-----------------------------------------
def ShowsOptions():
	options = []
	if CtraktAuth:
		options.append('Reproduzir próximo episódio')
	if len(cDirtrtvDown) > 2:
		options.append('Download próximo episódio')
	options.append('Abrir a pasta')
	sel = 0
	if len(options) > 1:
		sel = xbmcgui.Dialog().contextmenu(options)
	if options[sel] == 'Reproduzir próximo episódio':
		RP = '{0}?mode=trakt.ShowsNext&url={1}&dados={2}'.format(sys.argv[0], quote_plus(url), quote_plus(str(dados)))
		xbmc.executebuiltin('PlayMedia("'+RP+'")')
	elif options[sel] == 'Abrir a pasta' or len(options) == 1:
		RP = '{0}?mode=trakt.Shows&url={1}&dados={2}'.format(sys.argv[0], quote_plus(url), quote_plus(str(dados)))
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
	elif options[sel] == 'Download próximo episódio':
		RP = '{0}?mode=trakt.ShowsNextDownload&url={1}&dados={2}'.format(sys.argv[0], quote_plus(url), quote_plus(str(dados)))
		xbmc.executebuiltin('PlayMedia("'+RP+'")')
def ShowsNext(playordownload="play"):
	import trtv
	meta = eval(dados)
	try:
		tvshow = meta["trtv"]
	except:
		tvshow = ""
	#ST(trtv)
	#return
	meta["forcemg"] = "1"
	imdb = meta["meta"]["imdbnumber"]
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
		request = Request('https://api.trakt.tv/shows/'+imdb+'/progress/watched', headers=headers)
		response_body = urlopen(request).read()
		rpj=json.loads(response_body)
		#ST(rpj)
		#return
		if not rpj["next_episode"]:
			xx.NF("Não há próximo episódio")
			return
		Season = str(rpj["next_episode"]["season"])
		Episode = str(rpj["next_episode"]["number"])
	except:
		xx.NF("Erro no trakt")
		return
	#ST(rpj["aired"]-rpj["completed"])
	#ST(Season)
	try:
		for entry in rpj["seasons"]:
			if int(Season) == entry["number"]:
				if int(Episode) > entry["episodes"][len(entry["episodes"])-1]["number"]:
					xx.NF("Não há próximo episódio")
					return
				xx.NF("S "+ Season +" - E "+ Episode+"/"+str(entry["episodes"][len(entry["episodes"])-1]["number"]), 6000)
				break
	except:
		pass
	if not tvshow:
		tvshow = trtv.RetId(imdb)
	try:
		link = xx.OpenURL(Cproxy + "https://trailers.to/en/tvshow/"+tvshow+"/tvshow")
	except:
		xx.NF("Erro no servidor 2!")
		return
	#ST(tvshow)
	entries = re.compile("\/en\/episode\/(\d+).{1,155}(Season|Volume) (\d?"+Season+").{1,155}Episode (\d+)", re.IGNORECASE).findall(link.replace('\n','').replace('\r',''))
	entries2 = re.compile("\/en\/episode\/(\d+).{1,155}(Season|Volume) (\d?"+Season+").+?(\d+)", re.IGNORECASE).findall(link.replace('\n','').replace('\r',''))
	entries = entries2 + entries
	if not entries:
		xx.NF("Não encontrado")
		return
	for entry in entries:
		if Episode == entry[3]:
			#ST(entry)
			#return
			meta["season"] = entry[2]
			meta["episode"] = entry[3]
			if playordownload == "download":
				#ST(1)
				RP = '{0}?mode=trtv.PlayFile&url={1}&dados={2}'.format(sys.argv[0], quote_plus(entry[0]), quote_plus(str(meta)))
				xbmc.executebuiltin('PlayMedia("'+RP+'")')
			elif playordownload == "play":
				#ST(1)
				RP = '{0}?mode=trtv.PlayUrlTv&url={1}&dados={2}'.format(sys.argv[0], quote_plus(entry[0]), quote_plus(str(meta)))
				xbmc.executebuiltin('PlayMedia("'+RP+'")')
			#trtv.PlayPrevia(entry[0])
			break
#-----------------------------------------			
def ListSeries(elo='https://api.trakt.tv/users/'+Ctrakt+'/watched/shows?extended=noseasons',typeload="DialogProgress",whereto="Shows",Play=[True,False]):
	try:
		headers = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': '888a9d79a643b0f4e9f58b5d4c2b13ee6d8bd584bc72bff8b263f184e9b5ed5d'}
		response_body = xx.OpenURL(elo,headers=headers)
		entries=json.loads(response_body)
		prog = 1
		progress = eval("xbmcgui."+typeload+"()")
		progress.create('Carregando...')
		progress.update(0, "Carregando...")
		for entry in entries:
			#ST(entry['seasons'])
			try:
				if (progress.iscanceled()): break
			except:
				pass
			progtotal = int( 100*prog/(len(entries)) )
			progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
			prog+=1
			#titley = re.findall('(.+) \((\d+)\)', entry)
			meta = mg.get_tvshow_details(title="", tmdb_id=str(entry['show']['ids']['tmdb']), ignore_cache=MUcache, lang=MUlang)
			try:
				xx.AddDir(entry['show']['title'], str(entry['show']['ids']['tmdb']), "trakt."+whereto, isFolder=Play[0], IsPlayable=Play[1], dados={'meta': meta[-1]})
			except:
				pass
		progress.close()
	except:
		xx.AddDir("Trakt não configurado", "", "ReloadSkin", isFolder=False)
def ListMovies(elo='https://api.trakt.tv/users/'+Ctrakt+'/watchlist/movies/added',typeload = "DialogProgress"):
	trak = xx.traktM()
	headers = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': '888a9d79a643b0f4e9f58b5d4c2b13ee6d8bd584bc72bff8b263f184e9b5ed5d'}
	response_body = xx.OpenURL(elo,headers=headers)
	#response_body = xx.OpenURL("https://api.themoviedb.org/3/watch/providers/movies?api_key=bd6af17904b638d482df1a924f1eabb4&language=en-US&watch_region=AU")
	entries=json.loads(response_body)
	#ST(entries)
	prog = 1
	progress = eval("xbmcgui."+typeload+"()")
	progress.create('Carregando...')
	progress.update(0, "Carregando...")
	for entry in entries:
		if (progress.iscanceled()): break
		progtotal = int( 100*prog/(len(entries)) )
		progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
		prog+=1
		try:
			mm = mg.get_tmdb_details(tmdb_id=str(entry["movie"]["ids"]["tmdb"]), imdb_id="", tvdb_id="", title="", year="", media_type="movies", preftype="", manual_select=False, ignore_cache=False, lang=MUlangM)
			pc = 1 if str(mm["tmdb_id"]) in trak else None
			#pc = 0
			#ST(mm)
			#xx.AddDir(str(entry['id']), "plugin://plugin.video.elementum/library/movie/play/"+str(entry['id'])+"?doresume=true", "PlayUrl", isFolder=False, IsPlayable=True, dados={'mmeta': mm})
			xx.AddDir("", str(entry["movie"]["ids"]["tmdb"]), "tmdb.Opcoes", isFolder=False, IsPlayable=True, dados={'mmeta': mm, 'pc': pc})
		except:
			pass
		#break
def Shows():
	import trtv
	meta = eval(dados)["meta"]
	imdb = meta["imdbnumber"]
	id = trtv.RetId(imdb)
	#ST(id)
	#RetId
	if id:
		xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Play[/COLOR])", id, "trtv.SeasonsPlay", isFolder=True, dados={'meta': meta})
		if cDirtrtvDown:
			xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Download[/COLOR])", id, "trtv.Seasons", isFolder=True, dados={'meta': meta})
		
	xx.AddDir(meta["TVShowTitle"]+" ([COLOR red]Torrents[/COLOR])", meta["tmdb_id"], "trakt.Seasons", isFolder=True, dados={'meta': meta})
	if CexternalUrl:
		xx.AddDir(meta["TVShowTitle"]+" ([COLOR red]Url[/COLOR])", meta["tmdb_id"], "trakt.SeasonsUrl", isFolder=True, dados={'meta': meta})
	if id:
		if CtraktAuth:
			xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Play Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNext", isFolder=False, IsPlayable=True, dados={'meta': meta, 'trtv': id})
			xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Download Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNextDownload", isFolder=False, IsPlayable=True, dados={'meta': meta, 'trtv': id})
	return
	#options = []
	#options.append('Busca série em trailers.to')
	#options.append('Elementum')
	#sel = xbmcgui.Dialog().contextmenu(options)
	#if sel == 0:
	try:
		mdb = xx.OpenURL('http://api.themoviedb.org/3/tv/'+url+'?api_key=bd6af17904b638d482df1a924f1eabb4&language=en&append_to_response=external_ids')
		mdbj = json.loads(mdb)
		imdb = mdbj["external_ids"]["imdb_id"]
		#ST(imdb)
		#trtv = xx.OpenURL("https://trailers.to/en/popular/movies-tvshows-collections?q="+quote_plus(mdbj["name"]))
		q = re.sub('[^A-Za-z0-9] +', ' ', mdbj["name"])
		q = re.sub('\-', '', q)
		if "premiered" in meta:
			year = re.sub('(\d{4}).+', r'+\1', meta["premiered"])
		else:
			year = ""
		#ST(year)
		try:
			git = eval(xx.OpenURL("https://raw.githubusercontent.com/D4anielCB/cb.rep/master/trtv/tvshows.txt"))
			#ST(git[imdb])
			tvshow=[git[imdb]]
		except:
			trtv = xx.OpenURL(Cproxy + "https://trailers.to/en/quick-search?q="+quote_plus(q)+year)
			#ST(trtv)
			tvshow = re.compile("\/en\/tvshow\/(\d+)").findall(trtv)
		if tvshow:
			xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Play[/COLOR])", tvshow[0], "trtv.SeasonsPlay", isFolder=True, dados={'meta': meta})
			if cDirtrtvDown:
				xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Download[/COLOR])", tvshow[0], "trtv.Seasons", isFolder=True, dados={'meta': meta})
		elif len(trtv) < 80:
			xx.AddDir("Busca Trailers.to indisponível, usar Google", mdb, "google.BuscaTrtvTvshow", isFolder=True, dados={'meta': meta})
		else:
			xx.AddDir("Indisponível em Trailers.to", "", "", isFolder=False)
	except:
		xx.AddDir("Trailers.to pode estar offline", "", "", isFolder=False)
	dados2 = eval(dados)
	#xx.AddDir(meta["TVShowTitle"]+" (Torrents)", tvshow[0], "trtv.Seasons", isFolder=True, dados={'meta': meta})
	try:
		xx.AddDir(meta["TVShowTitle"]+" ([COLOR red]Torrents[/COLOR])", meta["tmdb_id"], "trakt.Seasons", isFolder=True, dados={'meta': meta})
		if CexternalUrl:
			xx.AddDir(meta["TVShowTitle"]+" ([COLOR red]Url[/COLOR])", meta["tmdb_id"], "trakt.SeasonsUrl", isFolder=True, dados={'meta': meta})
	except:
		pass
	if CtraktAuth:
		try:
			if tvshow:
				xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Play Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNext", isFolder=False, IsPlayable=True, dados={'meta': meta})
				xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Download Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNextDownload", isFolder=False, IsPlayable=True, dados={'meta': meta})
		except:
			pass
def Seasons(tororurl="trakt.Episodes"):
	dados2 = eval(dados)["meta"]
	trak = xx.traktT(dados2["imdbnumber"])
	link = xx.OpenURL('https://api.themoviedb.org/3/tv/'+url+'?api_key=bd6af17904b638d482df1a924f1eabb4')
	entries=json.loads(link)
	#ST(entries)
	for season in entries["seasons"]:
		try:
			mmm = mg.get_tvshow_details(title="",tmdb_id=url, ignore_cache=MUcache, lang=MUlang)
			metasea=xx.mergedicts(mmm[-1],mmm[season['season_number']])
			pc = 1 if season['season_number'] in trak else None
			xx.AddDir(metasea["name"], str(season['season_number']), tororurl, isFolder=True, dados={'meta': metasea, 'pc': pc})
		except:
			pass
#def Episodes(playordownload="trakt.PlayTraktDirect"):
def Episodes(tororurl="PlayUrl"):
	#from datetime import datetime
	#today = datetime.timestamp( datetime.now() )
	dados2 = eval(dados)
	#ST(dados2)
	#season = dados2["season"]
	lastepisode = LastEpisode(dados2["meta"]["imdbnumber"])
	trak = xx.traktS()
	link = xx.OpenURL('https://api.themoviedb.org/3/tv/'+dados2['meta']['tmdb_id']+'/season/'+url+'?api_key=bd6af17904b638d482df1a924f1eabb4')
	entries=json.loads(link)
	#ST(entries)
	#return
	prog = 1
	progress = xbmcgui.DialogProgress()
	progress.create('Carregando...')
	progress.update(0, "Carregando...")
	for entry in entries["episodes"]:
		try:
			#epidate = entry['air_date'].split("-")
			#timesepi = datetime.timestamp(  datetime(int(epidate[0]), int(epidate[1]), int(epidate[2]))  ) 
			#ST(entry['air_date'].split("-"))
			#ST(str(entry["episode_number"]) + " - " +str(today - timesepi),"1")
			progtotal = int( 100*prog/(len(entries["episodes"])) )
			progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
			prog+=1
			if (progress.iscanceled()): break
			pc = 1 if dados2['meta']['tmdb_id']+url+str(entry["episode_number"]) in trak else None
			play = "plugin://plugin.video.elementum/library/show/play/"+dados2['meta']["tmdb_id"]+"/"+url+"/"+str(entry["episode_number"])
			xx.AddDir( "" , play, tororurl, isFolder=False, IsPlayable=True, dados={'meta': dados2['meta'], 'season': url, 'episode': str(entry["episode_number"]), 'pc': pc})
		except:
			pass
		if lastepisode[0] == entry["season_number"] and lastepisode[1] == entry["episode_number"]:
			break
	progress.close()
#----------------------------------------
def PlayUrl():
	d = xbmcgui.Dialog().input("Digite a URL externa")
	if d:
		xx.PlayUrl("", d, srt=True)
#----------------------------------------
def PlayTrakt():
	if not CtraktAuth:
		xx.NF("Trakt não configurado!")
		return
	d = xbmcgui.Dialog().yesno("CubeTor", "Marcar como visto?")
	if not d:
		return
	try:
		values = """
		  {
			"movies": [
			  {
				"ids": {
				  "tmdb": %s
				}
			  }
			]
		  }
		"""
		values2 = values % (url)
		#ST(values)
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'ec2a1e688607858f031a99c2c4966b3dfd2c0e86ea48582e2ec97b9f06fd5882'}
		request = Request('https://api.trakt.tv/sync/history', data=values2.encode('utf-8'), headers=headers)

		response_body = urlopen(request).read()
		xx.NF("Marcado como visto!")
	except:
		xx.NF("Erro")
	#ST(response_body)
def PlayTrakt_naousado(): #antigo
	global url
	d = xbmcgui.Dialog().yesno("CubeTor", "Marcar como visto?")
	if not d:
		return
	url = "https://github.com/D4anielCB/cb.rep/raw/master/trakt.mp4"
	dados2 = eval(dados)
	RP = '{0}?mode=PlayUrl&url={1}&dados={2}&url=https://github.com/D4anielCB/cb.rep/raw/master/trakt.mp4'.format(sys.argv[0], quote_plus(url), quote_plus(str(dados2)))
	xbmc.executebuiltin('PlayMedia("'+RP+'")')
	#xx.PlayUrl("", "https://github.com/D4anielCB/cb.rep/raw/master/trakt.mp4")
#----------------------------------------
def LastEpisode(id):
	try:
		headers = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': '888a9d79a643b0f4e9f58b5d4c2b13ee6d8bd584bc72bff8b263f184e9b5ed5d'}
		response_body = xx.OpenURL('https://api.trakt.tv/shows/'+id+'/last_episode',headers=headers)
		j=json.loads(response_body)
		return [j["season"],j["number"]+1]
	except:
		return [0,0]
#----------------------------------------
def ST(x="", o="w"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]) or type(x) == type(set([''])):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		y = str(str(x).encode("utf-8"))
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, o)
	file.write(y+"\n"+str(type(x)))
	file.close()
#-----------------------------------------