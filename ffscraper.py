import time, os, fanfiction, requests, bs4


def get_fanfic_text(sid):
    if not os.path.exists("stories"):
        os.makedirs("stories")
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
    fulltext = str(fulltext).replace("\\n","")
    fulltext = str(fulltext).replace("\\'","'")
    title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    f = open("stories/"+canon+"/"+str(sid)+" "+title+".txt", "w")
    f.write(str(metadata)+"\n")
    f.write("\n")
    f.write(str(fulltext))
    f.close
    print("Saved to", "stories/"+canon+"/"+str(sid)+" "+title+".txt")

def get_sids_from_catagory(webpage):

    webpageext=webpage[27:]
    print(webpageext)
    #get page 1 of fanfiction and import to bs4 for processing
    session = requests.Session()
    session.trust_env = False 
    r = session.get(webpage)

    soup = bs4.BeautifulSoup(r.content, "html.parser")

    singlepage = True
    #loop to find link of last page
    templinklist=[]
    for a in soup.find_all('a', href=True):
        fullurl = str(a['href'])
        if fullurl.startswith("/"+webpageext):
            templinklist.append(fullurl)
        if "&p=" in fullurl:
            
            singlepage = False
    
    sidlist=[]
    if singlepage:
        print("This has only one page")
        time.sleep(1)
        downloadpage = webpage
        print("Downloading and parsing page:", downloadpage)
        r = session.get(downloadpage)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        pagesidlist=[]
        for a in soup.find_all('a', href=True):
            fullurl = str(a['href'])
            if fullurl.startswith("/s/"):
                slicedurl = fullurl[3:]
                endofsid = slicedurl.find('/')
                sid = slicedurl[:endofsid]
                sidlist.append(sid)

    else:
        print("This canon has multiple pages")
        lastpage = templinklist[-2]
        lastpagenum = lastpage[(len(lastpage))-lastpage.find("&pe")*-1:]
        currentpage = 1
        webpage=webpage+"?&srt=1&r=103&p="
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

    return(sidlist)


def scrape_site_for_categories():
    mediatypes=["anime","book","cartoon","comic","game","misc","movie","play","tv"]
    webpage = str("http://fanfiction.net")
    if not os.path.exists("links"):
        os.makedirs("links")

    #Crossover story links
    crossoverlinks=[]
    finallinks=[]
    for media in mediatypes:
        print("Sleeping to prevent spam")
        print("Searching "+media)
        time.sleep(1)
        fullurl = webpage + "/crossovers/" + media + "/"
        session = requests.Session()
        session.trust_env = False 
        r = session.get(fullurl)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        for a in soup.find_all('a', href=True):
            link = str(a['href'])
            if link.startswith("/crossovers/"):
                crossoverlinks.append(link)

    for crosslink in crossoverlinks:
        print("Sleeping to prevent spam")
        print("Searching "+crosslink)
        time.sleep(1)
        fullurl2 = webpage + crosslink
        session = requests.Session()
        session.trust_env = False
        r = session.get(fullurl2)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        for a in soup.find_all('a', href=True):
            link = str(a['href'])
            if "Crossovers" in link:
                if link not in finallinks:
                    finallinks.append(link)             
        f = open("links/crossovers.txt", "w")
        for link in finallinks:
            f.write(webpage+str(link)+"\n")
        f.close

    #Rgular story links
    for media in mediatypes:
        time.sleep(1)
        linklist=[]
        fullurl = webpage + "/" + media + "/"
        session = requests.Session()
        session.trust_env = False 
        r = session.get(fullurl)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        for a in soup.find_all('a', href=True):
            link = str(a['href'])
            if link.startswith("/"+media):
                linklist.append(link)
        f = open("links/"+media+".txt", "w")
        for link in linklist:
            f.write(webpage+str(link)+"\n")
        f.close
