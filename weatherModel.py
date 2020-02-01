class weatherModel:
    lastUpdate = 0
    temp = 0
    feelsLike = 0
    windSpeed = 0
    windGust = 0
    barometer = 0
    humidity = 0
    visibility = 0
    windBearing = 0.0

    def __init__(self, lastUpdate, temp, feelsLike, windSpeed, windGust, barometer, humidity, visibility, windBearing):
        self.lastUpdate = lastUpdate
        self.temp = temp
        self.feelsLike = feelsLike
        self.windSpeed = windSpeed
        self.windGust = windGust
        self.barometer = barometer
        self.humidity = humidity
        self.visibility = visibility
        self.windBearing = windBearing

    def __str__(self):
        return "\nlastUpdate: " + str(self.lastUpdate) + \
                "\ntemp: " + str(self.temp) + \
                "\nfeelsLike: " + str(self.feelsLike) + \
                "\nwindSpeed: " + str(self.windSpeed) + \
                "\nwindGust: " + str(self.windGust) + \
                "\nbarometer: " + str(self.barometer) + \
                "\nhumidity: " + str(self.humidity) + \
                "\nvisibility: " + str(self.visibility) + \
                "\nwindBearing: " + str(self.windBearing) + \
                "\n"
