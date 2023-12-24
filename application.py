from flask import Flask,request,render_template,jsonify
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline


application=Flask(__name__)

app=application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        # Get form values
        carat = request.form.get('carat')
        depth = request.form.get('depth')
        table = request.form.get('table')
        x = request.form.get('x')
        y = request.form.get('y')
        z = request.form.get('z')
        cut = request.form.get('cut')
        color = request.form.get('color')
        clarity = request.form.get('clarity')

        # Check if required fields are not empty
        if None in [carat, depth, table, x, y, z, cut, color, clarity]:
            return render_template('form.html', final_result="Please fill out all fields.")

        # Create CustomData object
        data = CustomData(
            carat=float(carat),
            depth=float(depth),
            table=float(table),
            x=float(x),
            y=float(y),
            z=float(z),
            cut=cut,
            color=color,
            clarity=clarity
        )

        # Get data as a DataFrame
        final_new_data = data.get_data_as_dataframe()

        # Use PredictPipeline to make predictions
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        # Display the prediction result
        results = round(pred[0], 2)

        return render_template('form.html', final_result=results)

    

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
    

# http://127.0.0.1:5000
# http://127.0.0.1:5000/predict
