function FindProxyForURL(url, host)
{
	if (url.toLowerCase().substring(0, 6) == "https:") 
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".crl", url.length - ".crl".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".js", url.length - ".js".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".json", url.length - ".json".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".png", url.length - ".png".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".jpg", url.length - ".jpg".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".jpeg", url.length - ".jpeg".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf(".gif", url.length - ".gif".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("favicon.ico", url.length - "favicon.ico".length) !== -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("scholar.google.") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("ad.doubleclick.net") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("localhost") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("127.0.0.1") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("news.ycombinator.com") != -1)
		return "DIRECT";
//	else if (url.toLowerCase().indexOf(".c.youtube.com") != -1)
//		return "DIRECT";
	else if (url.toLowerCase().indexOf("http%3A%2F%2F") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("talk.google.com") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("talkx.l.google.com") != -1)
		return "DIRECT";
//	else if (url.toLowerCase().indexOf(".youtube.com/get_video_info") != -1)
//		return "DIRECT";
//	else if (url.toLowerCase().indexOf(".youtube.com/ptracking") != -1)
//		return "DIRECT";
//	else if (url.toLowerCase().indexOf(".youtube.com/annotations_iv") != -1)
//		return "DIRECT";
//	else if (url.toLowerCase().indexOf("www.youtube-nocookie.com") != -1)
//		return "DIRECT";
//	else if (url.toLowerCase().indexOf("www.youtube.com/gen") != -1)
//		return "DIRECT";
//	else if (url.toLowerCase().indexOf("www.youtube.com") != -1)
//		return "DIRECT";
	else if (url.toLowerCase().indexOf("http://clients1.google.com/generate_204") == 0)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("http://ocsp.") == 0)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("http://safebrowse") == 0)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("-pct.channel.facebook.com/p") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("ws.detectlanguage.com/") != -1)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("http://127.") == 0)
		return "DIRECT";
	else if (url.toLowerCase().indexOf("http://192.") == 0)
		return "DIRECT";
	 else if (url.toLowerCase().indexOf("http://10.") == 0)
		return "DIRECT";
		
	return "PROXY {{ server.ip_address }}:{{ server.port }}; DIRECT";
}
