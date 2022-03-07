from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import utils

app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return jsonify(message="captcha ocr demo endpoint...")

class Predict(Resource):
    def get(self):
        return jsonify(message="send a post request...")

    def post(self):
        json_data = request.get_json(force=True)
        img_uri = json_data['uri']
        
        predictor = utils.Predictor(api_key='AIzaSyByI4h7HRINmQOKjl92TgtPm9S672qT_tU',
                                url='https://vision.googleapis.com/v1/images:annotate')
        
        img_numpy = predictor.readb64(img_uri)

        response1 = predictor.sendRequest(img_numpy)
        text1 = predictor.responseToText(response1)
        operation = predictor.findOperation(text1)

        processed_img = predictor.getProcessedImg(img_numpy)
        response2 = predictor.sendRequest(processed_img)
        text2 = predictor.responseToText(response2)
        values = predictor.getVals(text2, operation)

        final_output = predictor.findResult(values,operation)

        return jsonify(message="success", result=final_output)


api.add_resource(Predict, '/predict')
api.add_resource(Index, '/')

if __name__ == '__main__':    
    app.run()
