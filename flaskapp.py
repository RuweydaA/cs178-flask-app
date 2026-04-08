## author: Ruweyda Abdi (starter code by T. Urness and M. Moore)
# description: employee customer directory flask App using MySQL (RDS) and DynamoDB


import boto3

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')                                    

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            name = request.form['name']
            major = request.form['major']
            table.put_item(Item={
                'UserID': user_id,
                'Name': name,
                'Major': major
            })
            flash('User added successfully! Huzzah!', 'success')
            return redirect(url_for('display_users'))
        except Exception as e:
            flash(f'Error adding user: {e}', 'error')
    return render_template('add_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            table.delete_item(Key={'UserID': user_id})
            flash('User deleted successfully! Hoorah!', 'warning')
            return redirect(url_for('display_users'))
        except Exception as e:
            flash(f'Error deleting user: {e}', 'error')
    return render_template('delete_user.html')

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            new_major = request.form['major']
            table.update_item(
                Key={'UserID': user_id},
                UpdateExpression='SET Major = :m',
                ExpressionAttributeValues={':m': new_major}
            )
            flash('User updated successfully!', 'success')
            return redirect(url_for('display_users'))
        except Exception as e:
            flash(f'Error updating user: {e}', 'error')
    return render_template('update_user.html')

@app.route('/display-users')
def display_users():
    try:
        response = table.scan()
        users = response.get('Items')
    except Exception as e:
        flash(f'Error fetching users: {e}', 'error')
        users = []
    return render_template('display_users.html', users=users)

#question 6
#SELECT Employee.FirstName, Employee.LastName, Employee.Title,
#Customer.FirstName AS CustFirst, Customer.LastName AS CustLast
#FROM Employee
#JOIN Customer ON Employee.EmployeeId = Customer.SupportRepId
#LIMIT 50;

@app.route('/employee-customer')
def employee_customer():
    try:
        query = """
            SELECT Employee.FirstName, Employee.LastName, Employee.Title,
            Customer.FirstName AS CustFirst, Customer.LastName AS CustLast
            FROM Employee
            JOIN Customer ON Employee.EmployeeId = Customer.SupportRepId
            LIMIT 50;
        """
        rows = execute_query(query)
        return render_template('employee_customer.html', rows=rows)
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/testdb')
def testdb():
    rows = execute_query("SELECT * FROM Artist LIMIT 10;")
    return str(rows)

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
