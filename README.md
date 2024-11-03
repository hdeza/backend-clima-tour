# Temperature Prediction Project

This project utilizes a machine learning model to predict temperature based on various weather features. It has been implemented using Django and Django REST Framework to create an API that allows POST requests to obtain predictions.

## Table of Contents
- [General Description](#general-description)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Contributions](#contributions)
- [License](#license)

## General Description

- **Imports**: Essential modules are imported for file handling, model loading, and API view creation.
- **Model Loading**: The path to the prediction model is established and loaded using joblib.
- **Class `PrediccionTemperatura`**: This class handles POST requests for temperature predictions.
- **Method `post`**: This method processes the request, extracts the data, validates it, performs the prediction, and returns the result or an error if something fails.

### Workflow

1. **Receives Request**: The class listens for POST requests.
2. **Extracts Data**: Retrieves the necessary data from the request body.
3. **Validates Data**: Checks that all required data is present.
4. **Performs Prediction**: Uses the loaded model to make a temperature prediction.
5. **Returns Result**: Sends the prediction as a JSON response, or an error message if something goes wrong.

## Technologies Used

- Python
- Django
- Django REST Framework
- Joblib (for loading the machine learning model)

## Installation

To install and run the project, follow the steps below:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hdeza/backend-clima-tour.git
   cd backend-clima-tour
2. Create a virtual environment (optional but recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
 ```
4. Run migrations:
 ```bash
  python manage.py migrate
 ```
5. Start the server:
 ```bash
  python manage.py runserver
 ```
## Usage

To make a temperature prediction, send a POST request to the API with the following parameters in JSON format:
 ```json
  {
  "tavg": <value>,
  "tmin": <value>,
  "tmax": <value>,
  "prcp": <value>,
  "wdir": <value>,
  "wspd": <value>,
  "pres": <value>,
  "latitude": <value>,
  "longitude": <value>
}
 ```
### Example request using curl:
 ```bash
 curl -X POST http://localhost:8000/api/prediction/ -H "Content-Type: application/json" -d '{"tavg": 25, "tmin": 20, "tmax": 30, "prcp": 5, "wdir": 180, "wspd": 10, "pres": 1010, "latitude": 10.0, "longitude": -74.0}'
 ```
The response will be a JSON containing the predicted temperature:
 ```json
  {
  "predicted_temperature": <value>
}
 ```

## Contributions

Contributions are welcome. Please open an issue or submit a pull request to discuss changes you would like to make.

## License 

This project is licensed under the MIT License. See the LICENSE file for more details.
 ```vbnet
  Feel free to copy and paste this content into a `README.md` file at the root of your project. If you need further modifications or additional sections, just let me know!
 ```





