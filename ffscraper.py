import time, os
import fanfiction
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
    f = open("stories/"+canon+"/"+title+".txt", "w")
    print(fulltext)
    f.write(str(fulltext))
    f.close
#StoryID
sid = "4264713"
get_fanfic_text(sid)