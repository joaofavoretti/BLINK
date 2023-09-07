# Important considerations
- Add some phishing tank urls inside to check my success rate

# Tasks
[X] Create a simple website using vuetify and nuxt
[X] Create a simple server
[X] Getting the URLs with warc library
[X] Request for GSB using postman
    After:
    [X] Create a new api key
    [X] Create a script to make the request
[ ] Store some of the URLs in the database
    Before:
    [X] Create a non-relational database
    [X] Integrate it with python

    [X] Understand what are all the parameters I want to fill for each of them (Can be changed in the future)
    {
        url: "http://aeon-cardkkm.tokyo/jp/login.html",
        gsb_inspection: {
            triggered: true,
            response: {}
        }
        manual_inspection: {
            triggered: true,
            comments: {}
        }
    }
    [X] Choose which URLs we will store (maybe 3000 of them)
    Random selection -- For now
    [ ] Store some of the URLs in a text file
    [ ] Store 500 urls from PhishTank in a text file 
[ ] Store the results from GSB in the database for each url stored
[ ] Make the endpoints to interact with the data
[ ] Create the website to interact with the endpoints
    After:
    [ ] Try to create a view button for the URL

# In progress
[ ] Adding 500 phishtank urls to test my success rate

# 4 the Future
[ ] Figure out how to get more URLs from the CommonCrawl website
    -> Could not find a way to discover where are the .gz files containing the URLs (WARC files)

[ ] Host it all in a single Docker container
[ ] Make it easily available to everybody that want to help (Host the website and the database remotely)
[ ] Put it in some cloud platform
    Before: 
    [ ] Check if the Oracle machine is still free
    [ ] Check Github Student Pack

[ ] Should I use Firebase to store the data?
