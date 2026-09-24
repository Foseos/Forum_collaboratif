import re
source=open('find_elena_gifs.py').read()
source=re.sub(r'names=\[.*?\]',"names=['dakota-johnson','millie-bobby-brown','peter-hale','malia-tate']",source,count=1)
exec(source)
