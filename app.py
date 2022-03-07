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
        predictor = utils.Predictor(api_key='AIzaSyByI4h7HRINmQOKjl92TgtPm9S672qT_tU',
                                    url='https://vision.googleapis.com/v1/images:annotate')
        json_data = request.get_json(force=True)
        img_uri = json_data['uri']
        img_numpy = predictor.readb64(img_uri)

        response1 = predictor.sendRequest(img_numpy)
        text1 = predictor.responseToText(response1)
        operation = predictor.findOperation(text1)
        for index, i in enumerate(text1):
            if i.isnumeric():
                question = text1[:index]
                break

        processed_img = predictor.getProcessedImg(img_numpy)
        response2 = predictor.sendRequest(processed_img)
        text2 = predictor.responseToText(response2)
        values = predictor.getVals(text2, operation)

        question = question.strip() + str(values)

        final_output = predictor.findResult(values, operation)

        return jsonify(message="success", question=question, result=final_output)


api.add_resource(Predict, '/predict')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run()
