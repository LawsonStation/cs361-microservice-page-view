# cs361-microservice-page-view

---

**Author**: hokevi@oregonstate.edu  
**Project**: CS 361 - Software Engineering I  
**Assignment**: Microservice B

## Overview
This microservice tracks page views for items, increments the view count each time an item is viewed, and allows for querying the page view count. It uses Flask, SQLAlchemy, and SQLite for storing and managing data.


## Features
- **Track Item Views**: When an item is viewed, the page view count for that item is incremented.
- **Fetch Page View Count**: You can fetch the current page view count for any item.
- **Database Reset**: Allows you to reset the database (delete all page view records).
- **Microservice Structure**: It can be integrated with other Flask applications or used as a standalone microservice.
   

## Technologies Used
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- SQLite (default database)


## Getting Started
1.  Clone this repository to your local machine.
2.  Ensure that Python and PIP (Preferred Installer Program) are installed.
3.  Create a virtual environment (env) with `python -m venv env` and run it using `.\env\Scripts\activate`.
4.  Ensure that dependencies are installed: `pip install -r requirements.txt`.
5.  Start the microservice using `python app.py` (default: port=5001).


## Using the Microservice
The microservice allows you to interact with the page view data using HTTP requests. You can request data about the page view count for a specific item using a `GET` request to the `/*/<item_id>` endpoint, where `<item_id>` is the ID of the item you're interested in.

### Incrementing and Receiving the PageView Count
To increment the page count view for an item, you can make a `POST` request to the `/view/<item_id>` endpoint. This action will increase the page view count for the specified item by 1. If the specified `<item_id>` does not exist in the PageView table, it will be created.

<!-- ### Getting the PageView Count -->
To get the page view count, the `<item_id>` data that the client requested will be returned back as a JSON object containing the current page view count for the specified item. If the item ID exists, the success response (status code `200`) will have the following format:

```json
{
    "item_id": 1,
    "count": 5
}
```

If the item does not exist or another erroro occurre, the following response will be sent along with a `404` or `500` status code:

```json
{
    "error": "Item not found."
}
{
    "error": "Could not process the request."
}
```

### Deleting an Item from the PageView Database
If the `<item_id>` is deleted from the client, a `POST` request can be made to the the `/delete/<item_id>` endpoint to delete the corresponding `<item_id>` record from the PageView database. This maintains referential consistency between the client and microservice. A successful deletion will return a `200` status response, with the following payload:

```json
{
    "message": "Item {item_id} deleted successfully."
}
```

An error while deleting will yield a `404` or `500` status code:

```json
{
    "message":"Error deleting item."
}
{
    "message": "Item {item_id} not found."
}
```

## Contact Me 
For any issues, please send me a message at hokevi@oregonstate.edu or file a bug here.