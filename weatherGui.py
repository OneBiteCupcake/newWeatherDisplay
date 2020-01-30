import pygame
import time
import string
from icon_defs import *


def disp_weather(self):
    # Fill the screen with black
    self.screen.fill((0, 0, 0))
    xmin = 0
    xmax = self.xmax
    ymax = self.ymax
    lines = 5
    lc = (255, 255, 255)
    fn = "freesans"

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
    txt = font.render(self.feels_like, True, lc)
    self.screen.blit(txt, (xmax * x2, ymax * st))
    (tx, ty) = txt.get_size()
    # Show degree F symbol using magic unicode char.
    dfont = pygame.font.SysFont(fn, int(ymax * dh), bold=1)
    dtxt = dfont.render(chr(0x2109), True, lc)
    self.screen.blit(dtxt, (xmax * x2 + tx * 1.01, ymax * (st + so)))

    txt = font.render('Windspeed:', True, lc)
    self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 1)))
    txt = font.render(self.wind_speed + ' mph', True, lc)
    self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 1)))

    txt = font.render('Direction:', True, lc)
    self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 2)))
    txt = font.render(string.upper(self.wind_dir), True, lc)
    self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 2)))

    txt = font.render('Barometer:', True, lc)
    self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 3)))
    txt = font.render(self.baro + ' Hg', True, lc)
    self.screen.blit(txt, (xmax * x2, ymax * (st + gp * 3)))

    txt = font.render('Humidity:', True, lc)
    self.screen.blit(txt, (xmax * xp, ymax * (st + gp * 4)))
    txt = font.render(self.humid + '%', True, lc)
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
    icon = pygame.image.load(sd + icons[self.icon[0]]).convert_alpha()
    (ix, iy) = icon.get_size()
    if self.scaleIcon:
        icon2 = pygame.transform.scale(icon, (int(ix * 1.5), int(iy * 1.5)))
        (ix, iy) = icon2.get_size()
        icon = icon2
    if (iy < 90):
        yo = (90 - iy) / 2
    else:
        yo = 0
    self.screen.blit(icon, (xmax * wx - ix / 2, ymax * (wy + gp * 1.2) + yo))

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
    icon = pygame.image.load(sd + icons[self.icon[1]]).convert_alpha()
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
    icon = pygame.image.load(sd + icons[self.icon[2]]).convert_alpha()
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
    icon = pygame.image.load(sd + icons[self.icon[3]]).convert_alpha()
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

    # Update the display
    pygame.display.update()