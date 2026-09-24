import re,json
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
names=['matt-donovan','tyler-lockwood']
def run(n):
 try:
  s=urlopen(Request('https://tenor.com/search/'+n+'-gifs',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode()
  urls=list(dict.fromkeys(re.findall(r'https://media[^"<>\s]+?\.gif',s)))
  return n,urls[:8]
 except Exception as e:return n,str(e)
print(json.dumps(list(ThreadPoolExecutor(7).map(run,names)),indent=2))


