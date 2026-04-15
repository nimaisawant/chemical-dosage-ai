from flask import Flask, render_template, request
import pickle
import json

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        pH = float(request.form['pH'])
        turbidity = float(request.form['turbidity'])
        temp = float(request.form['temp'])

        prediction = model.predict([[pH, turbidity, temp]])
        dosage = round(prediction[0], 2)

        # Status logic
        if dosage < 4:
            status = "Safe Water ✅"
        elif dosage <= 8:
            status = "Moderate Treatment ⚠️"
        else:
            status = "Unsafe Water ❌"

        # Explanation
        explanation = []

        if turbidity > 5:
            explanation.append("High turbidity increased chlorine demand")
        else:
            explanation.append("Low turbidity required less chlorine")

        if pH < 6.5 or pH > 8.5:
            explanation.append("pH is far from neutral, requiring more treatment")
        else:
            explanation.append("pH is near neutral, reducing chlorine need")

        if temp > 30:
            explanation.append("Higher temperature speeds reactions slightly increasing dosage")
        else:
            explanation.append("Normal temperature has moderate effect")

        # Graph data
        turbidity_values = [turbidity-2, turbidity-1, turbidity, turbidity+1, turbidity+2]
        turbidity_values = [max(0, t) for t in turbidity_values]
        turbidity_dosage = [round(model.predict([[pH, t, temp]])[0], 2) for t in turbidity_values]

        ph_values = [pH-1, pH-0.5, pH, pH+0.5, pH+1]
        ph_values = [max(0, min(14, p)) for p in ph_values]
        ph_dosage = [round(model.predict([[p, turbidity, temp]])[0], 2) for p in ph_values]

        temp_values = [temp-5, temp-2, temp, temp+2, temp+5]
        temp_values = [max(0, t) for t in temp_values]
        temp_dosage = [round(model.predict([[pH, turbidity, t]])[0], 2) for t in temp_values]

        return render_template(
            'index.html',
            result=dosage,
            status=status,
            explanation=explanation,
            turbidity_data=json.dumps(turbidity_values),
            dosage_data=json.dumps(turbidity_dosage),
            ph_data=json.dumps(ph_values),
            ph_dosage=json.dumps(ph_dosage),
            temp_data=json.dumps(temp_values),
            temp_dosage=json.dumps(temp_dosage),

            # Keep values
            input_ph=pH,
            input_turbidity=turbidity,
            input_temp=temp
        )

    except:
        return render_template('index.html', error="Invalid input")


# 🔥 IMPORTANT FOR DEPLOYMENT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)