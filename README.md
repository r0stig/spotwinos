Spotwinos
==================================
**Spo**tify T**wi**tter So**nos**

Arguing what music to choose at the office? With this service you set up a twitter account (or using an existing one) which you send spotify track URIs to. The service will then add the tracks to the sonos queue.


Dependencies
============
* twython (pip install twython)
* SoCo - I'm using my own implementation of this with spotify plugin until the soco team approved my Pull request, find it at: https://github.com/r0stig/SoCo

Howto
======
* Set up a twitter dev account (dev.twitter.com)
* Retrieve Api key, secret, access token, secret
* Retrieve your twitter user id (http://gettwitterid.com/)
* Find your sonos device name, the one you choose the first time you used it
* Make a copy of settings.cfg.sample with name settings.cfg and set all settings using the above information
