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



<br>
<br>

## `Clients`
## /api/clients

HTTP methods available : **GET, POST, PATCH, DELETE**

### `GET`

Returns information about a single client with given **`client_id`**.<br>
Returns **the client_id argument is required**, if the **`client_id`** is not sent. 

**Required Params:** 
```
{
    client_id : (number)
}
```

**Data Returned:**
```
{
    cliend_id: (number),
    first_name: (string),
    last_name: (string),
    email: (string),
    username: (string),
    image_url: (string)

}
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
HTTP methods available: **GET, POST, PATCH, DELETE**

### `GET`

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

