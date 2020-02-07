Started a new weather project. The last one stopped working due to an API change 
with pywapi.

The API DarkSky.net only allows 1000 api calls per day for free. I adjusted the 
amount of API calls to be made every even minute. 

Created a function to determine the wind bearing. This API returns a integer
value, so needed to calculate which degree maps to what direction.

Created a weatherModel class to hold data.

I had to install haveged due to error with bad handshake.
See this link:
https://www.raspberrypi.org/forums/viewtopic.php?t=228971