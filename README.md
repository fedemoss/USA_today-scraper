# USA Today newspaper scraper

This is a web scraper for the famous American newspaper 'USA Today'. The aim of this project is to get information about 
certain topics from different perspectives. So I started by analyzing which news are relevant in the USA.

## ADVICE & IP STUFF

This script is intended to work from google colab by default, since you dont use your IP when using this service.

If you want to run the script locally, be aware that, thanks to the many requests, 
out IP can be blocked by the newspaper site. In this case, we would want some kind of IP protection. 

I tried to protect my IP by generating a random number in each request and using that number to sleep the script....
but this is a poor way of protecting my IP...



## USING THE SCRIPT

The main function is:
    
    usa_today_scraper(topic)

-Where the topic is the topic we want to search about (ie topic='global warming'). 
 There are going to be news related with this topic. 


The main function returns a PANDAS dataframe with every article found related with the topic inserted.
