import shapely.geometry as geometry
import sqlite3
import datetime


def createBase(cursor):
  cursor.execute(
    """
    CREATE TABLE if not exists cam7
      (
        ID INTEGER PRIMARY KEY,
        FileName TEXT,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        Горького INTEGER,
        Рабочекрестьянская INTEGER,
        Пушкина INTEGER,
        Хлебокомбинат INTEGER
      )
    """)

def analysis(objects, fileName, timestamp):
  roadParts = {
    "Горького": [
      [1,768],
      [58,870],
      [197,806],
      [421,607],
      [450,468],
      [253,456],
      [118,451],
      [42,453],
      [0,464]
    ],
    "Рабочекрестьянская": [
      [0,1076],
      [1355,1076],
      [1189,858],
      [369,839],
      [191,829],
      [43,881]
    ],
    "Пушкина": [
      [1121,622],
      [1196,820],
      [1581,805],
      [1908,759],
      [1806,486],
      [1132,500]
    ],
    "Хлебокомбинат": [
      [448,602],
      [464,434],
      [686,337],
      [1004,327],
      [1104,620]
    ]
  }

  counter = {
    "Горького": 0,
    "Рабочекрестьянская": 0,
    "Пушкина": 0,
    "Хлебокомбинат": 0
  }

  trackingData = {}

  for name in objects:
    obj = objects[name]
    centerIndex = len(obj) // 2
    halfs = [[], []]
    for frame in obj:
      index = obj.index(frame)
      dimensions = frame["dimensions"]
      if (index <= centerIndex):
        halfs[0].append(dimensions)
      else:
        halfs[1].append(dimensions)

    trajectory = []

    if not len(halfs[0]) or not len(halfs[1]): 
      continue

    if len(halfs[0]) > 1:
      trajectory.append(geometry.LineString(halfs[0]))
    else:
      trajectory.append(geometry.Point(halfs[0][0]))

    if len(halfs[1]) > 1:
      trajectory.append(geometry.LineString(halfs[1]))
    else:
      trajectory.append(geometry.Point(halfs[1][0]))

    trackingData[name] = {
      "directions": [
        "",
        ""
      ]
    }

    for nameDirection in roadParts:
      direction = roadParts[nameDirection]
      directionHanlder = geometry.Polygon(direction)
      if (trajectory[0].intersects(directionHanlder)):
        trackingData[name]["directions"][0] = nameDirection;
      if (trajectory[1].intersects(directionHanlder)):
        trackingData[name]["directions"][1] = nameDirection;
        counter[nameDirection] += 1
  
  conn = sqlite3.connect("analysis.db")
  cursor = conn.cursor()

  createBase(cursor)
  
  inserting = ("INSERT INTO cam7 ( FileName, Timestamp, Горького, Рабочекрестьянская, Пушкина, Хлебокомбинат ) VALUES( \"" 
                + str(fileName) + "\", \""
                + str(timestamp) + "\", "
                + str(counter["Горького"]) + ", "
                + str(counter["Рабочекрестьянская"]) + ", "
                + str(counter["Пушкина"]) + ", "
                + str(counter["Хлебокомбинат"]) + " )")
  
  print(inserting)
  
  cursor.execute(inserting)
  conn.commit()
  conn.close()