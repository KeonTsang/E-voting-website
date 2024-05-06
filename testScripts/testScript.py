import concurrent.futures
import time
from website import create_app, db, models
import requests

# Function to simulate website requests and database interactions
def simulate_website_and_db_interaction():
    start_time = time.time()
    
    # Perform website request
    response = requests.get('http://localhost:5000/')
    if response.status_code != 200:
        print(f"Error: Website request failed with status code {response.status_code}")
    
    #Perform database interactions
    with app.app_context():
        new_record = models.Message(fname='John', lname='Doe', email='john@example.com', message='Hello, world!')
        db.session.add(new_record)
        db.session.commit()
    
    end_time = time.time()
    return end_time - start_time

# Function to run the test with concurrency
def run_test_with_concurrency(num_requests, concurrency):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(simulate_website_and_db_interaction) for _ in range(num_requests)]
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    # Set up Flask app
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    
    # Initialize the database
    with app.app_context():
        db.create_all()

    # Parameters
    num_requests = 100
    concurrency_levels = [1, 2, 5, 10]

    # Run the test with different concurrency levels
    for concurrency in concurrency_levels:
        response_time = run_test_with_concurrency(num_requests, concurrency)
        throughput = num_requests / response_time if response_time > 0 else 0
        print(f"Concurrency: {concurrency}, Response Time: {response_time:.2f} seconds, Throughput: {throughput:.2f} requests/second")
