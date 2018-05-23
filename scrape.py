import requests
from lxml import html
import csv
from multiprocessing.dummy import Pool as ThreadPool

def parseUrl(url, csvfile):
	csvWriter = csv.writer(csvfile,delimiter=',')
	result = requests.get(
		url, 
		headers = dict(referer = url)
	)
	tree = html.fromstring(result.content)

	results = tree.xpath("//td[starts-with(@class, 'dbbeedetaildata')]")
	arr = [x.text_content() if x.text_content() else '' for x in results]
	arr = [x.strip() for x in arr]
	arr = [x if x != '\xa0' and x != "" else " " for x in arr]
	csvWriter.writerow(arr)
	return(len(arr) > 0)


pool = ThreadPool(4)
file = input("Output file name: ")
rpp = int(input("# results per page: "))
burl = input("List url: ") #https://thyme.dbbee.com/u/BP05945QON/BLOGDIRECTORY13qbdsl.wbsp?wb_mq=F&WB_StartRec=
burl = burl.split("?",1)[0]
burl += "?wb_mq=F&WB_StartRec="
i = 1;
rurls = set()
results = set()
print("Gathering result urls...")
while True:
	print(i)
	url = burl + str(i)
	i += rpp
	result = requests.get(
		url, 
		headers = dict(referer = url)
	)
	tree = html.fromstring(result.content)
	rows = tree.xpath("//tr/@onclick")
	urls = [("https:" + x.strip("document.location=").strip(";").strip("'")) for x in rows]
	rurls = rurls | set(urls)
	if len(rows) < rpp: break;


with open(file, 'a+') as csvfile:
	results = pool.map(lambda x: parseUrl(x,csvfile), rurls)
		