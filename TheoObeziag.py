import os
import requests as re
import sys
import lxml.html as lx


#get all Links from Website
#html = re.get("https://www21.in.tum.de/teaching/theo/SS19/").text

#root = lx.fromstring(html.encode('utf-8'))

#l = root.iterlinks()

#for temp in l:
#    print(temp)

exercise_link = "https://www21.in.tum.de/teaching/theo/SS19/ex/ex{}.pdf"
solution_link = "https://www21.in.tum.de/teaching/theo/SS19/ex/lo{}.pdf"

#
#'{:02d}'.format(11)


url = exercise_link.format('01')
filepath = '/Users/maximilianpalmer/Desktop/test/blatt1.pdf'

res = re.get("http://www14.in.tum.de/lehre/2019SS/dwt/uebung/loesungen/LO01.pdf", stream=True)

print(re.head(url).headers)

#if not res.ok:
    #return None

with open(filepath, 'wb') as f:
    for chunk in res:
        f.write(chunk)




#Theo:  https://www21.in.tum.de/teaching/theo/SS19/ex/ex02.pdf
#       https://www21.in.tum.de/teaching/theo/SS19/ex/lo01.pdf

#DWT:   http://www14.in.tum.de/lehre/2019SS/dwt/uebung/UE01.pdf
#       http://www14.in.tum.de/lehre/2019SS/dwt/uebung/loesungen/TL01.pdf   login dwt19 bernoulli