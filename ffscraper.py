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
    #create extensions for url based on input, create directory for saving, and craft url to scrape
    if crossover:
        webpageext = "crossovers"+medium+"/" 
    else:
        webpageext = medium+"/"
    if not os.path.exists(webpageext):
        os.makedirs(webpageext)
    webpage = str("http://fanfiction.net/") + webpageext + ffcatagory

    #get page 1 of fanfiction and import to bs4 for processing
    session = requests.Session()
    session.trust_env = False 
    r = session.get(webpage)

    soup = bs4.BeautifulSoup(r.content, "html.parser")

    #loop to find link of last page
    templinklist=[]
    for a in soup.find_all('a', href=True):
        fullurl = str(a['href'])
        if fullurl.startswith("/"+webpageext):
            templinklist.append(fullurl)
    lastpage = templinklist[-2]
    lastpagenum = lastpage[(lastpage.find("&pe")-2):]
    currentpage = 1
    webpage=webpage+"/?&srt=1&r=103&p="
    sidlist=[]

    #Loop for each page until last page and get SIDs on each page
    while currentpage <= int(lastpagenum):
        print("Waiting 1 second to prevent spam")
        time.sleep(1)
        downloadpage = webpage + str(currentpage)
        print("Downloading and parsing page:", downloadpage)
        r = session.get(downloadpage)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        pagesidlist=[]

    #iterate through links on page to collect SIDs
        for a in soup.find_all('a', href=True):
            fullurl = str(a['href'])
            if fullurl.startswith("/s/"):
                slicedurl = fullurl[3:]
                endofsid = slicedurl.find('/')
                sid = slicedurl[:endofsid]
                pagesidlist.append(sid)
        print("Found", len(pagesidlist), "SIDs on page")

        for sid in pagesidlist:
            if sid not in sidlist:
                sidlist.append(sid)
        currentpage+=1

    #Save into file    
    savedir = "sids/"+webpageext+ffcatagory+".txt"
    print("Saving:", len(sidlist), "SIDs to", savedir)
    with open(savedir, "w") as f:
        for sid in sidlist:
            f.write(sid+"/n")
        f.close()
    print("Done")

get_sids_from_catagory(False, "movie", "Zootopia")