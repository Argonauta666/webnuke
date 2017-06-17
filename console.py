#!/usr/bin/env python

# add owa to quickdetect - look for function IsOwaPremiumBrowser

import curses
import time
from libs.AngularUtil import *
from libs.WordPressUtil import *
from libs.DrupalUtil import *
from libs.JQueryUtil import *
from libs.WebDriverUtil import *
from libs.gui.cursesutil import *
from libs.gui.javascriptmenu import *
from libs.gui.angularmenu import *
from libs.gui.htmlmenu import *
from libs.QuickDetect import *
from libs.JSConsole import *
from libs.spider.spiderscreen import *
from libs.spider.spidercommands import *
from libs.logger import *
from webnukeproxy import *
from libs.javascriptinjector import *

class mainframe:
	def __init__(self, logger, proxy_port):
		self.debug = True
		#self.proxy_host = 'localhost'
		#self.proxy_port = proxy_portv
		self.proxy_host = ''
		self.proxy_port = 0
		self.driver = 'notset'
		self.current_url = "NONE"
		self.warning = ''
		self.curses_util = CursesUtil()
		self.logger = logger
		self.jsinjector = JavascriptInjector()
		# load plugin javascript
		self.plugins = [JSConsoleScript(self.jsinjector), JavascriptScript(self.jsinjector), HTMLToolsScript(self.jsinjector)]
		
	def run_main(self):
		self.logger.log("run_main")
		mystr = 'startup'
		mystr_elements = mystr.split()
		firstelement=mystr_elements[0]

		while firstelement != 'quit' and firstelement != 'q':
			 self.screen = self.curses_util.get_screen()

			 self.screen.addstr(2, 2,  "Please enter a command")
			 self.screen.addstr(4, 4,  "goto <url>   - opens url")
			 self.screen.addstr(5, 4,  "quickdetect  - detect technologies in use on url...")
			 self.screen.addstr(6, 4,  "jsconsole    - opens a console bound to a browser javascript console...")
			 self.screen.addstr(7 , 4, "html         - HTML tools menu...")
			 self.screen.addstr(8 , 4, "javascript   - Javascript tools menu...")
			 self.screen.addstr(9 , 4, "angularjs    - AngularJS tools menu...")
			 self.screen.addstr(10, 4, "spider       - Spider tools menu...")
			 self.screen.addstr(14, 4, "debug        - toggle debug on/off")
			 self.screen.addstr(15, 4, "proxy        - set proxy settings...")
			 self.screen.addstr(16, 4, "!sh          - escape to unix land...")
			 self.screen.addstr(18, 4, "quit         - Exit webnuke")
			 # pic from http://ascii.co.uk/art/rockets
			 self.screen.addstr(8, 45, "                 *    ", curses.color_pair(2))
			 self.screen.addstr(9, 45, "     +               ", curses.color_pair(2))
			 self.screen.addstr(10,45, "        *          +   '--'  *", curses.color_pair(2))
			 self.screen.addstr(11,45, "            +   /\\", curses.color_pair(2))
			 self.screen.addstr(12,45, "+             .'  '.   *", curses.color_pair(2))
			 self.screen.addstr(13,45, "      *      /======\\      +", curses.color_pair(2))
			 self.screen.addstr(14,45, "            ;:.      ;", curses.color_pair(2))
			 self.screen.addstr(15,45, "            |:.      |", curses.color_pair(2))
			 self.screen.addstr(16,45, "            |:.      |", curses.color_pair(2))
			 self.screen.addstr(17,45, "  +         |:.      |          *", curses.color_pair(2))
			 self.screen.addstr(18,45, "            ;:.      ;", curses.color_pair(2))
			 self.screen.addstr(19,45, "          .' \\:.    / `.", curses.color_pair(2))
			 self.screen.addstr(20,45, "         / .-'':._.'`-. \\", curses.color_pair(2))
			 self.screen.addstr(21,45, "         |/    /||\\    \\|", curses.color_pair(2))
			 
			 if self.warning is not '':
				 self.screen.addstr(22, 2, self.warning, curses.color_pair(1))
				 self.warning=''
			 
			 if self.proxy_host is not '':
				 self.screen.addstr(0, 1, "PROXY ENABLED", curses.color_pair(1))
			 if self.debug:
				 self.screen.addstr(0, 71, "DEBUG ON", curses.color_pair(1))
			 self.screen.refresh()

			 mystr = self.screen.getstr(20,4).decode(encoding="utf-8")
			 mystr_elements = mystr.split()
			 firstelement='notset'
			 if len(mystr_elements) >= 1:
				firstelement=mystr_elements[0]

			 if firstelement == 'd':
				 self.debug = True
				 self.current_url = "https://www.wufoo.com/html5/types/11-hidden.html"
				 self.open_url(self.current_url)
				 firstelement="html"
				 
			 
			 if firstelement == 'goto':
				 if len(mystr_elements) >= 2:
					 url = mystr_elements[1]
				 else:
					 url = self.curses_util.get_param("Enter the url")
				
				 self.open_url(url)
				 
			 
			 if firstelement == 'debug':
				  self.debug = not self.debug
				  
			 if firstelement == 'proxy':
				  self.proxy_host = self.curses_util.get_param("Enter Proxy Server Hostname or IP, Leave BLANK for no proxy")
				  self.proxy_port = self.curses_util.get_param("Enter Proxy Server Port Number")
				  
			 if firstelement == 'quickdetect':
				 if len(mystr_elements) >= 2:
					 url = mystr_elements[1]
					 self.open_url(url)
				 
				 if self.driver == 'notset':
					 self.warning = "QUICKDETECT requires a url is loaded, please set a url using GOTO"
					 return
					
				 QuickDetect(self.screen, self.driver, self.curses_util).run()
			 
			 if firstelement == 'jsconsole':
				 self.curses_util.close_screen()
				 JSConsole(self.driver, self.jsinjector).run()
				 
			 if firstelement == '!sh':
				  self.curses_util.execute_cmd("bash")
				  
			 if firstelement == 'javascript':
				 JavascriptScreen(self.screen, self.driver, self.curses_util, self.jsinjector).show()

			 if firstelement == 'angularjs':
				 AngularScreen(self.screen, self.driver, self.curses_util).show()
				 
			 if firstelement == 'spider':
				 SpiderScreen(self.screen, self.curses_util, self.current_url, self.proxy_host, self.proxy_port).show()
				 
			 #if firstelement == 'javascript':
				# ResendScreen(self.screen, self.curses_util)
			 
			 if firstelement == 'html':
				 HTMLScreen(self.screen, self.driver, self.curses_util, self.jsinjector).show()


		self.curses_util.close_screen()
	def create_browser_instance(self):
		self.webdriver_util = WebDriverUtil()
		self.webdriver_util.setDebug(self.debug)
		if self.proxy_host is not '' and int(self.proxy_port) is not 0:
			return self.webdriver_util.getDriverWithProxySupport(self.proxy_host, int(self.proxy_port))
		else:
			return self.webdriver_util.getDriver(self.logger)
		 
	def open_url(self, url):
		if self.driver == 'notset':
			self.driver = self.create_browser_instance()
		self.current_url = url
		
		self.driver.get(url)
		self.current_url = self.driver.current_url
		

logger = FileLogger()
logger.log('app started')

try:
	#webserver = webnuke_api_server(logger)
	#webserver.start()
	currently_not_used_local_proxy_port = 8008
	#webnukeproxy = ProxySupport("bah1", proxy_port, logger)
	
	
		
	mainwin = mainframe(logger, currently_not_used_local_proxy_port)
	mainwin.run_main()
except:
	logger.log('app error')
	raise
#finally:
	#webnukeproxy.stop()
	

logger.log('app ended')


		
