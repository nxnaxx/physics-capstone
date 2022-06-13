from rplidar import RPLidar
import time
lidar = RPLidar('/dev/ttyUSB0')

try :
  for i, scan in enumerate(lidar.iter_scans()):
    if int(len(scan)) >= 150:
      break
    print('%d: Got %d measurments' % (i, len(scan)))
  print('too long!')
except KeyboardInterrupt:
  pass

lidar.stop_motor()
lidar.stop()
lidar.disconnect()