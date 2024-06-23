# Online Store Inventory and Supplier Management API 

You are developing a system for an online store to manage its inventory and suppliers. The store requires an API to handle these aspects efficiently. This API will be utilized by various internal systems, including the front-end interface and the inventory tracking system.

## Prerequisites
- Python 3.12
- Pip (python package install)
- Docker (if applicable)

## Installation

You can either build the application and run a docker container to quickly get started or you can install dependencies and run the application from scratch.

#### Clone the repository to your local machine

```bash
git clone https://github.com/Timadey/inventory.git
cd inventory

```
#### Start with Docker

```bash
docker build -t inventory .
docker run -p 8000:8000 inventory
```

Navigate to `https://localhost:8000/api/docs/swagger-ui/` or `https://localhost:8000/api/docs/redoc/` to view api documentations

#### Install dependencies and start application
Install Python dependencies using pip

```bash
pip install -r requirements.txt
```
Apply initial database migrations

```bash
python manage.py migrate
```
Start the Django development server

```bash
python manage.py runserver
```
Navigate to `https://localhost:8000/api/docs/swagger-ui/` or `https://localhost:8000/api/docs/redoc/` to view api documentations

## Testing
To test the application run

```bash
python manage.py test
```

## License

[MIT](https://choosealicense.com/licenses/mit/)