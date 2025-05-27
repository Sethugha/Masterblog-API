# Masterblog-API
The Masterblog API is a first contact with the creation of RESTful APIs.
It simulates the management of a blog written in Python via web interface 
using this api.

## Getting started
To start the project and begin experimenting with this currently rudimentary API
you need first to install the packages listed in requirements.txt.
From folder Masterblog-API start backend/backend.py
(terminal: **python3 backend/backend_app.py**)
Use, if possible, another computer to host the frontend (which requires a second installation process mirroring this process here.)
Nevertheless, to enable using he same Machine for frontend hosting, the application uses CORS thus using both applications
on the same host should work smoothly.

##Some hints for frontend and API: 

-The API has rate limits
-The API returns request responses in JSON format. When an API request returns an error, it is sent in the JSON response as an error key.
-To show the endpoints which are not cast in webpages an api documentation accessible via **<backend-host>:5002/api/docs** 
 has been implemented with swagger. 
-The only direct accessible page is the index page  on 
 **<frontend-host>5001/** 
-there you can view all posts by using the *load posts* button.
-add new posts by filling title and content into the form fields and clicking *add Post*. 
-delete posts using the *delete post* button on the right side of every post.
-Operations like search, sort or update are **only** avilable via REST-tool like *Postman* or *SoapUI*. 

###Rate and usage limits
API access rate limits apply at a client connection in unit time. The preset limit is 10 requests per minute. 

