# Test-Personal
<!-- ABOUT THE PROJECT -->
## About the Code
**Objective**: Place the food order for emplyees who will attend the event

**Input** : employee_order.xml file, has all data of employees

**Output** : JSON encoded list of orders

Code is divided into three steps of implementation

1. Get the list of dishes(food items) which are orderd by employees who will attend the event
2. Get the dish_id from the API GET method response.
3. Prepare/build the JSON encoded list of orders having all necessary values to place order to API endpoint using POST method.

## Usage
1. Download the zipped git repository
2. unzip the it.
3. Place the folder to any working directory and go there via terminal
 ```sh
   cd Documents/Test-Personal-main/order_food/
   ```
4. Run the code
```sh
   /Documents/Test-Personal-main/order_food$ python challenge.py
   ```
After step 4, you will see the result , a JSON encoded list of orders which will be used to place order using API enpoints.

## Note
I have used static data as a response from GET method for the endpoint ```nourish.me/api/v1/menu```, as it is dummy endpoint and could not get any response to get `dish_id` for every orderd dish from employess.
