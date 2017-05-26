# kindle-weather
Shows current time and temperatures on Amazon Kindle reader.
Tested on  [**jailbroken**](https://wiki.mobileread.com/wiki/Kindle4NTHacking#Jailbreak) [Kindle 4](https://wiki.mobileread.com/wiki/K4_Index) with broken screen (last 3-4 lines are unreadable - see pic).

  ![sample](doc/img/kindle.jpg)

## Demo
http://demo.ceszke.com/kindle-weather/

## Run

#### backend
* you will need any www server, python (tested on 2.7) and imagemagic
* install following pythons's packages: thingspeak and feedparser
* clone the code and make sure that dirs&files have appropriate permissions
* adapt [conf/settings.py](conf/settings.py)
* configure your www server to expose [www/](www/) and execute cgi scripts under [www/cgi-bin](www/cgi-bin)
* open [index.html](index.html) in your browser and check if png image was correctly rendered


#### kindle
* you will need Kindle with ssh access (jailbroken)
* copy [on_kindle/show.sh](on_kindle/show.sh) to /opt on your Kindle using i.e. WinSCP
* open that file and change PNG_URL variable according to your environment
* try to run manually show.sh and watch your Kindle's screen - time&temperatures should appear
* add new entries to crontab:
```
*/1  * * * * /opt/show.sh
0  */1 * * * /opt/show.sh clear
```
* that's all ;)



## Technology stack
* python
* bash
* e-ink
* imagemagic


