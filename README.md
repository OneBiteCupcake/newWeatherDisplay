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

2/8/2020
Adding logic to check for internet connection prior to making API call.

3/4/202
Removing DarkSky api secret key and latitude/longitude pair. Apparently someone else was using the same secret
key as me and was causing the daily limit to be exceeded. This way, users will have to supply their own key
and latitude/longitude pair. Powered by: https://darksky.net/poweredby/