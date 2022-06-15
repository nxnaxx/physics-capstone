import cv2
import pyzbar.pyzbar as pyzbar
import requests

url = "http://192.168.137.1:3000/items"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

if __name__ == '__main__':
  try:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 7)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while (cap.isOpened()):
      ret, img = cap.read()

      # convert to gray scale images
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      # detect a barcode
      decoded = pyzbar.decode(gray)
      
      for d in decoded:
        x, y, w, h = d.rect
        barcode_data = d.data.decode("utf-8")
        print(barcode_data)
        data = {'barcode': barcode_data}

        r = requests.post(url + "?barcode=" + barcode_data, data=data, headers=headers)
        print(r)
        
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(img, barcode_data, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

      cv2.imshow('Barcode Reader', img)
      
      key = cv2.waitKey(10)
      if key == 27:
        break
      
  except KeyboardInterrupt:
    pass

cap.release()
cv2.destroyAllWindows()