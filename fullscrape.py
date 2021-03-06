import ffscraper, os, time

def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)


#ffscraper.scrape_site_for_categories() #Get a link to every catagory on the site and save them in text files
#remove the first link from each file, except the crossover file

"""
#Create folders for saving sids
mediatypes=["anime","book","cartoon","comic","game","misc","movie","play","tv","crossovers"]
if not os.path.exists("sids"):
    os.mkdir("sids")
for folder in mediatypes:
    if not os.path.exists("sids/"+folder):
        os.mkdir("sids/"+folder)
time.sleep(1)

for txt in os.listdir("links"):
    media=txt[:-4]
    if media == "crossovers":
        lowerbound=2
        upperbound=3
    else:
        lowerbound=3
        upperbound=4
    f = open("links/"+txt)
    for line in f:
        line = str(line).replace("\n","")
        slash1 = findnth(line,"/",lowerbound)
        slash2 = findnth(line,"/",upperbound)
        filename = line[slash1+1:slash2]
        sids = ffscraper.get_sids_from_catagory(line)
        if len(filename)>=250:
            filename = filename[:249]
        f = open("sids/"+media+"/"+filename+".txt","w")
        for sid in sids:
            f.write(sid+"\n")
        f.close()
"""

#Scrape Fanfiction
scrapedSid=open("scrapedsid.txt","a+")
scrapedSid.close()
for media in os.listdir("sids"):
    for canon in os.listdir("sids/"+media):
        canonsiddir="sids/"+media+"/"+canon
        f = open(canonsiddir,"r")
        for line in f:
            line = str(line).replace("\n","")
            fileread = open("scrapedsid.txt","r+")
            found = False
            for ssid in fileread:
                ssid = str(ssid).replace("\n","")
                if line==ssid:
                    found = True
                    break
            fileread.close() 
            if not found:
                ffscraper.get_fanfic_text(line)
                filewrite = open("scrapedsid.txt","a+")
                filewrite.write(line+"\n")
                filewrite.close()
            else:
                print("SID:", line, "already scraped.")

                
            
