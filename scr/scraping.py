import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import ssl


colorama.init()
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

internal_urls = set() #internal links form one domain
external_urls = set() #external links form one domain
all_external_urls = set() #external link from one deepth
nodes = set()
edges = list()
total_urls_visited = 0
deepth = 0

def is_valid(url):
    #check if url is valid
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):

    # urls set for scraping one link
    urls = set()

    # domain of URL
    domain_name = urlparse(url).netloc

    #get links from URL
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
    except ssl.SSLCertVerificationError:
        pass

    #search for a tags, egs: <a href="https://www.onet.pl">Visit Onet.pl!</a> 
    for a_tag in soup.findAll("a"):

        #get href 
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if "download" in href:
            #should exclude .pdf, .docx, etc. 
            continue
        if ".pdf" in href:
            #should exclude .pdf, .docx, etc. 
            continue
        if parsed_href.scheme == "mailto":
            #exclude mails
            continue
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                if len(external_urls) > 10: #number of external links form input link
                    continue
                print(f"{GRAY}External link: {href}{RESET}")
                external_urls.add(href) 
                all_external_urls.add(href) 
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls):

    global total_urls_visited
    total_urls_visited += 1
    
    #get links from URL
    links = get_all_website_links(url)

    # get links form multiple links with domain of URL
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def deep_crawl(dp,max_urls):

    # all links from deepth
    ext_temp = all_external_urls.copy()
    all_external_urls.clear()
    
    global deepth
    deepth += 1

    if deepth > dp:      
            return
    
    # get links form every link from deepth
    for link in ext_temp:

        global total_urls_visited
        total_urls_visited = 0

        internal_urls.clear()

        crawl(link,max_urls)

        #add domains to edges and nodes
        for link2 in external_urls:      
            edges.append((urlparse(link).netloc,urlparse(link2).netloc))
            nodes.add(urlparse(link2).netloc)
        
        external_urls.clear()
     
    deep_crawl(dp, max_urls)



def main():
    max_urls = 5 #number of internal links of url from which we scrap external links
    how_deep = 2  
    url = "http://www.mchtr.pw.edu.pl/"
    nodes.add(urlparse(url).netloc)
    
    #first iteration - deepth 0
    crawl(url, max_urls)
    for link in external_urls:
        edges.append((urlparse(url).netloc,urlparse(link).netloc))
    deep_crawl(how_deep, max_urls)

    #saving nodes and edges to csv file
    with open(f"nodes.csv", "w") as f:
        print("name", file=f)
        for node in nodes:
            print(node.strip(), file=f)

    with open(f"edges.csv", "w") as f:
        print("source,target,value", file=f)
        for link in edges:
            print( str(link[0]) + ',' + str(link[1]) + ",1", file=f)

main()