import urllib.request
import pandas

fp = urllib.request.urlopen("https://gerbil-qa.aksw.org/gerbil/experiment?id=202304170000")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

print(mystr)