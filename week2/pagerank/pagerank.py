import os
import random
import re
import sys
from copy import deepcopy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    return_corpus = {}
    link_dir = {}

    #complete the damping probablity of each page
    link_set = corpus[page]
    num_link = len(link_set)
    for pages in link_set:
        link_dir[pages] = (1/num_link)*damping_factor
    
    #comlete the not damping probablity of each page and plus the damping probablity
    num_page = len(corpus.keys())
    for pages in corpus.keys():
        return_corpus[pages]=(1/num_page)*(1-damping_factor)
        if pages in link_set:
            return_corpus[pages]+=link_dir[pages]

    return return_corpus


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    return_corpus = {}
    page_pro = {}   #each page's probablity to be chosen
    pages = []
    pro = []    #two list to save the page and their probablity to use random to chosen one page
    page_dir = {}   #count each page's appear num in sample
    for page in corpus.keys():
        page_dir[page] = 0

    #generate each sample
    for i in range(n):
        if i==0:
            num_pro = 1/len(corpus.keys())
            for page in corpus.keys():
                pages.append(page)
                pro.append(num_pro)
            chosen_page = random.choices(pages, weights=pro, k=1)[0]
            print(chosen_page)
            page_dir[chosen_page]+=1
        else:
            page_pro = transition_model(corpus,chosen_page,damping_factor)
            pages = list(page_pro.keys())
            pro = list(page_pro.values())
            chosen_page = random.choices(pages, weights=pro, k=1)[0]
            page_dir[chosen_page]+=1

    #compute probablity of each page
    for page in page_dir.keys():
        return_corpus[page] = page_dir[page]/n
    return return_corpus



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


    #complete begin numlink and pr
    numlinks = {}
    pr = {}
    num_page = len(corpus.keys())
    for page in corpus.keys():
        numlinks[page] = len(corpus[page])
        pr[page] = 1/num_page

    #two dir to save old probablity and new probablity
    #(not empty in old beacause use it to "simulate do-while loop")
    new_corpus = {}
    old_corpus = {'hi':0}

    while new_corpus!=old_corpus:
        old_corpus = deepcopy(new_corpus)

        old_pr = deepcopy(pr)
        for page in corpus.keys():
            pr[page] = (1-damping_factor)/num_page
            for page2 in corpus.keys():
                if page in corpus[page2]:
                    pr[page]+=damping_factor*(old_pr[page2]/numlinks[page2])
                if len(corpus[page2])==0:
                    pr[page]+=damping_factor*(old_pr[page2]/num_page)
            new_corpus[page] = round(pr[page],4)

    return new_corpus




if __name__ == "__main__":
    main()
