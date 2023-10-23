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
        address_line1 = request.form['address_line1']
        borough = request.form['borough']
        zip = request.form['zip']
        description = request.form['description']
        cost = request.form['cost']
        sunday_hours = request.form['sunday_hours']
        monday_hours = request.form['monday_hours']
        tuesday_hours = request.form['tuesday_hours']
        wednesday_hours = request.form['wednesday_hours']
        thursday_hours = request.form['thursday_hours']
        friday_hours = request.form['friday_hours']
        saturday_hours = request.form['saturday_hours']
        # You can also handle the uploaded file if necessary

        # Create a dictionary with the data
        restaurant_data = {
            "restaurant_name": restaurant_name,
            "address_line1": address_line1,
            "borough": borough,
            "zip": zip,
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
        print("**** rest ", restaurant_data)
        # Insert the data into the MongoDB collection
        collection.insert_one(restaurant_data)
        # Redirect to a thank you page or a page of your choice
        message = "Restaurant data submitted successfully."
        return render_template('pages/response.html', message=message)

@app.route('/add', methods=['GET'])
def show_add_restaurant_form():
    return render_template('pages/addresturant.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_restaurant():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant_name')
        adminid = request.form.get('adminid')
        
        # Check if the adminid matches the expected value
        if adminid == "plantmaster":
            # Check if the restaurant exists in the MongoDB collection
            restaurant = collection.find_one({"restaurant_name": restaurant_name})
            if restaurant:
                # Delete the restaurant document
                collection.delete_one({"restaurant_name": restaurant_name})
                message = "Restaurant deleted successfully."
                return render_template('pages/response.html', message=message)

            else:
                message = "Restaurant not found. Check submitted restaurant name for typos."
                return render_template('pages/response.html', message=message)
        else:
            return render_template('pages/response.html', message=message)

    return render_template('pages/deleterestaurant.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit_restaurant():
    message = None

    if request.method == 'POST':
        # Get the restaurant_name from the form
        restaurant_name = request.form['restaurant_name']

        # Check if the restaurant exists
        existing_restaurant = collection.find_one({"restaurant_name": restaurant_name})
        if existing_restaurant:
            # Define the updates you want to make based on user input
            updates = {}

            # Iterate through the fields of existing_restaurant and update the updates dictionary
            for field in existing_restaurant:
                form_input = request.form.get(field)
                if form_input is not None and form_input != "":
                    updates[field] = form_input
                else:
                    updates[field] = existing_restaurant[field]

            # Update new name, if included
            updates["restaurant_name"] = request.form.get('new_name')

            # Update the document in the MongoDB collection
            collection.update_one({"restaurant_name": restaurant_name}, {"$set": updates})
            message = "Restaurant updated successfully."
            return render_template('pages/response.html', message=message)

        else:
            message = "Restaurant not found. Please check the restaurant name."
            return render_template('pages/response.html', message=message)

    return render_template('pages/edit.html')

@app.route('/', methods=['GET'])
def show_all():
    # Retrieve all documents from the MongoDB collection
    restaurants = list(collection.find({}))

    # Get the selected borough from the form
    selected_borough = request.args.get('borough', 'all').lower()

    # Render an HTML template to display the list of restaurants
    return render_template('pages/home.html', restaurants=restaurants, selected_borough=selected_borough)

@app.route('/search', methods=['GET'])
def search_restaurants():
    # Get the search term from the form
    selected_name = request.args.get('search', '')
    # Define a query to search for restaurants with names matching the selected_name
    query = {"restaurant_name": selected_name}
    # Retrieve documents from the MongoDB collection that match the query
    restaurants = list(collection.find(query))
    # Render an HTML template to display the list of restaurants
    return render_template('pages/search.html', restaurants=restaurants, selected_borough='all', selected_name=selected_name)

@app.route('/filter', methods=['GET'])
def filter():
    # # Get the search term from the form
    restaurants = list(collection.find({}))
    selected_borough = request.args.get('borough', 'all').lower()
    selected_cost = request.args.get('cost', 'all')
    return render_template('pages/filter.html', restaurants=restaurants, selected_borough=selected_borough, selected_cost=selected_cost)


if __name__ == '__main__':
    app.run(debug=True)