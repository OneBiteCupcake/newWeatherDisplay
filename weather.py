import time, pygame
from SmDisplay import SmDisplay


if __name__ == "__main__":
    myDisp = SmDisplay()

    running = True  # Stay running while True
    s = 0
    m = 0

    while running:
        # print("in while")

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # On 'q' or keypad enter key, quit the program.
                if (event.key == pygame.K_KP_ENTER) or (event.key == pygame.K_q):
                    running = False

        if s != time.localtime().tm_sec:
            s = time.localtime().tm_sec
            m = time.localtime().tm_min
            print("m: " + str(m))
            # print('in if')
            # print("before calling disp_weather")
            myDisp.disp_weather()
        # ser.write( "Weather\r\n" )
        # Once the screen is updated, we have a full second to get the weather.
        # Once per minute, update the weather from the net.
        # print("s: " + str(s))
        if s == 0:
            # print('in else')
            # print("before calling UpdateWeather")
            myDisp.UpdateWeather()

        # print("before calling time.wait")
        # Loop timer.
        pygame.time.wait(1000)

    pygame.quit()
    # else:
    #    raise Exception("To err is human to forgive divine.")
