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
[X] Store the entries in the database
    Before:
    [X] Create a non-relational database
    [X] Integrate it with python

    [X] Understand what are all the parameters I want to fill for each of them (Can be changed in the future)
    {
        url: "http://aeon-cardkkm.tokyo/jp/login.html",
        online: true,
        phishtank_inspection: {
            triggered: true,
        }
        gsb_inspection: {
            triggered: true,
            comments: {}
        }
        manual_inspection: {
            triggered: true,
            comments: {}
        }
    }
    [X] Choose which URLs we will store (maybe 3000 of them)
    Random selection -- For now

    -> First option: Make separate scripts for each of the following tasks
    [ ] Decide which urls from commoncrawl are going in
    [ ] Decide which urls from phishtank are going in
    [ ] Add them directly to the database
    -> Alternative: Should I centralize all those functionalities on the server?
    [X] Structuring a regular rest api with flask
    [X] What should the endpoints be
        /urls/
        /gsb/validate
    [X] Create multiple endpoints

[X] Store the results from GSB in the database for each url stored
[X] Make the endpoints to interact with the data
[ ] Create the website to interact with the endpoints
    After:
    [ ] Try to create a view button for the URL

# In progress
[X] Adding 500 phishtank urls to test my success rate

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
