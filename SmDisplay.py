import os, pygame, time, requests
from weatherModel import weatherModel
from datetime import datetime
import calendar
from pygame.locals import *

'''new icons from http://darkskyapp.github.io/skycons/'''


# Small LCD Display.
def convertWindBearing(windBearing):
    print("in convertWindBearing - windBearing: " + str(windBearing))

    if windBearing != '':
        if 337.5 < windBearing <= 22.5:
            return "N"
        elif 22.5 < windBearing <= 67.5:
            return "NE"
        elif 67.5 < windBearing <= 112.5:
            return "E"
        elif 112.5 < windBearing <= 157.5:
            return "SE"
        elif 157.5 < windBearing <= 202.5:
            return "S"
        elif 202.5 < windBearing <= 247.5:
            return "SW"
        elif 247.5 < windBearing <= 292.5:
            return "W"
        elif 292.5 < windBearing <= 337.5:
            return "NW"
        else:
            return "ERR"
    else:
        return "ERR"


class SmDisplay:
    screen = None

    ####################################################################
    def __init__(self):
        print("in __init__")
        "Initializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("X Display = {0}".format(disp_no))

        print("getting ready to check drivers")
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break
        print("done checking drivers")
        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer Size: %d x %d" % (size[0], size[1]))
        # todo - figure out what's going on here
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        print("clear screen to start")
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        print("font init")
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.mouse.set_visible(0)
        print("display update")
        pygame.display.update()
        # for fontname in pygame.font.get_fonts():
        #        print fontname
        print("initialize vars")
        self.temp = ''
        self.feels_like = 0
        self.wind_speed = 0
        self.baro = 0.0
        self.wind_dir = ''
        self.humid = 0
        self.wLastUpdate = ''
        self.day = ['', '', '', '']
        self.icon = ['clear-day.png', 'clear-day.png', 'clear-day.png', 'clear-day.png']
        self.rain = ['', '', '', '']
        self.temps = [['', ''], ['', ''], ['', ''], ['', '']]
        self.sunrise = '7:00 AM'
        self.sunset = '8:00 PM'

        print("larger display")
        # Larger Display
        self.xmax = 800
        self.ymax = 600
        self.scaleIcon = True  # Weather icons need scaling.
        self.iconScale = 1.5  # Icon scale amount.
        self.subwinTh = 0.05  # Sub window text height
        self.tmdateTh = 0.100  # Time & Date Text Height
        self.tmdateSmTh = 0.06
        self.tmdateYPos = 10  # Time & Date Y Position
        self.tmdateYPosSm = 18  # Time & Date Y Position Small

        print("small display")
        """
        # Small Display
        self.xmax = 656 - 35
        self.ymax = 416 - 5
        self.scaleIcon = False		# No icon scaling needed.
        self.iconScale = 1.0
        self.subwinTh = 0.065		# Sub window text height
        self.tmdateTh = 0.125		# Time & Date Text Height
        self.tmdateSmTh = 0.075
        self.tmdateYPos = 1		# Time & Date Y Position
        self.tmdateYPosSm = 8		# Time & Date Y Position Small
        """

        print("done in __init__")

    ####################################################################
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    ####################################################################
    def getIcon(w, i):
        try:
            return int(w['forecasts'][i]['day']['icon'])
        except:
            return 29

    ####################################################################
    def UpdateWeather(self):
        print("in UpdateWeather")
        # Use Weather.com for source data.
        # cc = 'current_conditions'
        # f = 'forecasts'

        # This is where the majic happens.
        # self.w = requests.get('https://api.darksky.net/forecast/c3942c89e1f9bd21d67991d4718d0b3f/39.615040,-104.753680')
        # w = self.w
        r = requests.get('https://api.darksky.net/forecast/c3942c89e1f9bd21d67991d4718d0b3f/39.615040,-104.753680')
        # print(r.status_code)
        # print(r.json())
        if r.status_code == 200:
            currently = r.json().get("currently")
            print(currently)

            model = weatherModel(datetime.fromtimestamp(currently.get("time")),
                                 currently.get("temperature"),
                                 currently.get("apparentTemperature"),
                                 currently.get("windSpeed"),
                                 currently.get("windGust"),
                                 currently.get("pressure"),
                                 currently.get("humidity"),
                                 currently.get("visibility"),
                                 currently.get("windBearing"))
            dailyData = r.json().get("daily").get('data')

            print(model.__str__())
            print(dailyData)
            day1 = dailyData[0]
            print(day1)

            day2 = dailyData[1]
            print(day2)

            day3 = dailyData[2]
            print(day3)

            day4 = dailyData[3]
            print(day4)

            try:
                if model.lastUpdate != self.wLastUpdate:
                    self.wLastUpdate = model.lastUpdate
                    print("New Weather Update: " + str(self.wLastUpdate))
                    self.temp = str(int(model.temp)).lower()
                    self.feels_like = str(int(model.feelsLike)).lower()
                    self.wind_speed = str(int(model.windSpeed)).lower()
                    self.baro = str(round(model.barometer / 33.864, 2)).lower()
                    print("model.windBearing: " + str(model.windBearing))
                    self.wind_dir = convertWindBearing(model.windBearing)
                    self.humid = str(int(model.humidity * 100)).upper()
                    # self.vis = str(model.visibility).upper()
                    # self.gust = str(model.windGust).upper()
                    # self.wind_direction = string.ascii_uppercase(w[cc]['wind']['direction'])
                    self.day[0] = calendar.day_name[datetime.fromtimestamp(day1.get("time")).weekday()]
                    self.day[1] = calendar.day_name[datetime.fromtimestamp(day2.get("time")).weekday()]
                    self.day[2] = calendar.day_name[datetime.fromtimestamp(day3.get("time")).weekday()]
                    self.day[3] = calendar.day_name[datetime.fromtimestamp(day4.get("time")).weekday()]
                    print("self.day: " + str(self.day))
                    # self.sunrise = w[f][0]['sunrise']
                    # self.sunset = w[f][0]['sunset']
                    self.icon[0] = day1.get("icon") + ".png"
                    self.icon[1] = day2.get("icon") + ".png"
                    self.icon[2] = day3.get("icon") + ".png"
                    self.icon[3] = day4.get("icon") + ".png"
                    print('Icon Index: ', self.icon[0], self.icon[1], self.icon[2], self.icon[3])
                    # print 'File: ', sd+icons[self.icon[0]]
                    self.rain[0] = str(int(day1.get("precipProbability") * 100))
                    self.rain[1] = str(int(day2.get("precipProbability") * 100))
                    self.rain[2] = str(int(day3.get("precipProbability") * 100))
                    self.rain[3] = str(int(day4.get("precipProbability") * 100))
                    # if (w[f][0]['high'] == 'N/A'):
                    #    self.temps[0][0] = '--'
                    # else:
                    #    self.temps[0][0] = w[f][0]['high'] + unichr(0x2109)
                    self.temps[0][0] = str(int(day1.get("temperatureMax")))
                    self.temps[0][1] = str(int(day1.get("temperatureMin")))
                    self.temps[1][0] = str(int(day2.get("temperatureMax")))
                    self.temps[1][1] = str(int(day2.get("temperatureMin")))
                    self.temps[2][0] = str(int(day3.get("temperatureMax")))
                    self.temps[2][1] = str(int(day3.get("temperatureMin")))
                    self.temps[3][0] = str(int(day4.get("temperatureMax")))
                    self.temps[3][1] = str(int(day4.get("temperatureMin")))
            except KeyError:
                print("KeyError -> Weather Error")
                self.temp = '??'
                self.wLastUpdate = ''
                return False
            # except ValueError:
            # print "ValueError -> Weather Error"

            print("done in UpdateWeather")
            return True

    ####################################################################
    def disp_weather(self):
        # print("in disp_weather")
        # Fill the screen with black
        self.screen.fill((0, 0, 0))
        xmin = 0
        xmax = self.xmax
        ymax = self.ymax
        lines = 5
        lc = (255, 255, 255)
        fn = "freesans"

        # print("draw screen border")
        # Draw Screen Border
        pygame.draw.line(self.screen, lc, (xmin, 0), (xmax, 0), lines)
        pygame.draw.line(self.screen, lc, (xmin, 0), (xmin, ymax), lines)
        pygame.draw.line(self.screen, lc, (xmin, ymax), (xmax, ymax), lines)  # Bottom
        pygame.draw.line(self.screen, lc, (xmax, 0), (xmax, ymax + 2), lines)
        pygame.draw.line(self.screen, lc, (xmin, ymax * 0.15), (xmax, ymax * 0.15), lines)
        pygame.draw.line(self.screen, lc, (xmin, ymax * 0.5), (xmax, ymax * 0.5), lines)
        pygame.draw.line(self.screen, lc, (xmax * 0.25, ymax * 0.5), (xmax * 0.25, ymax), lines)
        pygame.draw.line(self.screen, lc, (xmax * 0.5, ymax * 0.15), (xmax * 0.5, ymax), lines)
        pygame.draw.line(self.screen, lc, (xmax * 0.75, ymax * 0.5), (xmax * 0.75, ymax), lines)

        # print("time & date")
        # Time & Date
        th = self.tmdateTh
        sh = self.tmdateSmTh
        font = pygame.font.SysFont(fn, int(ymax * th), bold=1)  # Regular Font
        sfont = pygame.font.SysFont(fn, int(ymax * sh), bold=1)  # Small Font for Seconds

        tm1 = time.strftime("%a, %b %d   %I:%M", time.localtime())  # 1st part
        tm2 = time.strftime("%S", time.localtime())  # 2nd
        tm3 = time.strftime(" %P", time.localtime())  #

        rtm1 = font.render(tm1, True, lc)
        (tx1, ty1) = rtm1.get_size()
        rtm2 = sfont.render(tm2, True, lc)
        (tx2, ty2) = rtm2.get_size()
        rtm3 = font.render(tm3, True, lc)
        (tx3, ty3) = rtm3.get_size()

        tp = xmax / 2 - (tx1 + tx2 + tx3) / 2
        self.screen.blit(rtm1, (tp, self.tmdateYPos))
        self.screen.blit(rtm2, (tp + tx1 + 3, self.tmdateYPosSm))
        self.screen.blit(rtm3, (tp + tx1 + tx2, self.tmdateYPos))

        # print("outside temp")
        # Outside Temp
        font = pygame.font.SysFont(fn, int(ymax * (0.5 - 0.15) * 0.9), bold=1)
        txt = font.render(self.temp, True, lc)
        (tx, ty) = txt.get_size()
        # Show degree F symbol using magic unicode char in a smaller font size.
        dfont = pygame.font.SysFont(fn, int(ymax * (0.5 - 0.15) * 0.5), bold=1)
        dtxt = dfont.render(chr(0x2109), True, lc)
        (tx2, ty2) = dtxt.get_size()
        x = xmax * 0.27 - (tx * 1.02 + tx2) / 2
        self.screen.blit(txt, (x, ymax * 0.15))
        # self.screen.blit( txt, (xmax*0.02,ymax*0.15) )
        x = x + (tx * 1.02)
        self.screen.blit(dtxt, (x, ymax * 0.2))
        # self.screen.blit( dtxt, (xmax*0.02+tx*1.02,ymax*0.2) )

        # print("conditions")
        # Conditions
        st = 0.16  # Yaxis Start Pos
        gp = 0.065  # Line Spacing Gap
        th = 0.06  # Text Height
        dh = 0.05  # Degree Symbol Height
        so = 0.01  # Degree Symbol Yaxis Offset
        xp = 0.52  # Xaxis Start Pos
        x2 = 0.78  # Second Column Xaxis Start Pos

        font = pygame.font.SysFont(fn, int(ymax * th), bold=1)
        txt = font.render('Windchill:', True, lc)
        self.screen.blit(txt, (xmax * xp, ymax * st))
        txt = font.render(str(self.feels_like), True, lc)
        self.screen.blit(txt, (xmax * x2, ymax * st))
        (tx, ty) = txt.get_size()
        # Show degree F symbol using magic unicode char.
        dfont = pygame.font.SysFont(fn, int(ymax * dh), bold=1)
        dtxt = dfont.render(chr(0x2109), True, lc)
        self.screen.blit(dtxt, (xmax * x2 + tx * 1.01, ymax * (st + so)))

        # print("windspeed")
        txt = font.render('Windspeed:', True, lc)
        self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 1)))
        txt = font.render(str(self.wind_speed) + ' mph', True, lc)
        self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 1)))

        # print("direction")
        txt = font.render('Direction:', True, lc)
        self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 2)))
        # print("wind_dir: " + convertWindBearing(self.wind_dir))
        txt = font.render(self.wind_dir, True, lc)
        self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 2)))

        # print("barometer")
        txt = font.render('Barometer:', True, lc)
        self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 3)))
        txt = font.render(str(self.baro) + ' Hg', True, lc)
        self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 3)))

        # print("humidity")
        txt = font.render('Humidity:', True, lc)
        self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 4)))
        txt = font.render(str(self.humid) + '%', True, lc)
        self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 4)))

        wx = 0.125  # Sub Window Centers
        wy = 0.510  # Sub Windows Yaxis Start
        th = self.subwinTh  # Text Height
        rpth = 0.100  # Rain Present Text Height
        gp = 0.065  # Line Spacing Gap
        ro = 0.010 * xmax  # "Rain:" Text Window Offset winthin window.
        rpl = 5.95  # Rain percent line offset.

        font = pygame.font.SysFont(fn, int(ymax * th), bold=1)
        rpfont = pygame.font.SysFont(fn, int(ymax * rpth), bold=1)

        # print("sub window 1")
        # Sub Window 1
        txt = font.render('Today:', True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * wx - tx / 2, ymax * (wy + gp * 0)))
        txt = font.render(self.temps[0][0] + ' / ' + self.temps[0][1], True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * wx - tx / 2, ymax * (wy + gp * 5)))
        # rtxt = font.render( 'Rain:', True, lc )
        # self.screen.blit( rtxt, (ro,ymax*(wy+gp*5)) )
        rptxt = rpfont.render(self.rain[0] + '%', True, lc)
        (tx, ty) = rptxt.get_size()
        self.screen.blit(rptxt, (xmax * wx - tx / 2, ymax * (wy + gp * rpl)))
        icon = pygame.image.load(os.path.join(os.path.abspath(os.getcwd()), 'icons', str(self.icon[0]))).convert_alpha()
        (ix, iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale(icon, (int(ix * 1.5), int(iy * 1.5)))
            (ix, iy) = icon2.get_size()
            icon = icon2
        if iy < 90:
            yo = (90 - iy) / 2
        else:
            yo = 0
        self.screen.blit(icon, (xmax * wx - ix / 2, ymax * (wy + gp * 1.2) + yo))

        # print("sub window 2")
        # Sub Window 2
        txt = font.render(self.day[1] + ':', True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * (wx * 3) - tx / 2, ymax * (wy + gp * 0)))
        txt = font.render(self.temps[1][0] + ' / ' + self.temps[1][1], True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * wx * 3 - tx / 2, ymax * (wy + gp * 5)))
        # self.screen.blit( rtxt, (xmax*wx*2+ro,ymax*(wy+gp*5)) )
        rptxt = rpfont.render(self.rain[1] + '%', True, lc)
        (tx, ty) = rptxt.get_size()
        self.screen.blit(rptxt, (xmax * wx * 3 - tx / 2, ymax * (wy + gp * rpl)))
        # todo
        icon = pygame.image.load(os.path.join(os.path.abspath(os.getcwd()), 'icons', str(self.icon[1]))).convert_alpha()
        (ix, iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale(icon, (int(ix * 1.5), int(iy * 1.5)))
            (ix, iy) = icon2.get_size()
            icon = icon2
        if (iy < 90):
            yo = (90 - iy) / 2
        else:
            yo = 0
        self.screen.blit(icon, (xmax * wx * 3 - ix / 2, ymax * (wy + gp * 1.2) + yo))

        # print("sub window 3")
        # Sub Window 3
        txt = font.render(self.day[2] + ':', True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * (wx * 5) - tx / 2, ymax * (wy + gp * 0)))
        txt = font.render(self.temps[2][0] + ' / ' + self.temps[2][1], True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * wx * 5 - tx / 2, ymax * (wy + gp * 5)))
        # self.screen.blit( rtxt, (xmax*wx*4+ro,ymax*(wy+gp*5)) )
        rptxt = rpfont.render(self.rain[2] + '%', True, lc)
        (tx, ty) = rptxt.get_size()
        self.screen.blit(rptxt, (xmax * wx * 5 - tx / 2, ymax * (wy + gp * rpl)))
        # todo
        icon = pygame.image.load(os.path.join(os.path.abspath(os.getcwd()), 'icons', str(self.icon[2]))).convert_alpha()
        (ix, iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale(icon, (int(ix * 1.5), int(iy * 1.5)))
            (ix, iy) = icon2.get_size()
            icon = icon2
        if (iy < 90):
            yo = (90 - iy) / 2
        else:
            yo = 0
        self.screen.blit(icon, (xmax * wx * 5 - ix / 2, ymax * (wy + gp * 1.2) + yo))

        # print("sub window 4")
        # Sub Window 4
        txt = font.render(self.day[3] + ':', True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * (wx * 7) - tx / 2, ymax * (wy + gp * 0)))
        txt = font.render(self.temps[3][0] + ' / ' + self.temps[3][1], True, lc)
        (tx, ty) = txt.get_size()
        self.screen.blit(txt, (xmax * wx * 7 - tx / 2, ymax * (wy + gp * 5)))
        # self.screen.blit( rtxt, (xmax*wx*6+ro,ymax*(wy+gp*5)) )
        rptxt = rpfont.render(self.rain[3] + '%', True, lc)
        (tx, ty) = rptxt.get_size()
        self.screen.blit(rptxt, (xmax * wx * 7 - tx / 2, ymax * (wy + gp * rpl)))
        # todo
        icon = pygame.image.load(os.path.join(os.path.abspath(os.getcwd()), 'icons', str(self.icon[3]))).convert_alpha()
        (ix, iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale(icon, (int(ix * 1.5), int(iy * 1.5)))
            (ix, iy) = icon2.get_size()
            icon = icon2
        if (iy < 90):
            yo = (90 - iy) / 2
        else:
            yo = 0
        self.screen.blit(icon, (xmax * wx * 7 - ix / 2, ymax * (wy + gp * 1.2) + yo))

        # print("update the display")
        # Update the display
        pygame.display.update()
        # print("done in disp_weather")

    ####################################################################
    def sPrint(self, s, font, x, l, lc):
        f = font.render(s, True, lc)
        self.screen.blit(f, (x, self.ymax * 0.075 * l))
