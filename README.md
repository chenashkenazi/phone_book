# Phone Book API ☎️

Welcome to my phone book API! 

You can use this API for a phone book app. It includes the basic phone book operations such as adding, searching and deleting contacts.

### Features
- **Create contact**: Create a new contact with the following fields:
    - First name: A string up to 30 characters.
    - Last name: A string up to 30 characters.
    - Phone number: Up to 9 digits.
    - Address: A string up to 40 characters.
    - id: A uuid assigned to the contact upon creation.
    - Favorite: a boolean representing if a contact is marked as favorite. Default is `false`.
- **Get contacts**: Get all the contact from the database in paginated form. Optional parameters:
    - Limit: The number of contacts to return from the database. Default is 10.
    - Page: The page of results to return based on the limit.
    - Favorites: Prioritize contacts marked as favorites at the top of the list.
- **Search contacts**: Free-text search to find contacts by name or phone number.
- **Delete contact**: Delete a contact from the database by its id.
- **Update contact**: Update contact's details.

### Important Points
- It is not possible to save two records with the same phone number.
- You can view the API documentation when is it running at http://localhost:8000/docs.
- The API is limited to 100 requests per minute.



## How to run

### Using Docker
Clone the git repository: paste the following command in your terminal:
```bash
git clone https://github.com/chenashkenazi/phone_book.git
```
Make sure [docker desktop](https://www.docker.com/products/docker-desktop/) in Installed on your computer, or that you have another environment that can run Docker Engine.


Then run the docker compose command:
```bash
docker-compose up --build
```

### Locally
If you want to run the API locally, make sure to have a Postgres database running and a `.env` file with the database URL.

## Usage
You can use [this postman collection](https://team22-1890.postman.co/workspace/team-Workspace~ea3a6291-66a7-4810-821c-d5c4ecb0c298/collection/12175517-3feeb71d-7b65-4189-b9e1-4dc0d5715381?action=share&creator=12175517) for testing.
### Create new contact
Create new contact with all its details:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "phone_number": "027986482", "address": "Hollywood", "is_favorite": "true"}' http://localhost:8000/contacts/
```

### Get contacts
Get all contact from the database

The list of contact that returned is ordered by ascending order of the first names:

```bash
curl -X GET http://localhost:8000/contacts/
```
Optional parameters:

```bash
curl -X GET http://localhost:8000/contacts/?limit=10&page=1&favorites=true
```

### Search contact
Search contact by name or phone number
```bash
curl -X GET "http://localhost:8000/contacts/search/?search_text=keyword"
```

### Delete contact
Delete a contact by its id
```bash
curl -X DELETE http://localhost:8000/contacts/uuid
```

### Update contact
Update contact details by its id
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key":"value", "key", "value"}' http://localhost:8000/contacts/uuid
```

## Tests
The API has unit tests written with Pytest.

For the tests I used an in-memory SQLite database. SQLite is lightweight anf file-based database meaning it exists during the tests and is cleared once the tests are done. It's a fast database and simple to set up.

To run the tests use the Pytest command:
```bash
pytest
```

Thank you for the opportunity!
