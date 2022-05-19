import pyzbar.pyzbar as pyzbar  # barcode, QR code 인식 라이브러리
import cv2  # OpenCV 영상인식 라이브러리
# import matplotlib.pyplot as plt  # matplotlib 그래프 라이브러리
import requests
 
url = "http://localhost:8000"
#url = "http://192.168.0.147:8000"

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

cap = cv2.VideoCapture(0)

i = 0
while(cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    decoded = pyzbar.decode(gray)

    for d in decoded:
        x, y, w, h = d.rect

        barcode_data = d.data.decode("utf-8")  # 바코드, QR코드 URL
        barcode_type = d.type
        
        data = {'barcode': barcode_data}

        r = requests.post(url, data=data, headers=headers)

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        text = '%s (%s)' % (barcode_data, barcode_type)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        i += 1
        cv2.imwrite('c_%03d.jpg' % i, img)

cap.release()
cv2.destroyAllWindows()
