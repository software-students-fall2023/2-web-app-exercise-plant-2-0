import pymongo
# from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__, template_folder='../templates')

connection = pymongo.MongoClient('mongodb+srv://plant2:plant2@cluster0.ttioiyj.mongodb.net/')

db = connection["project"]

collection = db["restaurants"]

@app.route('/add', methods=['POST'])
def submit_new_restaurant():
    if request.method == 'POST':
        # Retrieve data from the submitted form
        restaurant_name = request.form['restaurant_name']
        address_line1 = request.form['ad1']
        borough = request.form['borough']
        zip_code = request.form['zip']
        description = request.form['desc']
        cost = request.form['cost']
        sunday_hours = request.form['sundayhours']
        monday_hours = request.form['mondayhours']
        tuesday_hours = request.form['tuesdayhours']
        wednesday_hours = request.form['wednesdayhours']
        thursday_hours = request.form['thursdayhours']
        friday_hours = request.form['fridayhours']
        saturday_hours = request.form['saturdayhours']
        # You can also handle the uploaded file if necessary

        # Create a dictionary with the data
        restaurant_data = {
            "restaurant_name": restaurant_name,
            "address_line1": address_line1,
            "borough": borough,
            "zip_code": zip_code,
            "description": description,
            "cost": cost,
            "sunday_hours": sunday_hours,
            "monday_hours": monday_hours,
            "tuesday_hours": tuesday_hours,
            "wednesday_hours": wednesday_hours,
            "thursday_hours": thursday_hours,
            "friday_hours": friday_hours,
            "saturday_hours": saturday_hours
        }

        # Insert the data into the MongoDB collection
        collection.insert_one(restaurant_data)
        # Redirect to a thank you page or a page of your choice
        return "Restaurant data submitted successfully."

@app.route('/add', methods=['GET'])
def show_add_restaurant_form():
    return render_template('pages/addresturant.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_restaurant():
    if request.method == 'POST':
        restaurantID = request.form.get('restaurantID')
        adminid = request.form.get('adminid')
        
        # Check if the adminid matches the expected value
        if adminid == "plantmaster":
            # Check if the restaurant exists in the MongoDB collection
            restaurant = collection.find_one({"restaurant_name": restaurantID})
            if restaurant:
                # Delete the restaurant document
                collection.delete_one({"restaurant_name": restaurantID})
                return "Restaurant deleted successfully."
            else:
                return "Restaurant not found."
        else:
            return "Access denied. Admin code is incorrect."

    return render_template('pages/deleterestaurant.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit_restaurant():
    error_message = None

    if request.method == 'POST':
        # Get the restaurant_name from the form
        restaurant_name = request.form['restaurant_name']

        # Check if the restaurant exists
        existing_restaurant = collection.find_one({"restaurant_name": restaurant_name})

        if existing_restaurant:
            # Define the updates you want to make based on user input
            updates = {
                "address_line1": request.form['ad1'],
                "borough": request.form['borough'],
                "zip_code": request.form['zip'],
                "description": request.form['desc'],
                "cost": request.form['cost'],
                "sunday_hours": request.form['sundayhours'],
                "monday_hours": request.form['mondayhours'],
                "tuesday_hours": request.form['tuesdayhours'],
                "wednesday_hours": request.form['wednesdayhours'],
                "thursday_hours": request.form['thursdayhours'],
                "friday_hours": request.form['fridayhours'],
                "saturday_hours": request.form['saturdayhours']
            }

            # Update the document in the MongoDB collection
            collection.update_one({"restaurant_name": restaurant_name}, {"$set": updates})

            return "Restaurant updated successfully."
        else:
            error_message = "Restaurant not found. Please check the restaurant name."

    return render_template('pages/edit.html', error_message=error_message)

@app.route('/', methods=['GET'])
def show_all():
    # Retrieve all documents from the MongoDB collection
    restaurants = list(collection.find({}))

    # Get the selected borough from the form
    selected_borough = request.args.get('borough', 'all')

    # Render an HTML template to display the list of restaurants
    return render_template('pages/home.html', restaurants=restaurants, selected_borough=selected_borough)

@app.route('/search', methods=['GET'])
def search_restaurants():
    # Get the search term from the form
    selected_name = request.args.get('search', '')

    # Define a query to search for restaurants with names matching the selected_name
    query = {"restaurant_name": selected_name}
    print("**** selected: ", selected_name)
    # Retrieve documents from the MongoDB collection that match the query
    restaurants = list(collection.find(query))
    print("*****  ", restaurants)
    # Render an HTML template to display the list of restaurants
    return render_template('pages/search.html', restaurants=restaurants, selected_borough='all', selected_name=selected_name)

if __name__ == '__main__':
    app.run(debug=True)