# Environment setup
1. Create a virtual environment using 
```python
python -m venv venv
```
2. Activate the virtual environment using following command<br>

for windows
```
venv\Scripts\activate
```
<br>
for Ubuntu or similar

```
source venv/bin/activate
```
3. Install the required dependencies
```
pip install -r requirements.txt
```
4. Make migrations and Run the project
```
python manage.py makemigrations
python manage.py migrate

python manager.py runserver
```

<br><br>
# API Documentaion ###

# sign up
`POST` method endpoint: 

http://127.0.0.1:8000/api/v1/accounts/signup/

Data
```
post_data = {
    "name" : "your/company name",
    "email" : "your email",
    "password" : "your password with minimum length of 8"
}
```
response with `status: 201`
```
{
  "message": "User created",
  "data": {
    "name":  "your name",
    "email": "your email"
  }
}
```

response with `status: 400` if email already registered
```
{
  "non_field_errors": [
    "Email has already been used"
  ]
}
```

# login

`POST` method endpoint: 

http://127.0.0.1:8000/api/v1/accounts/login/

Data
```
post_data = {
    "username": "your registered email",
    "password": "your password"
}
```
response with `status: 200` if authenticated
```
{
  "token": "generated token for authorization to access data"
}
```

response with `status: 400` if not authenticated
```
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

<br><br>

From now we have to use `Authorization` in the request `Headers` with the generated `Token` after login.
Otherwise the response with `status: 401` will be like
```
{
  "detail": "Authentication credentials were not provided."
}
```

# add employee
`POST` method endpoint:

http://127.0.0.1:8000/api/v1/assets/add/employee/

Data
```
post_data = {
  "employee_email":"registered email of employee"
}
```
N.B. we could send invitation if the email isn't registered. which isn't part of this project.

response with `status: 201` if added
```
{
  "message": "Employee added",
  "data": {
    "id": 2,
    "company": "pk of the company who added",
    "employee": "pk of the employee"
  }
}
```
response with `status: 400` if the employee is already under any company
```
{
  "employee": [
    "company employee with this employee already exists."
  ]
}
```
<br><br>

# add device
`POST` method endpoint

http://127.0.0.1:8000/api/v1/assets/add/device/

data
```
post_data = {
  "device_id": "could be any unique ID given by company",
  "type": "Phone/Laptop/etc..",
  "brand": "Brand Name",
  "model": "Model No."
}
```
response with `status: 201`
```
{
  "message": "Device added",
  "data": {
    "id": "pk for the device",
    "device_id": "Given ID",
    "type": "Phone/Laptop/etc..",
    "brand": "Brand Name",
    "model": "Model No.",
    "is_available": true,
    "owner": 1
  }
}
```
Here is_available is by default true. That means it is available to be handed out. Owner is the company by which the device is added so we can verify which devices are under which company.

<br>
<br>

# handout device
`POST` method endpoint
http://127.0.0.1:8000/api/v1/assets/handout_device/

```
post_data = {
  "employee_email":"employee mail",
  "device_id": "ID of the device that is handed out",
  "condition": "Current condition like Good, Okay etc."
}
```
response with `status: 201`
```
{
  "message": "Handed out successfully",
  "data": {
    "id": 7,
    "checkout_time": "2022-11-13T17:47:21.860522Z",
    "checkout_condition": "Good",
    // null will be updated when returned
    "return_time": null, 
    "return_condition": null,
    "device": Device pk,
    "handed_to": Employee pk
  }
}
```

response with `status: 400` when the Device is already handed to someone or the employee not under the user(company)

```
{
  "message": "Employee or Device not available"
}
```

# return device
`PATCH` method endpoint

http://127.0.0.1:8000/api/v1/assets/return_device/{log_id}


now posting with just the return_condition and the log will be updated.
```
post data = {
  "return_condition": "Okay"
}
```
response of detail with `status: 200`
```
{
  "id": 4,
  "checkout_time": "2022-11-13T08:02:16.473350Z",
  "checkout_condition": "Good",
  "return_time": "2022-11-13T18:09:26.064205Z",
  "return_condition": "Okay",
  "device": 2,
  "handed_to": 4
}
```

# device logs
`GET` method endpoint

http://127.0.0.1:8000/api/v1/assets/device_logs

No params required

response of list of all devices with `status: 200`

```
[
  {
    "id": 4,
    "checkout_time": "2022-11-13T08:02:16.473350Z",
    "checkout_condition": "Good",
    "return_time": "2022-11-13T10:08:08.449325Z",
    "return_condition": "Okay",
    "device": 2,
    "handed_to": 4
  }
]
```
# All API Swagger UI

http://127.0.0.1:8000/api-documentation/
