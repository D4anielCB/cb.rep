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
def AddFav(q=""): #524
	query = url if q == "" else q
	#tmid = common.OpenURL("https://api.themoviedb.org/3/search/tv?api_key=bd6af17904b638d482df1a924f1eabb4&language=en&query=asdsadsadasda&append_to_response=keywords,videos,credits,images,seasons")
	tmid = common.OpenURL("https://api.themoviedb.org/3/search/tv?api_key=bd6af17904b638d482df1a924f1eabb4&language=en&query="+quote_plus(query)+"&append_to_response=keywords,videos,credits,images,seasons")
	tmdij = json.loads(tmid)
	list = ["Buscar"]
	season = [""]
	ids = [""]
	if tmdij['results']:
		for j in tmdij['results']:
			title = j["name"] +" "+j["first_air_date"] 
			id = str( j['id'])
			tmid2 = common.OpenURL("https://api.themoviedb.org/3/tv/"+id+"?api_key=bd6af17904b638d482df1a924f1eabb4&language=en")
			tmdij2 = json.loads(tmid2)
			for x in tmdij2['seasons']:
				list.append("["+str(x["season_number"])+"] "+title)
				season.append(str(x["season_number"]))
				ids.append(id)
	if len(list) > 1:
		d = xbmcgui.Dialog().select("Escolha o anime", list)
	else:
		d = 0
	if d == -1: return
	if d == 0 or not tmdij['results']:
		d = xbmcgui.Dialog().input("Digite o anime")
		if d:
			AddFav(d)
	else:
		data = {'erai': url, "tmdb": ids[d], "season": season[d] }
		sf = common.SaveFile(data, 'erai',  "erai", title="")
		if sf:
			xbmc.sleep(1000)
			xbmc.executebuiltin('reloadskin')	
# -----------------------------
def ListAnimeMeta(): #520
	#AddDir("Reload" , "", 40, isFolder=False)
	#xx.AddDir("[B][Erai-Raws][/B]" , "", 522, isFolder=True)
	file = os.path.join(addon_data_dir, "erai.txt")
	favList = common.ReadList(file)
	i = 0
	for ids in favList:
		mmm = mg.get_tvshow_details(title="",tmdb_id=ids["tmdb"], ignore_cache=MUcache, lang=MUlang)
		metasea=xx.mergedicts(mmm[-1],  mmm[ int( ids["season"] )] )
		#xx.AddDir2("["+ids["season"]+"] "+mmm[-1]["TVShowTitle"], ids["cr"], 535, "", "crunchyfav", info=ids["col_id"], isFolder=False, IsPlayable=True, background=ids["season"], metah=metasea, index=i)
		xx.AddDir2("["+ids["season"]+"] "+mmm[-1]["TVShowTitle"], ids["erai"], 523, "erai", metasea["tmdb_id"], info="", isFolder=True, background=ids["season"], metah=metasea, index=i)
		i+=1
def retsitereai(action,anime): ############
	try:
		import requests
		url = 'https://www.erai-raws.info/wp-admin/admin-ajax.php'
		#q = {'anime-list':'shingeki-no-kyojin-the-final-season','error':'','m':'','p':0,'post_parent':'','subpost':'','subpost_id':'','attachment':'','attachment_id':0,'name':'','pagename':'','page_id':0,'second':'','minute':'','hour':'','day':0,'monthnum':0,'year':0,'w':0,'category_name':'','tag':'','cat':'','tag_id':'','author':'','author_name':'','feed':'','tb':'','paged':0,'meta_key':'','meta_value':'','preview':'','s':'','sentence':'','title':'','fields':'','menu_order':'','embed':'','category__in':[],'category__not_in':[],'category__and':[],'post__in':[],'post__not_in':[],'post_name__in':[],'tag__in':[],'tag__not_in':[],'tag__and':[],'tag_slug__in':[],'tag_slug__and':[],'post_parent__in':[],'post_parent__not_in':[],'author__in':[],'author__not_in':[],'ignore_sticky_posts':False,'suppress_filters':False,'cache_results':True,'update_post_term_cache':True,'lazy_load_term_meta':True,'update_post_meta_cache':True,'post_type':'','posts_per_page':5,'nopaging':False,'comments_per_page':'50','no_found_rows':False,'taxonomy':'anime-list','term':'shingeki-no-kyojin-the-final-season','order':'DESC'}
		q = '{"anime-list":"'+anime+'","posts_per_page":250, "order":"DESC"}'
		qq =json.loads(q)
		#myobj = {'action':'load_more_5', 'query': 'anime-list%22%3A%22shingeki-no-kyojin-the-final-season%22%2C%22error%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A0%2C%22post_parent%22%3A%22%22%2C%22subpost%22%3A%22%22%2C%22subpost_id%22%3A%22%22%2C%22attachment%22%3A%22%22%2C%22attachment_id%22%3A0%2C%22name%22%3A%22%22%2C%22pagename%22%3A%22%22%2C%22page_id%22%3A0%2C%22second%22%3A%22%22%2C%22minute%22%3A%22%22%2C%22hour%22%3A%22%22%2C%22day%22%3A0%2C%22monthnum%22%3A0%2C%22year%22%3A0%2C%22w%22%3A0%2C%22category_name%22%3A%22%22%2C%22tag%22%3A%22%22%2C%22cat%22%3A%22%22%2C%22tag_id%22%3A%22%22%2C%22author%22%3A%22%22%2C%22author_name%22%3A%22%22%2C%22feed%22%3A%22%22%2C%22tb%22%3A%22%22%2C%22paged%22%3A0%2C%22meta_key%22%3A%22%22%2C%22meta_value%22%3A%22%22%2C%22preview%22%3A%22%22%2C%22s%22%3A%22%22%2C%22sentence%22%3A%22%22%2C%22title%22%3A%22%22%2C%22fields%22%3A%22%22%2C%22menu_order%22%3A%22%22%2C%22embed%22%3A%22%22%2C%22category__in%22%3A%5B%5D%2C%22category__not_in%22%3A%5B%5D%2C%22category__and%22%3A%5B%5D%2C%22post__in%22%3A%5B%5D%2C%22post__not_in%22%3A%5B%5D%2C%22post_name__in%22%3A%5B%5D%2C%22tag__in%22%3A%5B%5D%2C%22tag__not_in%22%3A%5B%5D%2C%22tag__and%22%3A%5B%5D%2C%22tag_slug__in%22%3A%5B%5D%2C%22tag_slug__and%22%3A%5B%5D%2C%22post_parent__in%22%3A%5B%5D%2C%22post_parent__not_in%22%3A%5B%5D%2C%22author__in%22%3A%5B%5D%2C%22author__not_in%22%3A%5B%5D%2C%22ignore_sticky_posts%22%3Afalse%2C%22suppress_filters%22%3Afalse%2C%22cache_results%22%3Atrue%2C%22update_post_term_cache%22%3Atrue%2C%22lazy_load_term_meta%22%3Atrue%2C%22update_post_meta_cache%22%3Atrue%2C%22post_type%22%3A%22%22%2C%22posts_per_page%22%3A9%2C%22nopaging%22%3Afalse%2C%22comments_per_page%22%3A%2250%22%2C%22no_found_rows%22%3Afalse%2C%22taxonomy%22%3A%22anime-list%22%2C%22term%22%3A%22shingeki-no-kyojin-the-final-season%22%2C%22order%22%3A%22ASC%22%7D&page=1'}
		myobj = {'action':action, 'page': 0, 'query':  q }
		head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36', 'Accept-Encoding': 'identity', 'Content-Type': 'application/x-www-form-urlencoded', 'DNT': '1'}
		resp = requests.post(url, data = myobj, headers=head)
		return resp.text.replace("\n", '\r\n')
	except:
		return "erro"
def ListAnime(): #522
	link = common.OpenURL("https://www.erai-raws.info/anime-list/")
	lista = re.compile("href\=\"?([^\"]+)\"?.title\=\"?([^(\"|\>)]+)").findall(link)
	for url2,title2 in lista:
		xx.AddDir2(title2 , url2, 521, isFolder=True)
def Listepi(): #521
	xx.AddDir("Reload!" , "", 40, isFolder=False)
	#loads = ["load_more_0","load_more_5","load_more_3"]
	link = common.OpenURL("https://www.erai-raws.info/anime-list/"+url)
	lista = re.compile("http[^\"]+1080p[^\"]+\.torrent").findall(link)
	if not lista:
		lista = re.compile("magnet:[^\"]+1080p[^\"]+").findall(link)
	lista.reverse()
	try:
		for magnet in lista:
			magnet2 = unquote(magnet)
			title2 = magnet2.split("/")
			title2 = [[title2[len(title2)-1]]]
			if not re.compile("\.torrent$").findall(magnet):
			#if not ".torrent" in magnet2:
				title2 = re.compile("dn=(.+?)(\&|$)").findall(magnet2)
				#return
			hevec = "[+] " if "HEVC" in magnet else ""
			xx.AddDir(hevec+"[COLOR white]" +str(title2[0][0]).replace("[Erai-raws] ","")+ "[/COLOR]", "plugin://plugin.video.elementum/play?uri="+quote_plus(magnet), 3, isFolder=False, IsPlayable=True)
	except:
		pass
	return
	'''for l in loads:
		text = retsitereai(l,url)
		try:
			lista = re.compile("http.+?1080p.+?.torrent").findall(text)
			#ST(lista)
			if not lista:
				lista = re.compile("magnet:\?.+?1080p[^\"]+").findall(text)
			for magnet in lista:
				magnet2 = unquote(magnet)
				title2 = magnet2.split("/")
				title2 = [[title2[len(title2)-1]]]
				if not title2:
					title2 = re.compile("dn=(.+?)(\&|$)").findall(magnet2)
				hevec = "[+] " if "HEVC" in magnet else ""
				xx.AddDir(hevec+"[COLOR white]" +title2[0][0].replace("[Erai-raws] ","")+ "[/COLOR]", "plugin://plugin.video.elementum/play?uri="+quote_plus(magnet), 3, isFolder=False, IsPlayable=True)
				#AddDir("[COLOR yellow]" +title2[0]+ "[/COLOR]", "plugin://plugin.video.elementum/play?uri="+magnet, 3, isFolder=False, IsPlayable=True)
			if text:
				xx.AddDir("------------------------------------------------------------------" , "", 40, isFolder=False)
		except:
			pass
	#except:
		#ST(1) '''
def ListEpiMeta(): #523
	xx.AddDir("Reload" , "", 40, isFolder=False)
	trak = xx.traktS()
	meta = eval(metah)
	#loads = ["load_more_0","load_more_5"]
	progress = xbmcgui.DialogProgress()
	progress.create('Carregando...')
	progress.update(0, "Carregando...")
	link = common.OpenURL("https://www.erai-raws.info/anime-list/"+url)
	lista = re.compile("http[^\"]+1080p[^\"]+\.torrent").findall(link)
	if not lista:
		lista = re.compile("magnet:[^\"]+1080p[^\"]+").findall(link)
	lista.reverse()
	prog = 1
	try:
		for magnet in lista:
			magnet2 = unquote(magnet)
			batch = re.compile("(\d+) ?\~ ?(\d+)").findall(magnet2)
			#ST(magnet2)
			#x.AddDir("[COLOR white]" +str(magnet2)+ "[/COLOR]", "", 3, isFolder=False, IsPlayable=True)
			Index = -1
			#totalepi = int(batch[0][1])+1 - int(batch[0][0])
			if batch:
				totalepi = int(batch[0][1])+1 - int(batch[0][0])
				for E in range(int(batch[0][0]), int(batch[0][1])+1):
					progtotal = int(100*prog/totalepi)
					progress.update(progtotal, str(progtotal)+" %")
					prog+=1
					if (progress.iscanceled()): break
					Index+=1
					title2 = magnet2.split("/")
					title2 = [[title2[len(title2)-1]]]
					if not title2:
						title2 = re.compile("dn=(.+?)(\&|$)").findall(magnet2)
					try:
						pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(E) in trak else None
						xx.AddDir2("" ,"plugin://plugin.video.elementum/play?uri="+quote_plus(magnet)+"&index="+str(Index), 3, "", "",  isFolder=False, IsPlayable=True, background=background, metah=meta, episode=str(E), playcount=pc, DL="")
					except:
						xx.AddDir("[COLOR yellow]" +title2[0][0]+ "[/COLOR]", "plugin://plugin.video.elementum/play?uri="+quote_plus(magnet)+"&index="+str(Index), 3, isFolder=False, IsPlayable=True)
	except:
		pass
	try:
		prog = 1
		for magnet in lista:
			progtotal = int(100*prog/len(lista))
			progress.update(progtotal, str(progtotal)+" %")
			prog+=1
			if (progress.iscanceled()): break
			magnet2 = unquote(magnet)
			E = re.compile("\- ?(\d+)").findall(magnet2)
			title2 = magnet2.split("/")
			title2 = [[title2[len(title2)-1]]]
			if not re.compile("\.torrent$").findall(magnet):
				title2 = re.compile("dn=(.+?)(\&|$)").findall(magnet2)
			hevec = "[+] " if "HEVC" in magnet else ""
			batch = re.compile("(\d+) ?\~ ?(\d+)").findall(magnet2)
			if not batch:
				try:
					pc = 1 if meta['imdbnumber']+str(meta['season_number'])+str(int(E[0])) in trak else None
					xx.AddDir2("" ,"plugin://plugin.video.elementum/play?uri="+quote_plus(magnet), 3, "", "",  isFolder=False, IsPlayable=True, background=background, metah=meta, episode=E[0], playcount=pc, DL=hevec)
				except:
					xx.AddDir("[COLOR yellow]" +title2[0][0]+ "[/COLOR]", "plugin://plugin.video.elementum/play?uri="+quote_plus(magnet), 3, isFolder=False, IsPlayable=True)		
	except:
		pass
	progress.close()
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
