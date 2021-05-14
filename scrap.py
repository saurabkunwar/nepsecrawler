from bs4 import BeautifulSoup
import requests
import requests, six
import lxml.html as lh
from itertools import cycle, islice
import pandas as pd
from openpyxl import Workbook


html_text = requests.get('http://www.nepalstock.com/stockWisePrices').text


soup = BeautifulSoup(html_text,'lxml')

select = soup.find('select',class_='stock-symbol')

options = select.find_all('option')

#At first we need to find symbol no of each company, its different from company sybmbol
for option in options:

	tostr = str(option)
	spl = tostr.split('\"')
	symbolno = spl[1]
	stockname = option.text

	#These company has \ in their symbol, I couldnt escape it and they are probably promoter share or something so i decided to skip it
	if(symbolno=="2840" or symbolno=="2825" or symbolno=="2868"):
		continue

	print(symbolno)
	print(stockname)


	#Real magic, leak i found on nepse
	url="http://www.nepalstock.com/main/stockwiseprices/index/150/?startDate=2000-01-01&endDate=2021-05-04&stock-symbol="+symbolno+"&_limit=5000"

	page = requests.get(url)

	workbook = Workbook()
	ws = workbook.active

	doc = lh.fromstring(page.content)

	tr_elements = doc.xpath('//tr')


	for j in range(1,len(tr_elements)):
		row = tr_elements[j]

		i=0

		rowdata = []

		for t in row.iterchildren():
			data=t.text_content()
			rowdata.append(data)

		print(rowdata)

		ws.append(rowdata)

	workbook.save(stockname+".xlsx")