def BuscaTrtvTvshow(type="episode"):
	meta = eval(dados)["meta"]
	#ST(meta)
	mdb = json.loads(url)
	imdb = mdb["external_ids"]["imdb_id"]
	try:
		query = mdb["name"] +" "+ mdb["first_air_date"].split("-")[0]+" site:https://trailers.to/en/"+type
	except:
		query = mdb["name"] +" site:https://trailers.to/en/"+type
	#ST(query)
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
				#xx.AddDir(meta["TVShowTitle"]+" ([COLOR yellow]Trailers.to - Play[/COLOR])", id[0], "trtv.SeasonsPlay", isFolder=True, dados={'meta': meta})
				progress.close()
				return
		except:
			pass
	if type=="episode":
		BuscaTrtvTvshow("tvshow")
