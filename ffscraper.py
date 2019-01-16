import time, os, fanfiction, requests, bs4
if not os.path.exists("stories"):
    os.makedirs("stories")

def get_fanfic_text(sid):
    scraper = fanfiction.Scraper()
    metadata = scraper.scrape_story_metadata(sid)
    title = metadata.get("title")
    canon = metadata.get("canon")
    chapters = metadata.get("num_chapters")
    fulltext=""
    if chapters == None:
        fulltext=scraper.scrape_chapter(sid, title, keep_html=False)
    else:
        for cid in range(int(chapters)):
            chaptext = scraper.scrape_chapter(sid, str(int(cid)+1), keep_html=False)
            time.sleep(1)
            fulltext=fulltext+str(chaptext)+" "
    if not os.path.exists("stories/"+canon):
        os.makedirs("stories/"+canon)
    f = open("stories/"+canon+"/"+str(sid)+" "+title+".txt", "w")
    f.write(str(fulltext))
    f.close

def get_sids_from_catagory(crossover,medium,ffcatagory):
    #create extensions for url based on input
    if crossover:
        webpageext = "crossovers"+medium+"/"+ffcatagory
    else:
        webpageext = medium+"/"+ffcatagory
    webpage = str("http://fanfiction.net/") + webpageext

    #get page 1 of fanfiction and import to bs4 for processing
    print("Retrieving webpage:", webpage)
    start = time.time()
    session = requests.Session()
    session.trust_env = False 
    r = session.get(webpage)
    print("Retrieved webpage. Scanning for SIDs now.")
    end = time.time()
    print("This took:", end-start, "seconds")
    soup = bs4.BeautifulSoup(r.content, "html.parser")

    #loop to find link of last page
    templinklist=[]
    for a in soup.find_all('a', href=True):
        fullurl = str(a['href'])
        if fullurl.startswith("/"+webpageext):
            templinklist.append(fullurl)
    lastpage = templinklist[-2]
    lastpagenum = lastpage[(lastpage.find("&pe")-2):]

    #iterate through links on first page to collect SIDs
    for a in soup.find_all('a', href=True):
        fullurl = str(a['href'])
        if fullurl.startswith("/s/"):
            slicedurl = fullurl[3:]
            endofsid = slicedurl.find('/')
            sid = slicedurl[:endofsid]
            print(sid)
    pagenum=2

get_sids_from_catagory(False, "movie", "Zootopia")