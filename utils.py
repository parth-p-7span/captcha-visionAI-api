import json
import base64
import cv2
import requests
import numpy as np


class Predictor:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        # self.image_base64 = image_base64

    def readb64(self, image):
        nparr = np.frombuffer(base64.b64decode(image), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def findOperation(self, responseString):
        if 'sum' in responseString:
            return 'sum'
        if 'min' in responseString:
            return 'min'
        if 'max' in responseString:
            return 'max'
        return ''

    def getProcessedImg(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_OTSU)
        krn = np.ones((3, 3), np.uint8)
        img_dilated = cv2.dilate(cv2.bitwise_not(thresh), kernel=krn, iterations=1)
        return img_dilated

    def sendRequest(self, img):
        string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

        img_req = {
            'image': {
                'content': string
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
        imgdata = json.dumps({"requests": img_req}).encode()

        result = requests.post(self.url,
                               data=imgdata,
                               params={'key': self.api_key},
                               headers={'Content-Type': 'application/json'})

        return result

    def responseToText(self, response):
        if response.status_code != 200 or response.json().get('error'):
            print("Error")
            return "error"
        else:
            result = response.json()['responses'][0]['textAnnotations'][0]['description']
            return result

    def changeItems(self, list):
        return [int(i.strip()) for i in list]

    def findResult(self, vals, operation):
        if operation == 'sum':
            return sum(vals)
        else:
            vals.sort()
            return vals[0] if (operation == 'min') else vals[-1]

    def getVals(self, responseText, operation):
        if operation == 'sum':
            for index, i in enumerate(responseText):
                if i.isnumeric():
                    vals = responseText[index:]
                    vals = vals.strip().split("&")
                    final_vals = self.changeItems(vals)
                    return final_vals
        else:
            for index, i in enumerate(responseText):
                if i.isnumeric():
                    vals = responseText[index:]
                    vals = vals.strip().split(",")
                    final_vals = self.changeItems(vals)
                    return final_vals
