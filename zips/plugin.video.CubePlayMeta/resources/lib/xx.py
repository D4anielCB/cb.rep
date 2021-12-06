# -*- coding: utf-8 -*-
import xbmc
#dbID = xbmc.getInfoLabel('ListItem.DBID')
#dbType = xbmc.getInfoLabel('ListItem.DBTYPE')
#filePath = xbmc.getInfoLabel('ListItem.FolderPath')
import sys, xbmcplugin, xbmcgui, xbmcaddon, os, json, hashlib, re, unicodedata, math, xbmcvfs
import shutil
from urllib.parse import urlparse, quote_plus, unquote
from urllib.request import urlopen, Request
import urllib.request, urllib.parse, urllib.error
import urllib.parse
from metadatautils import MetadataUtils
mg = MetadataUtils()
mg.tmdb.api_key = 'bd6af17904b638d482df1a924f1eabb4'

AddonID = 'plugin.video.CubePlayMeta'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
addonDir = Addon.getAddonInfo('path')
icon = os.path.join(addonDir,"icon.png")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cFonte1 = Addon.getSetting("cFonte1")
cFonte2 = Addon.getSetting("cFonte2")
cFonte3 = Addon.getSetting("cFonte3")

cTxt1 = Addon.getSetting("cTxt1")
cTxt2 = Addon.getSetting("cTxt2")
cTxt3 = Addon.getSetting("cTxt3")

DirM = Addon.getSetting("cDir")
DirB = Addon.getSetting("cDirB")
CEle = Addon.getSetting("cEle")

DirCount = Addon.getSetting("DirCount") if Addon.getSetting("DirCount") != "" else 0

MUlang = "pt-BR" if Addon.getSetting("MUlang") == "0" else "en"
MUcache = True if Addon.getSetting("MUcache") == "true" else False
MUcacheEpi = True if Addon.getSetting("MUcacheEpi") == "true" else False
MUfanArt = True if Addon.getSetting("MUfanArt") == "true" else False

Cat = Addon.getSetting("Cat") if Addon.getSetting("Cat") != "" else 0
Cat2 = Addon.getSetting("Cat2") if Addon.getSetting("Cat2") != "" else "0"
Cidi = Addon.getSetting("Cidi") if Addon.getSetting("Cidi") != "" else "0"

Ctrakt = Addon.getSetting("Ctrakt") if Addon.getSetting("Ctrakt") != "" else ""
CtraktAuth = Addon.getSetting("CtraktAuth") if Addon.getSetting("CtraktAuth") != "" else ""
CTraktResume = True if Addon.getSetting("CTraktResume") == "true" else False

Clista=["Sem filtro (Mostrar Todos)","Ação", "Animação", "Aventura", "Crime", "Comédia", "Documentário", "Drama", "Fantasia", "Ficção científica", "Mistério", "Romance", "Terror", 'Thriller']
CImdb=["nome","ano","vote"]
CImdb2=["Nome","Ano","Rating"]

#-----------------------------------------
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
# --------------  Trakt
def traktS():
	if not Ctrakt:
		return []
	try:
		headers1 = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': '888a9d79a643b0f4e9f58b5d4c2b13ee6d8bd584bc72bff8b263f184e9b5ed5d'}
		response_body = common.OpenURL('https://api.trakt.tv/users/'+Ctrakt+'/watched/shows',headers=headers1)
		j=json.loads(response_body)
		trak=[]
	except:
		return []
	for m in j:
		try:
			for Sea in m['seasons']:
				for epi in Sea['episodes']:
					trak.append(m['show']['ids']['imdb']+str(Sea['number'])+str(epi['number']))
		except:
			pass
	return trak	
def traktM():
	if not Ctrakt:
		return []
	headers1 = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': '888a9d79a643b0f4e9f58b5d4c2b13ee6d8bd584bc72bff8b263f184e9b5ed5d'}
	response_body = common.OpenURL('https://api.trakt.tv/users/'+Ctrakt+'/watched/movies',headers=headers1)
	j=json.loads(response_body)
	trak=[]
	for m in j:
		#ST(j)
		try:
			trak.append(str(m['movie']['ids']['imdb']))
		except:
			pass
	return trak
	
def TraktAuth():
	try:
		values = """
		  {
			"client_id": "bf937c524ef510ac9cf8b84207a30186cd9cbae32a6b98eab854eeadc807419b"
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
			"client_id": "bf937c524ef510ac9cf8b84207a30186cd9cbae32a6b98eab854eeadc807419b",
			"client_secret": "54b81cb9e635506d873d3c58172be2fb0d40af4dd6d3f7150355efe9f309f46e"
		  }
		"""
		values2 = values % (device_code)
		headers = {'Content-Type': 'application/json'}
		req = Request("https://api.trakt.tv/oauth/device/token", data=values2.encode('utf-8'), headers=headers)
		response_body = urlopen(req).read().decode("utf-8")
		entries=json.loads(response_body)
		token = entries["access_token"]
		Addon.setSetting("CtraktAuth", token )
		NF("Trakt configurado!")
	except:
		NF("Erro, refaça a configuração")
	setuser(token)
def setuser(token):
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'trakt-api-version': '2', 'trakt-api-key': 'bf937c524ef510ac9cf8b84207a30186cd9cbae32a6b98eab854eeadc807419b'}
		request = Request('https://api.trakt.tv/users/settings', headers=headers)
		response_body = urlopen(request).read()
		entries=json.loads(response_body)
		username = entries["user"]["username"]
		d = xbmcgui.Dialog().yesno("CubeTor", "Configurar como "+username)
		if not d: return
		Addon.setSetting("Ctrakt", username )
	except:
		pass
def TraktResumeS(dados="",S=0,E=0):
	import time
	dados2 = eval(dados)
	id = int(dados2["tmdb_id"])
	RS = 0
	#ST(dados2)
	if not CtraktAuth:
		return RS
	try:
		headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+CtraktAuth, 'trakt-api-version': '2', 'trakt-api-key': 'bf937c524ef510ac9cf8b84207a30186cd9cbae32a6b98eab854eeadc807419b'}
		request = Request('https://api.trakt.tv/sync/playback/episodes', headers=headers)
		response_body = urlopen(request).read()
		entries=json.loads(response_body)
		for entry in entries:
			try:
				if entry["type"] == "episode":
					if entry["episode"]["season"] == S and entry["episode"]["number"] == E:
					#if id == entry["movie"]["ids"]["tmdb"]:
						RS = entry["progress"]
					break
			except:
				pass
	except:
		RS = 0
	try:
		total = dados2["duration"]*int(RS)/100
		total = str(time.strftime("%H:%M:%S", time.gmtime(total*60)))
	except:
		total = str(RS)+"%"
	return [int(RS),str(RS), total]
#-----------------------------------------
def PlayUrl(name, url, iconimage=None, info='', sub='', epi=''):
	#global episode
	#if DirM in url:
		#sub=re.sub('\..{3}$', '.srt', url)
	#url = re.sub('\.mp4$', '.mp4?play', url)
	#url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	if metah:
		try:
			#ST(epi)
			#episode=epi
			metah2 = eval(metah)
			eInfo_ = mg.get_episode_details(metah2['tmdb_id'], SEAS(background), EPI(epi))
			eInfo = mergedicts(metah2,eInfo_)
			#ST(eInfo)
			if 'EpisodeTitle' in eInfo:
				eInfo["Title"]= eInfo['EpisodeTitle']
			else:
				eInfo['season'] = SEAS(background)
				eInfo['episode'] = EPI(epi)
				eInfo["Title"] = "Episode " + eInfo['episode']
			S=str(eInfo['season'])
			E=str(eInfo['episode'])		
			try:
				if CtraktAuth and CTraktResume:
					RSM = TraktResumeS(metah,int(S),int(E))
					#ST(RSM)
					if RSM[0] > 1:
						d = xbmcgui.Dialog().yesno("CubeTor", "Retomar de "+RSM[2]+"?")
						if d:
							listitem.setProperty('StartPercent', RSM[1])
			except:
				pass
			clearlogo=""
			if MUfanArt:
				#import random
				try:
					fanart = common.OpenURL("https://webservice.fanart.tv/v3/tv/"+eInfo['tvdb_id']+"?api_key=f8ba25de3d50ea5655f5b6bd78387878")
					fanartj = json.loads(fanart)
					#rand = random.randrange(0,len(fanartj["hdtvlogo"]))
					clearlogo = fanartj["hdtvlogo"][0]['url']
				except:
					pass
			#listitem.setArt({"poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'], "clearlogo": fanartj["hdtvlogo"][1]['url'] })
			listitem.setArt({"poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'], "clearlogo": clearlogo })
			eInfo.pop('cast', 1)
			#eInfo.pop('tmdb_id', 1)
			#eInfo['plot'] += "\nAired: " +Data(str(eInfo['premiered']))
			#try:
			#	eInfo['plot'] += u"\n[COLOR button_focus]Exibição:[/COLOR] " +Data(str(eInfo['premiered'])) if MUlang == "pt-BR" else "\nAired: " +Data(str(eInfo['premiered']))
			#except:
			#	pass
			eInfo['mediatype'] = "episode"
			#eInfo['genre'] = '[COLOR button_focus]S'+str(eInfo['season'])+'E'+str(eInfo['episode'])+'[/COLOR]: '+eInfo["TVShowTitle"]
			listitem.setInfo( "video",  eInfo )
		except:
			try:
				metah2 = eval(metah)
				metah2['Title'] = metah2['TVShowTitle']
				metah2['season'] = int(background)
				metah2['episode'] = int(episode)
				metah2['mediatype'] = "episode"
				#metah2['genre'] = '[COLOR button_focus]S'+str( SEAS(background) )+'E'+str( EPI(episode) )+'[/COLOR]'
				listitem.setInfo( "video", metah2 )
				#listitem.setInfo( type="Video", infoLabels= {'imdb_id': 'tt0078802'} )
			except:
				pass
		try:
			ids = json.dumps({u'tmdb': metah2['tmdb_id']})
			xbmcgui.Window(10000).setProperty('script.trakt.ids', ids)
		except:
			pass
	else:
		listitem.setInfo("Video", {"mediatype": "video", "Title": name, "Plot": info })
		#if iconimage is not None:
		#	try:
		#		listitem.setArt({'thumb' : iconimage})
		#	except:
		#		listitem.setThumbnailImage(iconimage)
	#if sub!='':
		#listitem.setSubtitles(['special://temp/example.srt', sub ])
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
#-----------------------------------------
def PlayUrl2(name, url, iconimage=None, info='', sub='', metah='', RS="0"):
	#container = dbID
	#ST(dbID)
	#return
	#url = re.sub('\.mp4$', '.mp4?play', url)
	#url = common.getFinalUrl(url)
	xbmc.log('--- Playing url2 "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	#listitem = xbmcgui.ListItem(path="D:\S\Shows\Under Pressure (2017)\SOBPRSAOS02E02.mp4")
	if RS != "0":
		listitem.setProperty('StartPercent', RS)
	if metah:
		#listitem.setArt({"thumb": metah['cover_url'], "poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
		#listitem.setArt({"poster": metah['art']['poster'], "banner": metah['art']['poster'], "fanart": metah['art']['fanart'] })
		metah.pop('cast', 1)
		metah.pop('castandrole', 1)
		metah.pop('art', 1)
		listitem.setInfo("video", metah)
		try:
			ids = json.dumps({u'tmdb': metah['tmdb_id']})
			xbmcgui.Window(10000).setProperty('script.trakt.ids', ids)
		except:
			pass
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	#if sub!='':
		#listitem.setSubtitles(['special://temp/example.srt', sub ])
	#if iconimage is not None:
		#try:
			#listitem.setArt({'thumb' : iconimage})
		#except:
			#listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
#-----------------------------------------
def AddDir2(name, url, mode, iconimage='', logos='', index="", move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', DL='', year='', metah={}, episode='', playcount=None): #add2
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'index': index, 'info': info, 'background': background, 'DL': DL, 'year': year, 'metah': metah, 'episode': episode, 'playcount': playcount, 'index': index}
	if metah:
		if background and episode:
			eInfo = mg.get_episode_details(metah['tmdb_id'], SEAS(background), EPI(episode), ignore_cache=MUcacheEpi, lang=MUlang)
			eInfo2 = mergedicts(metah,eInfo)
			#eInfo2['imagepi'] = eInfo2['imagepi'].replace("/original/","/w780/")
			#eInfo2['cover_url'] = eInfo2['cover_url'].replace("/original/","/w500/")
			#eInfo2['backdrop_url'] = eInfo2['backdrop_url'].replace("/original/","/w780/")
			eInfo2['playcount'] = 1 if playcount else 0
			eInfo2['mediatype'] = "episode"
			#eInfo2['userrating'] = eInfo2['rating']
			if 'EpisodeTitle' in eInfo2:
				#liz=xbmcgui.ListItem(DL+"[COLOR white]"+background+"x"+EPI(episode)+". "+eInfo2['EpisodeTitle']+"[/COLOR]")
				liz=xbmcgui.ListItem(DL+background+"x"+EPI(episode)+". "+eInfo2['EpisodeTitle'])
			else:
				liz=xbmcgui.ListItem(DL+background+"x"+EPI(episode)+". Episode "+EPI(episode))
			if ".jpg" in eInfo2['imagepi']:
				pass
				liz.setArt({"icon": eInfo2['imagepi'], "thumb": eInfo2['imagepi'], "poster": eInfo2['cover_url'], "banner": eInfo2['cover_url'], "fanart": eInfo2['backdrop_url'] })
			else:
				liz.setArt({"thumb": eInfo2['cover_url'], "poster": eInfo2['cover_url'], "banner": eInfo2['cover_url'], "fanart": eInfo2['backdrop_url'] })
			if "cast" in eInfo2:
				count = 0
				for value in eInfo2['cast']:
					for value2 in value:
						if 'thumbnail' in eInfo2['cast'][count]:
							eInfo2['cast'][count]['thumbnail']=eInfo2['cast'][count]['thumbnail'].replace("/original/","/w300/")
					count+=1
				liz.setCast(eInfo2['cast'])
			eInfo2.pop('cast', 1)
			eInfo2.pop('genre', 1)
			#eInfo2['genre'] = "b"
			#eInfo2['tagline'] = "a"
			liz.setInfo( "video", eInfo2 )
		else:
			#ST(1)
			liz=xbmcgui.ListItem(DL +""+name)
			#liz.setArt({"poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
			if "cast" in metah:
				liz.setCast(metah['cast'])
			metah.pop('cast', 1)
			if not 'mediatype' in metah:
				metah['mediatype'] = u'tvshow'
			metah['tagline'] = ""
			for i in metah['genre']:
				metah['tagline'] = i if metah['tagline'] == "" else metah['tagline'] + ", " + i
			#metah['tagline'] = i
			liz.setArt({"thumb": metah['cover_url'], "poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
			liz.setInfo("video", metah)
	else:
		liz = xbmcgui.ListItem(name)
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
		#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode == 96 and logos != "":
		liz.addContextMenuItems(items = [("Elementum", 'RunPlugin(plugin://plugin.video.elementum/library/movie/play/{0}?play&doresume=true)'.format(logos)) ])
	elif mode == 303:
		liz.addContextMenuItems(items = [("Excluir da lista", 'RunPlugin({0}?mode=305&logos={1})'.format(sys.argv[0], quote_plus(logos) ))])
	elif mode == 96:
		liz.addContextMenuItems(items = [("Excluir da lista", 'RunPlugin({0}?url={1}&mode=355&iconimage={2}&name={3}&index={4})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name), index))])
	elif (mode == 502 or mode == 504) and info:
		liz.addContextMenuItems(items = [('Adicionar ao fav.', 'RunPlugin({0}?url={1}&mode=507&background={2}&info={3})'.format(sys.argv[0], quote_plus(url), quote_plus(background), quote_plus(info))  )])
	elif mode == 521:
		liz.addContextMenuItems(items = [('Adicionar ao fav', 'RunPlugin({0}?url={1}&mode=524&info={2})'.format(sys.argv[0], quote_plus(url), quote_plus(info))  )])
	elif mode == 523:
		liz.addContextMenuItems(items = [('Remover dos fav'+str(index), 'RunPlugin({0}?url={1}&mode=511&index={2}&logos={3})'.format(sys.argv[0], quote_plus(url), index, quote_plus(iconimage))  )])
	elif mode == 504:
		liz.addContextMenuItems(items = [('Remover dos fav.', 'RunPlugin({0}?url={1}&mode=511&index={2}&logos={3})'.format(sys.argv[0], quote_plus(url), index, quote_plus(logos))  )])
	elif mode == 514:
		liz.addContextMenuItems(items = [( 'Excluir Anime', 'RunPlugin('+sys.argv[0]+'?url={1}&logos='+logos+'&mode=534&index='+str(index)+')')])
	elif mode == 541 and logos == "crunchyfav":
		liz.addContextMenuItems(items = [( 'Excluir Anime cr', 'RunPlugin('+sys.argv[0]+'?url={1}&logos='+logos+'&mode=534&index='+str(index)+')')])
	elif (mode == 533 or mode == 535) and logos:
		liz.addContextMenuItems(items = [('Adicionar ao fav. cr', 'RunPlugin({0}?url={1}&mode=537&background={2}&info={3}&logos={4})'.format(sys.argv[0], quote_plus(url), quote_plus(background), quote_plus(info), quote_plus(logos))  )])
	u = '{0}?{1}'.format(sys.argv[0], urllib.parse.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
# --------------------------------------------------
def mergedicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
def Data(x):
	x = re.sub('\d\d(\d+)\-(\d+)\-(\d+)', r'\3/\2/\1', x )
	return "[COLOR white]("+x+")[/COLOR]"
def EPI(x):
	x = re.sub('[0]+(\d+)', r'\1', x )
	return str(x)
def SEAS(x):
	x = re.sub('0(\d)', r'\1', x )
	return str(x)
def EPIz(x):
	if len(x) == 1:
		return "0"+x
	else:
		return x
def NF(text):
	xbmc.executebuiltin("Notification({0}, {1}, {3}, {2})".format(AddonName, str(text), icon, 1000))
# --------------------------------------------------
def AddDir(name, url, mode, iconimage='', logos='', index="", move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', DL='', year='', metah={}, episode='', playcount=None):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'index': index, 'info': info, 'background': background, 'DL': DL, 'year': year, 'metah': metah, 'episode': episode, 'playcount': playcount, 'index': index}
	if metah:
		if background and episode:
			mg = metahandlers.MetaData()
			#sInfo = mg.get_seasons(metah['TVShowTitle'], metah['imdbnumber'], [1])
			eInfo = mg.get_episode_meta(metah['TVShowTitle'], metah['imdbnumber'], SEAS(background), EPI(episode))
			#liz=xbmcgui.ListItem(DL+background+"."+EPI(episode)+" "+eInfo['title'] +" "+Data(eInfo['premiered'])+ " [COLOR blue]["+str(eInfo['rating'])+"][/COLOR]", iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			liz=xbmcgui.ListItem(DL+background+"x"+EPI(episode)+". "+eInfo['title'], iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			#liz.setRating("imdb", 0.1, 8940, False)
			liz.setArt({"thumb": eInfo['cover_url'], "poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'] })
			infoLabels = metah
			eInfo['userrating'] = eInfo['rating']
			eInfo['mediatype'] = u'movie'
			if playcount:
				eInfo['playcount'] = playcount
			else:
				eInfo.pop('playcount', 1)
			liz.setInfo( "video",  eInfo )
		else:
			metah['mediatype'] = u'movie'
			metah['Imdbnumber'] = metah['imdbnumber']
			metah['tagline'] = ""
			for i in metah['genre']:
				metah['tagline'] = i if metah['tagline'] == "" else metah['tagline'] + ", " + i
			if playcount:
				metah['playcount'] = playcount
			else:
				metah.pop('playcount', 1)
			liz=xbmcgui.ListItem(DL +""+name)
			liz.setArt({"poster": metah['art']['poster'], "banner": metah['art']['poster'], "fanart": metah['art']['fanart'] })
			count=0
			if "cast" in metah:
				count = 0
				for value in metah['cast']:
					for value2 in value:
						if 'thumbnail' in metah['cast'][count]:
							metah['cast'][count]['thumbnail']=metah['cast'][count]['thumbnail'].replace("/original/","/w300/")
					count+=1
				liz.setCast(metah['cast'])
			metah.pop('cast', 1)
			metah.pop('castandrole', 1)
			metah.pop('art', 1)
			liz.setInfo( "video", metah )
	else:
		liz = xbmcgui.ListItem(name)
		liz.setLabel(name)
		liz.setInfo("video", { "title": name, "Plot": info })
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos, "icon":  iconimage, "thumb": iconimage})
		#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode == 96 and logos != "":
		liz.addContextMenuItems(items = [("Elementum", 'RunPlugin(plugin://plugin.video.elementum/library/movie/play/{0}?play&doresume=true)'.format(logos)) ])
	elif mode == 303:
		liz.addContextMenuItems(items = [("Excluir da lista 1", 'RunPlugin({0}?mode=305&logos={1})'.format(sys.argv[0], quote_plus(logos) ))])
	elif mode == 96:
		liz.addContextMenuItems(items = [("Excluir da lista i="+ str(index), 'RunPlugin({0}?url={1}&mode=355&iconimage={2}&name={3}&index={4})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name), index))])
	u = '{0}?{1}'.format(sys.argv[0], urllib.parse.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
#----------------------------------------
def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])
#----------------------------------------
def ST(x="", o="w"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		try:
			y = str(x)
		except:
			y = str(str(x).encode("utf-8"))
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, o)
	file.write(y+"\n"+str(type(x)))
	file.close()