# -*- coding: utf-8 -*-
import sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, math, html, xbmcvfs
from urllib.parse import urlparse, quote_plus
from urllib.request import urlopen, Request
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

def CRsession(req,session,force=False):
	import requests
	if force==True:
		try:
			url = 'https://api.crunchyroll.com/start_session.1.json'
			#headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'}
			myobj = {'device_id': '35yuv973-KODI-nh6i-69l8-81m0p580id2j', 'device_type': 'com.crunchyroll.windows.desktop', 'access_token': 'LNDJgOit5yaRIWN'}
			x = requests.post(url, data = myobj)
			j=json.loads(x.text)
			Addon.setSetting("crsession", j['data']['session_id'])
			return CRsession(req,j['data']['session_id'],False)
		except:
			return "error"
	else:
		result = common.OpenURL(req+"&session_id="+session)
		resultj = json.loads(result)
		if resultj['error']:
			if 'bad_session' in resultj['code']:
				return CRsession(req,session,True)
			else:
				return resultj
			#return "erro"
		else:
			return resultj			
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
def AddFav(): #537
	data = {'cr': url, "tmdb": logos, 'col_id': info, "season": background }
	sf = common.SaveFile(data, 'col_id',  "crunchyfav", title="")
	if sf:
		xbmc.sleep(1000)
		xbmc.executebuiltin('reloadskin')	
# -----------------------------
def opcoes(): #514
	sel = xbmcgui.Dialog().yesno('CubePlay', 'O que fazer?','Play','Abir episódios',5000)
	if sel == False: #play
		PlayNextEpi()
	else:
		RP = '{0}?mode=533&url={1}&background={2}&metah={3}&info={4}'.format(sys.argv[0], quote_plus(url), quote_plus(background), quote_plus(metah), quote_plus(info))
		xbmc.executebuiltin('ActivateWindow(10025,"'+RP+'")')
def ListFavCRPlay(): #538
	if not Ctrakt:
		return
	file = os.path.join(addon_data_dir, "crunchyfav.txt")
	favList = common.ReadList(file)
	i = 0
	for ids in favList:
		mmm = mg.get_tvshow_details(title="",tmdb_id=ids["tmdb"], ignore_cache=MUcache, lang=MUlang)
		metasea=xx.mergedicts(mmm[-1],  mmm[ int( ids["season"] )] )
		metasea['mediatype'] = "episode"
		xx.AddDir2(mmm[-1]["TVShowTitle"], ids["cr"], 541, "", "crunchyfav", info=ids["col_id"], isFolder=False, IsPlayable=True, background=ids["season"], metah=metasea, index=i)
		i+=1
def ListFavCR(): #539
	file = os.path.join(addon_data_dir, "crunchyfav.txt")
	favList = common.ReadList(file)
	i = 0
	for ids in favList:
		mmm = mg.get_tvshow_details(title="",tmdb_id=ids["tmdb"], ignore_cache=MUcache, lang=MUlang)
		metasea=xx.mergedicts(mmm[-1],  mmm[ int( ids["season"] )] )
		#xx.AddDir2("["+ids["season"]+"] "+mmm[-1]["TVShowTitle"], ids["cr"], 535, "", "crunchyfav", info=ids["col_id"], isFolder=False, IsPlayable=True, background=ids["season"], metah=metasea, index=i)
		xx.AddDir2(mmm[-1]["TVShowTitle"], ids["cr"], 533, "", metasea["tmdb_id"], info=ids["col_id"], isFolder=True, background=ids["season"], metah=metasea, index=i)
		i+=1
# -----------------------------
def Crunchy(): #530
	xx.AddDir("------------Adicionar Anime------------" , "", 531, isFolder=False)
	file = os.path.join(addon_data_dir, "crunchy.txt")
	favList = common.ReadList(file)
	index = 0
	for ids in favList:
		try:
			mmm = mg.get_tvshow_details(title="",tmdb_id=str(ids['tmdb']), ignore_cache=MUcache, lang=MUlang)
			#ST(mmm)
			xx.AddDir2(mmm[-1]['TVShowTitle'], str(ids['cr']), 532, "", "crunchy", info="", isFolder=True, background=mmm[-1]["tmdb_id"], metah=mmm[-1], index=index)
			
		except:
			pass
		index+=1	
# -----------------------------		
def PlayNextEpi(): #535
	lista = CRsession("https://api.crunchyroll.com/list_media.0.json?series_id="+url+"&limit=200",crsession)
	meta = eval(metah)
	trak = xx.traktS()
	E = 1
	totalepis = 0
	for l in lista['data']:
		if info == l['collection_id']:
			totalepis+=1
	for l in lista['data']:
		if info == l['collection_id']:
			play = "plugin://plugin.video.crunchyroll/?plotoutline=1&tvshowtitle=D&aired=2&episode_id="+l['media_id']+"&series_id=2&duration=1&collection_id=2&plot=.&episode=623251&thumb=g&title=D&fanart=g&premiered=2&mode=videoplay&playcount=0&status=Continuing&season=0&studio=T&genre=anime"
			pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(int(E)) in trak else None
			if pc == None:
				NF( "Epi. "+str(E)+"/"+ str(totalepis) )
				xx.PlayUrl("", play, epi=str(E))
				return
			E+=1
	NF("Todos episódios assistidos")
			
def ListSeason(): #532
	lista = CRsession("https://api.crunchyroll.com/list_collections.0.json?series_id="+url,crsession)
	#ST(lista)
	mmm = mg.get_tvshow_details(title="",tmdb_id=background, ignore_cache=MUcache, lang=MUlang)
	collection = []
	reseason = str(lista['data'])
	for l in lista['data']:
		#if not "'season': '1'" in str(lista['data']) and "'season': '0'" in reseason and not "Dub" in l['name']:
		if not "'season': '1'" in reseason and "'season': '0'" in reseason:
			collection.append(["1", l['collection_id'], l['name'] ])
		else:
			if 0 in mmm and l['season']=="0":
				collection.append(["0", l['collection_id'], l['name'] ])
			elif int(l['season']) > 1:
				collection.append([l['season'], l['collection_id'], l['name'] ])
			else:
				collection.append(["1", l['collection_id'], l['name'] ])
			#collection[l['season']] = l['collection_id']
	#ST(0 in mmm)
	for s in collection:
		metasea=xx.mergedicts(mmm[-1],mmm[int(s[0])])
		xx.AddDir2("["+s[0]+"] "+s[2], url, 533, "", metasea["tmdb_id"], info=s[1], isFolder=True, background=s[0], metah=metasea)
	xx.AddDir("---------- Autoplay ----------" , "", 40, isFolder=False)
	for s in collection:
		metasea=xx.mergedicts(mmm[-1],mmm[int(s[0])])
		metasea['mediatype'] = "episode"
		#ST(metasea)
		xx.AddDir2("["+s[0]+"] "+metasea['TVShowTitle'], url, 535, metasea['tmdb_id'], metasea['tmdb_id'], info=s[1], isFolder=False, IsPlayable=True, background=s[0], metah=metasea)
	xx.AddDir("---------- Corrigir Temporada ----------" , "", 40, isFolder=False)
	for s in collection:
		metasea=xx.mergedicts(mmm[-1],mmm[int(s[0])])
		xx.AddDir2("["+s[0]+"] "+s[2], url, 536, "", metasea['tmdb_id'], info=s[1], isFolder=True, background=s[0], metah=metasea)
#-----------------------------------------
def ListEpi(): #533
	lista = CRsession("https://api.crunchyroll.com/list_media.0.json?series_id="+url+"&limit=200",crsession)
	#ST(lista)
	meta = eval(metah)
	trak = xx.traktS()
	prog = 1
	progress = xbmcgui.DialogProgress() 
	progress.create('Carregando...')
	progress.update(0, "Carregando...")
	E = 1
	#ST()
	for l in lista['data']:
		if info == l['collection_id']:
			progtotal = int( 100*prog/( meta["episode_count"]) )
			progress.update(progtotal, "Só o primeiro acesso que demora\n"+str(progtotal)+" %")
			prog+=1
			if (progress.iscanceled()): break
			play = "plugin://plugin.video.crunchyroll/?plotoutline=1&tvshowtitle=D&aired=2&episode_id="+l['media_id']+"&series_id=2&duration=1&collection_id=2&plot=.&episode=623251&thumb=g&title=D&fanart=g&premiered=2&mode=videoplay&playcount=0&status=Continuing&season=0&studio=T&genre=anime"
			try:
				pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(int(E)) in trak else None
			except:
				pc = None
			xx.AddDir2("" ,play, 3, "", "",  isFolder=False, IsPlayable=True, background=str(meta['season_number']), metah=meta, episode=str(E), playcount=pc)
			E+=1
			#except:
				#AddDir( "[COLOR]"+l["name"]+"[/COLOR] - "+str(l["episode_number"]) , "", 40, isFolder=False)
	progress.close()	
def AddtoList(): #531
	#AddDir("Reload" , "", 40, isFolder=False)
	q = quote_plus(xbmcgui.Dialog().input("Digite o anime:") )
	google = common.OpenURL("https://www.google.com/search?q="+q+"+crunchyroll")
	googlere = re.compile("url\=http.+?crunchyroll.com\/.+?\/([^\&]+)").findall(google)
	try:
		if not "/" in googlere[0]:
			google = googlere[0]
		else:
			NF("Não encontrado")
			return
	except:
		google = ""
	crqj = CRsession("https://api.crunchyroll.com/autocomplete.0.json?media_types=anime&q="+q,crsession)
	croption1 = []
	croption2 = []
	if not crqj['data']:
		crqj = CRsession("https://api.crunchyroll.com/autocomplete.0.json?media_types=anime&q="+google,crsession)
	#ST(crqj['data'])
	if not crqj['data']:
		NF("Não encontrado!")
		return
	for x in crqj['data']:
		croption1.append(x['series_id'])
		croption2.append(x['name'])
	d = 0
	if len(croption2) > 1:
		d = xbmcgui.Dialog().select("Escolha o anime no Crunchyroll:", croption2)
	if d==-1: return
	#ST(   ) #
	tmid = common.OpenURL("https://api.themoviedb.org/3/search/tv?api_key=bd6af17904b638d482df1a924f1eabb4&language=en&query="+ quote_plus(  re.sub(' ?(\(.+)', "", crqj['data'][d]['name'] )  ) )
	tmdij = json.loads(tmid)
	#ST(tmdij)
	if not tmdij['results']:
		NF("Não encontrado")
		return
	tmdboption1 = []
	tmdboption2 = []
	#tmdij = {"page":1,"results":[{"backdrop_path":"/3ILMlmC30QUnYkY3XEBOyJ82Dqu.jpg","first_air_date":"2016-04-03","genre_ids":[10765,10759,35,16],"id":65930,"name":"Boku no Hero Academia","origin_country":["JP"],"original_language":"ja","original_name":"","overview":"Devido a um fenómeno desconhecido, cerca de 80% da população possui \"Singularidades”, isto é, super-poderes. No entanto, a existência deste poderes levou a um aumento exponencial da taxa de criminalidade e obrigou os mais corajosos a entra em acção, utilizando os seus poderes para o bem e tornando-se super-heróis. Desde pequeno, Midoriya Izuku sonhava ser um destes super-heróis e seguir as pisadas do seu ídolo, All Might. Contudo, ainda muito jovem, Izuku descobre que não possui uma Singularidade e que, por isso, não poderá ser um herói. Não deixando que isso o impeça, Izuku está determinado a entrar em Yuuei, a melhor escola de super-heróis do Japão, apesar de ninguém o levar a sério. Mas poderá um fatídico encontro com o seu grande ídolo mudar o seu destino?","popularity":89.365,"poster_path":"/mWHCII5OWHx5pRSN2VYYLvT8DbB.jpg","vote_average":8.9,"vote_count":2690}],"total_pages":1,"total_results":1}
	for x in tmdij["results"]:
		tmdboption1.append(x['id'])
		try:
			tmdboption2.append(x['name']+ " ("+ x["first_air_date"][2]+x["first_air_date"][3]+")")
		except:
			tmdboption2.append(x['name'])
	d2 = 0
	if len(tmdboption2) > 1:
		d2 = xbmcgui.Dialog().select("Escolha o anime no tmdb:", tmdboption2)
	if d2==-1: return
	data = {"cr": croption1[d], "tmdb": tmdboption1[d2]}
	common.SaveFile(data,"cr","crunchy",tmdboption2[d2])
	xbmc.executebuiltin("Container.Refresh()")
	xbmc.sleep(1000)
	xbmc.executebuiltin('reloadskin')
#----------------------------------------
def CorrigirTemp(): #536
	#AddDir("Reload" , "", 40, isFolder=False)
	meta = eval(metah)
	mmm = mg.get_tvshow_details(title="",tmdb_id=meta['tmdb_id'], ignore_cache=MUcache, lang=MUlang)
	cor = []	
	cor2 = []	
	for s in mmm:
		if 'name' in mmm[s]:
			cor.append(mmm[s]['name'])
			cor2.append(str(s))
	d = xbmcgui.Dialog().select("Escolha o temporada correta: "+name, cor)
	if d == -1: return
	lista = CRsession("https://api.crunchyroll.com/list_collections.0.json?series_id="+url,crsession)
	tempcorreta=cor2[d]
	#ST(cor2[d])
	#mmm = mg.get_tvshow_details(title="",tmdb_id=background, ignore_cache=MUcache, lang=MUlang)
	collection = []
	reseason = str(lista['data'])
	for l in lista['data']:
		#if not "'season': '1'" in str(lista['data']) and "'season': '0'" in reseason and not "Dub" in l['name']:
		if info == l['collection_id']:
			collection.append(["1", l['collection_id'], l['name'] ])
	#ST(collection)
	for s in collection:
		metasea=xx.mergedicts(mmm[-1],mmm[int(tempcorreta)])
		xx.AddDir2("["+tempcorreta+"] "+s[2], url, 533, "", logos, info=s[1], isFolder=True, background=tempcorreta, metah=metasea)
	xx.AddDir("---------- Autoplay ----------" , "", 40, isFolder=False)
	for s in collection:
		metasea=xx.mergedicts(mmm[-1],mmm[int(tempcorreta)])
		metasea['mediatype'] = "episode"
		#ST(metasea)
		xx.AddDir2("["+tempcorreta+"] "+metasea['TVShowTitle'], url, 535, metasea['tmdb_id'], metasea['tmdb_id'], info=s[1], isFolder=False, IsPlayable=True, background=tempcorreta, metah=metasea)
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
#----------------------------------------	
def NF(x, t=5000):
	xbmc.executebuiltin("Notification({0}, {1}, {3}, {2})".format(AddonName, str(x), icon, t))
