import time
import pygame
import logging
from SmDisplay import SmDisplay
logging.basicConfig(filename='err.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


if __name__ == "__main__":
    try:
        myDisp = SmDisplay()

        running = True  # Stay running while True
        s = 0
        m = 0

        while running:
            if s != time.localtime().tm_sec:
                s = time.localtime().tm_sec
                m = time.localtime().tm_min
                myDisp.disp_weather()
            # Once the screen is updated, we have a full 2 minutes to get the weather.
            # Every even minute, update the weather from the net.
            if m % 2 == 0 and s == 0:
                myDisp.UpdateWeather()

            # Loop timer.
            pygame.time.wait(1000)

        pygame.quit()
    except Exception as ex:
        logging.error("Exception: " + str(ex))
