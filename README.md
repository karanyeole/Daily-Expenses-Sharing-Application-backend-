# Daily Expenses Sharing Application

## Overview

The **Daily Expenses Sharing Application** is a backend service that allows users to add and manage expenses while providing the functionality to split them among participants using three different methods: equal, exact amounts, and percentages. The application supports user management, expense management, input validation, and downloading balance sheets.

### Key Features:

- **User Management:** Users can register with their name, email, and mobile number.
- **Expense Management:** Users can add expenses and split them by:
  1. **Equal split:** Splits the amount equally among all participants.
  2. **Exact amounts:** Allows specifying exact amounts for each participant.
  3. **Percentage split:** Allows specifying percentages (ensuring they sum up to 100%).
- **Balance Sheet:** Shows individual user expenses and overall expenses, with an option to download the balance sheet as a CSV file.
- **Authentication:** User login with email and password.
- **Expense Filtering (optional):** Provides the ability to filter expenses based on date, category, or amount (if implemented).
- **Error Handling and Validation:** Ensures proper validation of user input (e.g., percentages summing to 100%).

## Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django
- Django REST Framework
- SQLite (default database, you can use PostgreSQL or MySQL if preferred)

### Setup

1. Clone the repository:

    ```bash
    git clone <repository_link>
    cd Daily-Expenses-Sharing-Application
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application** at `http://127.0.0.1:8000/`.

## API Endpoints

### User Management Endpoints:

1. **Create a User:**

   `POST /api/users/`

   - Request body:
     ```json
     {
       "name": "John Doe",
       "email": "john.doe@example.com",
       "mobile": "1234567890",
       "password": "password123"
     }
     ```

2. **User Login:**

   `POST /api/login/`

   - Request body:
     ```json
     {
       "email": "john.doe@example.com",
       "password": "password123"
     }
     ```

### Expense Management Endpoints:

1. **Add an Expense:**

   `POST /api/expenses/`

   - Request body for equal split:
     ```json
     {
       "description": "Dinner with friends",
       "amount": 3000,
       "split_method": "equal",
       "participants": [1, 2, 3]
     }
     ```

   - Request body for exact amounts:
     ```json
     {
       "description": "Shopping",
       "amount": 4299,
       "split_method": "exact",
       "participants": [1, 2, 3],
       "amounts": [799, 2000, 1500]
     }
     ```

   - Request body for percentage split:
     ```json
     {
       "description": "Party",
       "amount": 5000,
       "split_method": "percentage",
       "participants": [1, 2, 3],
       "percentages": [50, 25, 25]
     }
     ```

2. **Retrieve User Expenses:**

   `GET /api/users/<user_id>/expenses/`

   - Response:
     ```json
     {
       "user": {
         "id": 1,
         "name": "John Doe",
         "email": "john.doe@example.com"
       },
       "expenses": [...]
     }
     ```

3. **Retrieve Overall Expenses (with Pagination):**

   `GET /api/expenses/`

   - Response:
     ```json
     {
       "count": 50,
       "next": "http://127.0.0.1:8000/api/expenses/?page=2",
       "previous": null,
       "results": [...]
     }
     ```

4. **Download Balance Sheet:**

   `GET /api/expenses/download-balance-sheet/`

   - Response: CSV file of the balance sheet.

## Error Handling

- Proper validation is implemented to ensure that percentages add up to 100% when using the percentage split method.
- Errors are returned in a user-friendly JSON format with appropriate HTTP status codes.
- Authentication is required for sensitive actions such as adding expenses and retrieving user details.

## Testing

Unit tests have been written for the core features of the application:

- **User creation and authentication**
- **Expense addition and validation**

To run the tests, use the following command:

```bash
python manage.py test
