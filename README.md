# Phone Book API

Welcome to my phone book API

You can use this API for a phone book app. It includes the basic phone book operations.

### Features
- **Create contact**: create a new contact with the following fields:
    - First name: a string up to 30 characters.
    - Last name: a string up to 30 characters.
    - Phone number: up to 9 digits.
    - Address: a string up to 40 characters.
    - id: uuid that any contact gets at creation.
    - Favorite: a boolean represents if a contact is a favorite or not. Default is false.
- **Get contacts**: get all the contact from the database in parts. Optional parameters:
    - Limit: the amount of contacts to returnn from the database. Default is 10.
    - Page: which part of documents to return according to limit.
    - Favorites: put the contacts that marked as favorites at the beginning of the list.
- **Search contacts**: Free text search to find contacts, by name or phone number.
- **Delete contact**: delete a contact from the database by its id.
- **Update contact**: update contact's details

### Important Points
- It is not possible to save two records with the same phone number.
- You can view the API documentation when is it running at http://0.0.0.0:8000/docs.
- The API is limited to 100 requests per minute.



## How to run

### Using Docker
Clone the git repository: paste the following command in your terminal:
```bash
git clone https://github.com/chenashkenazi/phone_book.git
```
Make sure [docker desktop](https://www.docker.com/products/docker-desktop/) in Installed on your computer, or anything that runs docker engine.


Then run the docker compose command:
```bash
docker-compose up --build
```

### Locally
If you want to run the API locally, you need to make sure to have a Postgres database running and a `.env` file with the database URL.

## Usage
### Create new contact
Create new contact with all its details

```bash
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "", "last_name": "", "phone_number": "", "address": "", "is_favorite": "true"}' http://0.0.0.0:8000/contacts/
```

### Get contacts
Get all contact from the database

The list of contact that returned is ordered by asceding order of the first names.

```bash
curl -X GET http://0.0.0.0:8000/contacts/
```
Optional parameters to add:

```bash
curl -X GET http://127.0.0.1:8000/contacts/?limit=10&page=1&favorites=true
```

### Search contact
Search contact by name or phone number
```bash
curl -X GET "http://127.0.0.1:8000/contacts/search/?search_text=keyword"
```

### Delete contact
Delete a contact by its id
```bash
curl -X DELETE http://127.0.0.1:8000/contacts/uuid
```

### Update contact
Update contact details by its id
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key":"value", "key", "value"}' http://127.0.0.1:8000/contacts/uuid
```

## Tests
The API has unit tests written with Pytest.

For the tests I used an in-memory SQLite database. SQLite is lightweight anf file-based database meaning it exists during the tests and is cleared once the tests are done. It's a fast database and simple to set up.

To run the tests use the Pytest command:
```bash
pytest
```

