import unittest
import json
from app import app, listings, init_sample_data

class HomeyApiUnitTests(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Reset database before each test
        listings.clear()
        init_sample_data()
    
    def test_get_all_listings(self):
        # Test getting all listings
        response = self.app.get('/api/listings')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('listings', data)
        self.assertEqual(len(data['listings']), 2)  # We initialized with 2 sample listings
    
    def test_get_listing(self):
        # Get a listing ID from the database
        listing_id = list(listings.keys())[0]
        
        # Test getting a specific listing
        response = self.app.get(f'/api/listings/{listing_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('listing', data)
        self.assertEqual(data['listing']['id'], listing_id)
    
    def test_get_nonexistent_listing(self):
        # Test getting a listing that doesn't exist
        response = self.app.get('/api/listings/nonexistent-id')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
    
    def test_create_listing(self):
        # Create test data
        new_listing = {
            "title": "Mountain Cabin",
            "location": "Denver, USA",
            "price_per_night": 120,
            "description": "Cozy cabin in the mountains",
            "amenities": ["Fireplace", "Hiking trails"]
        }
        
        # Test creating a new listing
        response = self.app.post('/api/listings', 
                               data=json.dumps(new_listing),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('listing', data)
        self.assertEqual(data['listing']['title'], new_listing['title'])
        
        # Verify the listing was added to the database
        self.assertEqual(len(listings), 3)  # 2 sample + 1 new
    
    def test_create_listing_missing_fields(self):
        # Create test data with missing required fields
        incomplete_listing = {
            "title": "Incomplete Listing",
            "location": "Somewhere"
            # Missing price_per_night and description
        }
        
        # Test creating a listing with missing fields
        response = self.app.post('/api/listings', 
                               data=json.dumps(incomplete_listing),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_update_listing(self):
        # Get a listing ID from the database
        listing_id = list(listings.keys())[0]
        
        # Create update data
        update_data = {
            "title": "Updated Title",
            "price_per_night": 200
        }
        
        # Test updating a listing
        response = self.app.put(f'/api/listings/{listing_id}', 
                              data=json.dumps(update_data),
                              content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('listing', data)
        self.assertEqual(data['listing']['title'], update_data['title'])
        self.assertEqual(data['listing']['price_per_night'], update_data['price_per_night'])
    
    def test_update_nonexistent_listing(self):
        # Create update data
        update_data = {"title": "Updated Title"}
        
        # Test updating a listing that doesn't exist
        response = self.app.put('/api/listings/nonexistent-id', 
                              data=json.dumps(update_data),
                              content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
    
    def test_delete_listing(self):
        # Get a listing ID from the database
        listing_id = list(listings.keys())[0]
        
        # Test deleting a listing
        response = self.app.delete(f'/api/listings/{listing_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        
        # Verify the listing was removed from the database
        self.assertEqual(len(listings), 1)  # Started with 2, deleted 1
    
    def test_delete_nonexistent_listing(self):
        # Test deleting a listing that doesn't exist
        response = self.app.delete('/api/listings/nonexistent-id')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
    
    def test_health_check(self):
        # Test health check endpoint
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
