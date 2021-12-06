# -*- coding: utf-8 -*-
import xbmc
import sys, xbmcplugin, xbmcgui, xbmcaddon, os, json, hashlib, re, unicodedata, math, xbmcvfs
import shutil
from urllib.parse import urlparse, quote_plus, unquote, urlencode
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

Cproxy = "http://cbplay.000webhostapp.com/nc/nc.php?u="

CtraktAuth = Addon.getSetting("CtraktAuth") if Addon.getSetting("CtraktAuth") != "" else ""

MUlang = "pt-BR" if Addon.getSetting("MUlang") == "1" else "en"
MUlangM = "pt-BR" if Addon.getSetting("MUlangM") == "1" else "en"
MUcache = True if Addon.getSetting("MUcache") == "true" else False
MUcacheEpi = True if Addon.getSetting("MUcacheEpi") == "true" else False
MUfanArt = True if Addon.getSetting("MUfanArt") == "true" else False

Ctor = True if Addon.getSetting("Ctor") == "true" else False

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import xx, common

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
def PeerSeed(url2):
	import html
	try:
		link = quote_plus(html.unescape(url2))
		seeds = common.OpenURL("https://checker.openwebtorrent.com/check?magnet="+link, ssl=True)
		j = json.loads(seeds)
	except:
		j = {"error": "nao carregou"}
	return j
#-----------------------------------------
def BuscaTvShowsPre():
	q = xbmcgui.Dialog().input("O que busca? (Séries)")
	q = re.sub('^(s.rie(s)?|tvshow(s)?) ?', '', q, flags=re.IGNORECASE)
	q = re.sub(' ?(s.rie(s)?|tvshow(s)?)$', '', q, flags=re.IGNORECASE)
	if not q:
		RP = "plugin://plugin.video.CubeTor/?mode=&url="
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
		return
	RP = "plugin://plugin.video.CubeTor/?mode=google.BuscaTvShows&url="+quote_plus(q)
	xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
def BuscaTvShows():
	link = xx.OpenURL("http://api.themoviedb.org/3/search/tv?api_key=bd6af17904b638d482df1a924f1eabb4&language=en&query="+quote_plus(url))
	entries=json.loads(link)
	#ST(entries)
	#mmm = mg.get_tvshow_details(title="",tmdb_id=url, ignore_cache=MUcache, lang=MUlang)
	progress = xbmcgui.DialogProgress()
	progress.create('Carregando Séries...')
	progress.update(0, "Carregando...")
	prog = 1
	progress.close()
	for entry in entries['results']:
		#ST(entry)
		if (progress.iscanceled()): break
		progtotal = int( 100*prog/len(entries['results']) )
		progress.update(progtotal, str(progtotal)+" %")
		prog+=1
		try:
			mmm = mg.get_tvshow_details(title="",tmdb_id=str(entry["id"]), ignore_cache=MUcache, lang=MUlang)
			#xx.AddDir(str(entry['id']), "plugin://plugin.video.elementum/library/movie/play/"+str(entry['id'])+"?doresume=true", "PlayUrl", isFolder=False, IsPlayable=True, dados={'mmeta': mm})
			xx.AddDir(mmm[-1]["TVShowTitle"], mmm[-1]["tmdb_id"], "trakt.Shows", isFolder=True, dados={'meta': mmm[-1]})
		except:
			pass
#-----------------------------------------
def BuscaFilmesPre():
	q = xbmcgui.Dialog().input("Se quiser colocar o ano faça dessa forma: Titanic, 1997")
	q = re.sub('^(filme(s)?|movie(s)?) ?', '', q, flags=re.IGNORECASE)
	q = re.sub(' ?(filme(s)?|movie(s)?)$', '', q, flags=re.IGNORECASE)
	#q = "Mortal Kombat, 2021"
	if not q:
		RP = "plugin://plugin.video.CubeTor/?mode=&url="
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
		return
	RP = "plugin://plugin.video.CubeTor/?mode=google.BuscaFilmes&url="+quote_plus(q)
	xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
	#q = "Mortal Kombat"
def BuscaFilmes():
	yearre = re.compile(", (\d{4})$").findall(url)
	query = quote_plus(re.sub(', (\d{4})$', '', url))
	if yearre:
		year="&year="+yearre[0]
	else:
		year=""
	#ST("http://api.themoviedb.org/3/search/movie?api_key=bd6af17904b638d482df1a924f1eabb4&language=pt-br&query="+query+year)
	link = xx.OpenURL("http://api.themoviedb.org/3/search/movie?api_key=bd6af17904b638d482df1a924f1eabb4&language=pt-br&query="+query+year)
	entries=json.loads(link)
	progress = xbmcgui.DialogProgress()
	progress.create('Carregando Filmes...')
	progress.update(0, "Carregando...")
	prog = 1
	trak = xx.traktM()
	for entry in entries['results']:
		if (progress.iscanceled()): break
		progtotal = int( 100*prog/len(entries['results']) )
		progress.update(progtotal, str(progtotal)+" %")
		prog+=1
		try:
			mm = mg.get_tmdb_details(tmdb_id=str(entry['id']), imdb_id="", tvdb_id="", title="", year="", media_type="movies", preftype="", manual_select=False, ignore_cache=False, lang=MUlangM)
			pc = 1 if str(mm["tmdb_id"]) in trak else None
			#xx.AddDir(str(entry['id']), "plugin://plugin.video.elementum/library/movie/play/"+str(entry['id'])+"?doresume=true", "PlayUrl", isFolder=False, IsPlayable=True, dados={'mmeta': mm})
			xx.AddDir("", str(entry['id']), "tmdb.Opcoes", isFolder=False, IsPlayable=True, dados={'mmeta': mm, 'pc': pc})
		except:
			pass
	progress.close()
	if Ctor:
		xx.AddDir(url+" Dublado 1080p", quote_plus(url+" Dublado 1080p"), "google.BuscaCat", "", info="", isFolder=True, IsPlayable=False)
		xx.AddDir(url+" x265", quote_plus(url+" x265"), "google.BuscaCat", "", info="", isFolder=True, IsPlayable=False)
		xx.AddDir(url+" YTS", quote_plus(url+" YTS"), "google.BuscaCat", "", info="", isFolder=True, IsPlayable=False)
		xx.AddDir(url, quote_plus(url), "google.BuscaCat", "", info="", isFolder=True, IsPlayable=False)
#-----------------------------------------
def BuscaAllPre():
	q = xbmcgui.Dialog().input("Se quiser colocar o ano faça dessa forma: Titanic, 1997")
	#q = "chucky Movies"
	typere = re.compile(" ?(s.ries?|filmes?|tv ?show|movies?)$", re.IGNORECASE).findall(q)
	d = {'type':''}
	if typere:
		d = {'type': typere[0]}
	q = re.sub('^(filme(s)?|movie(s)?) ?', '', q, flags=re.IGNORECASE)
	q = re.sub(' ?(filme(s)?|movie(s)?)$', '', q, flags=re.IGNORECASE)
	q = re.sub('^(s.rie(s)?|tvshow(s)?) ?', '', q, flags=re.IGNORECASE)
	q = re.sub(' ?(s.rie(s)?|tvshow(s)?)$', '', q, flags=re.IGNORECASE)
	if q:
		RP = "plugin://plugin.video.CubeTor/?mode=google.BuscaAll&url="+quote_plus(q)+"&dados="+quote_plus(str(d))
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
def BuscaAll():
	dados2 = eval(dados)
	if re.compile("(s.ries?|tv ?shows?)", re.IGNORECASE).findall(dados2["type"]):
		BuscaTvShows()
	elif re.compile("(movies?|filmes?)", re.IGNORECASE).findall(dados2["type"]):
		BuscaFilmes()
	else:
		BuscaTvShows()
		BuscaFilmes()
#-----------------------------------------
def BuscaCat():
	try:
		google = xx.OpenURL("https://www.google.com/search?q="+url+"+torrent")
		googlere = re.compile(";url=([^\"]+)\&amp;ved\=").findall(google)
		progress = xbmcgui.DialogProgress()
		progress.create('Carregando...')
		progress.update(0, "Carregando...")
		prog = 1
		#ST(googlere)
		for links in googlere[:5]:
			if (progress.iscanceled()): break
			magnet = xx.OpenURL(links)
			magnetre = re.compile('magnet\:\?[^\'|"]+').findall(magnet)
			for link in magnetre:
				title = re.compile("dn=(.+?)(\&|$)").findall(link)
				if title:
					j = PeerSeed(link)
					if "seeds" in j:
						xx.AddDir(str(j["seeds"])+" / "+str(j["peers"])+" "+unquote(title[0][0]), link, "comando.PlayTorrents", iconimage, info=links, isFolder=False, IsPlayable=True)
					else:
						xx.AddDir(unquote(title[0][0]), link, "comando.PlayTorrents", iconimage, info=links, isFolder=False, IsPlayable=True)
			progtotal = int(100*prog/5)
			progress.update(progtotal, str(progtotal)+" %")
			prog+=1
		progress.close()
	except:
		xx.AddDir("Erro no servidor", "", "", iconimage, info="", isFolder=False, IsPlayable=True)
#----------------------------------------
def BuscaTrtvTvshow(type="episode"):
	meta = eval(dados)["meta"]
	mdb = json.loads(url)
	imdb = mdb["external_ids"]["imdb_id"]
	try:
		query = mdb["name"] +" "+ mdb["first_air_date"].split("-")[0]+" site:https://trailers.to/en/"+type
	except:
		query = mdb["name"] +" site:https://trailers.to/en/"+type
	try:
		link = xx.OpenURL("https://www.google.com/search?q="+quote_plus(query))
	except:
		xx.NF("Erro google " + type)
		if type=="episode":
			BuscaTrtvTvshow("tvshow")
		return
	entries = re.compile("url=(https?:\/\/trailers.to\/en\/"+type+"[^\&]+)", re.IGNORECASE).findall(link)
	prog = 1
	progress = xbmcgui.DialogProgress()
	progress.create('Procurando...')
	progress.update(0, "")
	for entry in entries:
		if (progress.iscanceled()): break
		try:
			progtotal = int(100*prog/len(entries))
			progress.update(progtotal, entry+"\n\n"+str(progtotal)+" %")
			prog+=1
			linksearch = xx.OpenURL(Cproxy + entry)
			tt = re.compile("https?...imdb.com\/title\/"+imdb, re.IGNORECASE).findall(linksearch)
			id = re.compile("\/en\/tvshow\/(\d+)", re.IGNORECASE).findall(linksearch)
			if tt and id:
				xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Play[/COLOR])", id[0], "trtv.SeasonsPlay", isFolder=True, dados={'meta': meta})
				if Addon.getSetting("cDirtrtvDown"):
					xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Download[/COLOR])", id[0], "trtv.Seasons", isFolder=True, dados={'meta': meta})
				if CtraktAuth:
					xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Play Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNext", isFolder=False, IsPlayable=True, dados={'meta': meta, 'trtv': id[0]})
					xx.AddDir(meta["TVShowTitle"]+" ([COLOR blue]Download Next[/COLOR])", meta["tmdb_id"], "trakt.ShowsNextDownload", isFolder=False, IsPlayable=True,  dados={'meta': meta, 'trtv': id[0]})
				progress.close()
				return
		except:
			pass
	if type=="episode":
		BuscaTrtvTvshow("tvshow")
def BuscaTrtvMovie(mdb):
	mdb = json.loads(mdb)
	imdb = mdb["external_ids"]["imdb_id"]
	try:
		query = mdb["title"] +" "+ mdb["release_date"].split("-")[0]+" site:https://trailers.to/en/movie"
	except:
		query = mdb["title"] +" site:https://trailers.to/en/movie"
	link = xx.OpenURL("https://www.google.com/search?q="+quote_plus(query))
	entries = re.compile("url=(https?:\/\/trailers.to\/en\/movie[^\&]+)", re.IGNORECASE).findall(link)
	ID = ""
	for entry in entries:
		try:
			linksearch = xx.OpenURL(Cproxy + entry)
			tt = re.compile("https?...imdb.com\/title\/"+imdb, re.IGNORECASE).findall(linksearch)
			id = re.compile("\/en\/movie\/(\d+)", re.IGNORECASE).findall(linksearch)
			if tt and id:
				ID = id[0]
				break
		except:
			pass
	return ID
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