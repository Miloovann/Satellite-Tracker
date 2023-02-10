
gs100 = "projected.txt" ## file with lon, lat, az, el
with open(gs100, "r") as f:
    x = f.read().replace("\00", "").split("Timestamp: ")
    az, el, lat, lon = [], [], [], []
    for txt in x:
        if len(txt) > 0:
            clean = txt[txt.find("AZ: ") + 4 : txt.find(", RX: ")]
            az.append(float(clean[ : clean.find(",")]))
            el.append(float(clean[clean.find(",")+6 : ]))

            clean2 = txt[txt.find("Latitude: ") + 10 : txt.find(", Altitude:")]
            lat.append(float(clean2[ : clean2.find(",")]))
            lon.append(float(clean2[clean2.find(",")+13 : ]))
