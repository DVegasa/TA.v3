import shapely.geometry as geometry

def analysis(objects):
  
  roadParts = {
    "влево": [
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
    "вниз": [
      [0,1076],
      [1355,1076],
      [1189,858],
      [369,839],
      [191,829],
      [43,881]
    ],
    "вправо": [
      [1121,622],
      [1196,820],
      [1581,805],
      [1908,759],
      [1806,486],
      [1132,500]
    ],
    "вверх": [
      [448,602],
      [464,434],
      [686,337],
      [1004,327],
      [1104,620]
    ]
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
  
  print(trackingData)