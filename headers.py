import requests
import sys

def getURL() :

	urlInput = input('Enter the URL: ')
	if urlInput.find('https://') == 0 or urlInput.find('http://') == 0 :
		url = urlInput	
	else:
		url = 'http://' + urlInput    
	try:
		response = requests.get(url)
	except requests.exceptions.Timeout:
		print("Connection has timed out.")
		sys.exit(1)
	
	except requests.exceptions.TooManyRedirects:
		print("Too Many Redirects. Please try another URL")
		sys.exit(1)
	except requests.HTTPError as exception:
		print(exception)
		sys.exit(1)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)
	""" except requests.ssl.CertificateError :
		print("SSL Certificate not verified")
		response = requests.get(url, verify=False) """
		
	print(response)
	
	checkHeaders(response)
  
def checkHeaders(response) : 
	headersPresent = response.headers
	secHeaders = {'Strict-Transport-Security':['max-age=31536000', 'includeSubDomains'], 'X-Frame-Options':['deny'],'X-Content-Type-Options':['nosniff'],'Content-Security-Policy':[],'X-Permitted-Cross-Domain-Policies':['none'],'Referrer-Policy':['no-referrer'],'Clear-Site-Data':['cache','cookies','storage'],'Cross-Origin-Embedder-Policy':['require-corp'],'Cross-Origin-Opener-Policy':['same-origin'],'Cross-Origin-Resource-Policy':['same-origin'], 'Set-Cookie':['httponly','secure'], 'Cache-Control' : ['no-cache','no-store'], 'Pragma':['no-cache']}

	missingHeader = []
	headersUsed = dict()

	for header in secHeaders.keys():
		if header not in headersPresent.keys():
			missingHeader.append(header)
		else :
			headersUsed[header] = headersPresent[header]
		
	printHeaders(headersUsed,missingHeader,secHeaders)
	
def printHeaders(headersUsed,missingHeader,secHeaders) :		
	print(' ')
	print('Headers used are: ')

	for header,value in headersUsed.items():
		print(header + ' : ' + value,end = '\t\t'),
		if(header == 'Content-Security-Policy' or header == 'Strict-Transport-Security') :
			print(' ')
			continue
		warn = 0
		for secValue in secHeaders[header] :
			if (header == 'Set-Cookie') :
				if headersUsed[header].lower().find(secValue) == -1 :
					print('[WARNING: Must contain '+secValue+']', end = ' ')
					warn = 1	
					continue
			else:
				if (secValue.lower() not in [val.lower() for val in value.split(';')]) :
					print('[WARNING: Must contain '+secValue+']', end = ' ')
					warn = 1
			
		if (warn == 0):
			print('[OK]')
		print(' ')
	
	if (len(missingHeader) > 0):
		print(' ')
		for header in missingHeader:
			print(header, ' is missing', end = '\t' );
			if header == 'Content-Security-Policy' :
				print(' ')
				continue
			recommended = secHeaders[header]
			print('[Recommended:', end = ' ')
			if len(recommended) == 1 :
				for value in recommended:
					print(value, end='')
			else:
				for value in recommended:
					print(value, end = ';')
		
			print(']')
			
getURL()
			

