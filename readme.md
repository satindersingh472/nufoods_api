# `Foodie_Api`

## `Introduction`

This is the api for **`foodie`** project
Every endpoint should be followed by 

https://nufoods.ml

# Endpoints

## `Client-Login`
## /api/client_login
HTTP methods available: **POST, DELETE**

### `POST`

Helps the client to login successfully with the email and password.<br>
returns the client id and token 

**Required Data**
```
{
    email: (string),
    password: (string)
}
```
**Data Returned**
```
{
    client_id : (number),
    token: (string)
}
```
### `DELETE`

Helps to logout the user from current session with valid token.<br>
 **Required Headers**
 ```
 {
    token: (string)
 }
```
**Data Returned**
**On Success**: "successfully logged out" <br>
**On failure**: "logout not successfull or already logged out" or **any other error**. <br>

<br>
<br>

## `Clients`
## /api/clients

HTTP methods available : **GET, POST, PATCH, DELETE**

### `GET`

Returns information about a single client with given client_id.<br>
Returns **the client_id argument is required**, if the client_id is not sent. 

**Required Params:** 
```
{
    client_id : (number)
}
```

**Data Returned:**
```
[
    {
        cliend_id: (number),
        first_name: (string),
        last_name: (string),
        email: (string),
        username: (string),
        image_url: (string)

    }
]
```
<br>

### `POST`

Creates a new client and returns back the id and token of client added.

**Required Data**
```
{
    email: (string),
    first_name: (string),
    last_name: (string),
    image_url: (string),
    username: (string),
    password: (string)
}
```
**Data Returned**
```
{
    client_id: (number),
    token: (string)
}
```
<br>

### `PATCH`

A client can edit its profile with a valid token. <br>

**Required Headers** <br>
```
{
    token: (string)
}
```

**Optional Data** : send **1** or more data arguments to make changes to the profile
```
{
    email: (string),
    first_name: (string),
    last_name: (string),
    image_url: (string),
    username: (string),
    password: (string)
}
```
**Data Returned**  <br>
**On success** : "client profile updated" <br>
**On failure** : "client profile not changed" or **any other error**. <br>

<br>

### `DELETE`

Deletes the existing client with token sent as header and password sent as required data

**Required Headers**
```
{
    token: (string)
}
```

**Required Data**
```
{
    password: (string)
}
```
**Data Returned**

**On success** : "client deleted successfully" <br>
**On failure** : "no client deleted" or **any other error message**

<br>
<br>

## `Restaurant_Login`
## /api/restaurant_login
HTTP methods available : **POST,DELETE**

### `POST`

Helps login a restaurant with valid email and password.<br>
Returns the restaurant id and token<br>

**Required Data**
```
{
    email: (string),
    password: (string)
}
```

**Data Returned**
```
{
    id: (number),
    token: (string)
}
```
<br>

### `DELETE`

Deletes the token in use for a restaurant to logout safely
send the token as a header

**Required Headers**
```
{
    token: (string)
}
```
**Returned Data**
**On success**: "restaurant logout successfully"<br>
**On failure**: "restaurant logout not successfull or already logged out" or **any other error**.<br>


<br>
<br>

## `Restaurants`
## /api/restaurants
HTTP methods available: **GET**

### `GET`

Return all the available restaurants.

**Data Returned**
```
[
    {
        restaurant_id: (number),
        name: (string),
        address: (string),
        phone_num: (string),
        bio: (string),
        city: (string),
        email: (string),
        profile_url: (string),
        banner_url: (string)
    },
]
```

## `Restaurant`
## /api/restaurant
HTTP methods available: **GET, POST, PATCH, DELETE**

### `GET`

Return the information about the single restaurant if `restaurant_id` is provided.<br>
if `restaurant_id` is not provided then it will show an error

**Required Params**
```
{
    restaurant_id: (number)
}
```
**Data Returned**
```
[
    {
        restaurant_id: (number),
        name: (string),
        address: (string),
        phone_num: (string),
        bio: (string),
        city: (string),
        email: (string),
        profile_url: (string),
        banner_url: (string)
    }
]
```
### `POST`

Adds a new restaurant to the database which can be viewed by clients and use the system.<br>
will show an error if any duplicate entry is present i.e. phone_num or email. will show the error of duplicate entry 
it will also send back the restaurant id and token for signing in right after the signup

**Required Data**
```
{
    email: (string),
    name: (string),
    address: (string),
    phone_number: (string),
    bio: (string),
    city: (string),
    profile_url: (string),
    banner_url: (string),
    password: (string)
}
```
**Data Returned**
```
{
    restaurant_id : (number),
    token: (string)
}
```
<br>

### `PATCH`  <br>

Restaurant can edit the profile by sending a valid token as a headers and optional data to edit. <br>

**Required Headers**  <br>
```
{
    token: (string)
}
```
**Optional Data** : Send one or more optional arguments to see any change. <br>
```
{
    email: (string),
    name: (string),
    address: (string),
    phone_number: (string),
    bio: (string),
    city: (string),
    profile_url: (string),
    banner_url: (string),
    password: (string) 
}

```
**Data Returned** <br>
**On success** : "restaurant profile updated" <br>
**On failure** : "restaurant profile not updated" or **any other error**  <br>


<br>

### `DELETE`

Deleted the existing restaurant with if token is given and password.<br>
return error if credentials are not correct.<br>

**Required Headers**
```
{
    token: (string)
}
```

**Required Data**
```
{
    passsword: (string)
}
```
**Data Returned**
**On success**: "restaurant deleted successfully"
**On failure**: "no restaurant deleted" or **any other error messages**


<br>
<br>

## `Menu`
## /api/menu
HTTP methods available: **GET, POST, PATCH, DELETE** <br>

### `GET` <br>

Returns all the menu items associated with a restaurant

**Required Params**
```
{
    restaurant_id: (number)
}
```
**Data Returned**
```
[
    {
        id: (number),
        name: (string),
        price: (string),
        description: (string),
        image_url: (string)
    },
]
```

### `POST` <br>

Adds a new menu item to the restaurant.<br>
Returns the id of newly added item.<br>

**Required Headers**
```
{
    token: (string)
}
```

**Required Data**
```
{
    name: (string),
    price: (number),
    description: (string),
    image_url: (string)
}
```
**Data Returned**

```
{
    id: (string)
}
```
<br>

### `PATCH` <br>

Menu item can be edited by a restaurant with a valid token and a valid menu_id

**Required Headers**
```
{
    token: (string)
}
```

**Required Data**
```
{
    menu_id: (number)
}
```
**Optional data** 
send optional 1 or more data arguments to change anything for the menu item
```
{
    description: (string),
    image_url: (string),
    name: (string),
    price: (number)
}
```
<br>


### `DELETE` <br>

Deletes a menu item if a valid token is sent as a header and menu_id as required data

**Required Headers**
```
{
    token: (string)
}
```
**Required Data**
```
{
    menu_id: (number)
}◊
```
**Data Returned** <br>
**On success**: "menu item deleted" <br>
**On failure**: "menu item not exists or user is not authorized" or **any other error**.

<br>

## `Client_Order`
## /api/client_order
HTTP methods available: **GET,POST** <br>

### `GET` <br>

Returns all the orders made by a client with valid token.
Data required is optional.<br>

**Required Headers** <br>
```
{
    token: (string)
}
```
**Optional Params** <br>
```
{
    is_completed : (string either "true" or "false)
    is_confirmed : (string either "true" or "false")
}
```
**Data returned**
```
[
    {
        is_complete: (boolean),
        is_confirmed: (boolean),
        name: (string),
        price: (number with 2 decimals),
        menu_item_id: (number),
        order_id: (number)
    },
]
```
<br>
<br>

<br>

### `POST`

Post a new order from client side given the valid token as a header<br>
and restaurant id and menu items as an arrar of numbers

**Required Headers**
```
{
    token: (string)
}
```
**Required Data**
```
{
    menu_items: [array of numbers],
    restaurant_id: (number)
}
```
**Data Returned**
```
{
    order_id: (number)
}
```

## `Restaurnt_Order` <br>
## api/restaurant_order <br>
HTTP methods available : **GET,PATCH** <br>

### `GET`

Returns order based on data sent.modify the return by sending optional params

**Required Headers**
```
{
    token: (string)
}
```

**Optional Params**
```
{
    is_confirmed: (string either "true" or "false"),
    is_completed: (string either "true" or "false")
}
```
**Data Returned** <br>
```
[
    {
        is_complete: (boolean),
        is_confirmed: (boolean),
        name: (string),
        price: (number),
        menu_item_id: (number),
        order_id: (number)
    }
]
```
<br>
<br>

### `PATCH`


Restaurant must be logged in to provide a valid token.
Modify the order by sending true for is_confirmed and is_completed.
The "true" value for is_confirmed will confirm the order. <br>
The "true" value for is_completed will complete and confirm the order as well.

**Required Headers**
```
{
    token: (string)
}
```

**Required Data**
```
{
    order_id: (number)
}
```
**Optional Data**
```
{
    is_confirmed: "true" (will confirm the order),
    is_completed: "true" (will complete the order and also confirm if not done before)
}
```
<br>
<br>