import shapely.geometry as geometry

def parseFile(file_name):
  data = open("./tracker_output/" + file_name + ".csv", 'r')
  objects = {}
  for row in data:
    objectData = row.split(',')
    frame = objectData[0]
    number = objectData[1]
    class_name =  objectData[2]
    dimensions = [
      float(objectData[3]),
      float(objectData[4]),
    ]

    objectInfo = {
      "frame": frame,
      "dimensions": dimensions,
    };

    if class_name + number in objects.keys():
      objects[class_name + number].append(objectInfo)
    else:
      objects[class_name + number] = [
        objectInfo
      ]
    
  return objects


def analysis(file_name, roadParts):
  objects = parseFile(file_name)

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