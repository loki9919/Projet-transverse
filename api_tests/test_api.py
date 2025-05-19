import requests
import unittest
import json
import time

# API base URL - update this if your service is deployed elsewhere
API_BASE_URL = "http://localhost:5000"

class HomeyApiTests(unittest.TestCase):
    
    def setUp(self):
        # Wait for API to be available
        self.wait_for_api()
        
        # Get initial listings (to use in tests)
        response = requests.get(f"{API_BASE_URL}/api/listings")
        self.initial_listings = response.json()["listings"]
        
        # For tests that create listings, we'll store the IDs to clean up later
        self.created_listing_ids = []
    
    def tearDown(self):
        # Clean up any listings created during tests
        for listing_id in self.created_listing_ids:
            try:
                requests.delete(f"{API_BASE_URL}/api/listings/{listing_id}")
            except:
                pass
    
    def wait_for_api(self, max_retries=5):
        """Wait for the API to become available"""
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(f"{API_BASE_URL}/health")
                if response.status_code == 200:
                    return True
                retries += 1
                time.sleep(1)
            except:
                retries += 1
                time.sleep(1)
        
        raise Exception("API is not available")
    
    def test_get_all_listings(self):
        """Test GET /api/listings endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/listings")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("listings", data)
        self.assertIn("count", data)
        self.assertEqual(len(data["listings"]), data["count"])
    
    def test_get_specific_listing(self):
        """Test GET /api/listings/{id} endpoint"""
        # Get the first listing ID from the initial listings
        if not self.initial_listings:
            self.skipTest("No initial listings available for testing")
        
        listing_id = self.initial_listings[0]["id"]
        response = requests.get(f"{API_BASE_URL}/api/listings/{listing_id}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("listing", data)
        self.assertEqual(data["listing"]["id"], listing_id)
    
    def test_create_listing(self):
        """Test POST /api/listings endpoint"""
        new_listing = {
            "title": "API Test Listing",
            "location": "API Test Location",
            "price_per_night": 99,
            "description": "Test listing created by API test",
            "amenities": ["API Testing"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/listings",
            json=new_listing
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("listing", data)
        self.assertEqual(data["listing"]["title"], new_listing["title"])
        
        # Store the ID for cleanup
        self.created_listing_ids.append(data["listing"]["id"])
    
    def test_update_listing(self):
        """Test PUT /api/listings/{id} endpoint"""
        # Create a listing to update
        new_listing = {
            "title": "API Test - Update",
            "location": "API Test Location",
            "price_per_night": 99,
            "description": "Test listing for update test",
            "amenities": ["API Testing"]
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/api/listings",
            json=new_listing
        )
        
        listing_id = create_response.json()["listing"]["id"]
        self.created_listing_ids.append(listing_id)
        
        # Update the listing
        update_data = {
            "title": "Updated API Test Listing",
            "price_per_night": 199
        }
        
        update_response = requests.put(
            f"{API_BASE_URL}/api/listings/{listing_id}",
            json=update_data
        )
        
        self.assertEqual(update_response.status_code, 200)
        data = update_response.json()
        self.assertIn("listing", data)
        self.assertEqual(data["listing"]["title"], update_data["title"])
        self.assertEqual(data["listing"]["price_per_night"], update_data["price_per_night"])
    
    def test_delete_listing(self):
        """Test DELETE /api/listings/{id} endpoint"""
        # Create a listing to delete
        new_listing = {
            "title": "API Test - Delete",
            "location": "API Test Location",
            "price_per_night": 99,
            "description": "Test listing for delete test",
            "amenities": ["API Testing"]
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/api/listings",
            json=new_listing
        )
        
        listing_id = create_response.json()["listing"]["id"]
        
        # Delete the listing
        delete_response = requests.delete(f"{API_BASE_URL}/api/listings/{listing_id}")
        
        self.assertEqual(delete_response.status_code, 200)
        data = delete_response.json()
        self.assertIn("message", data)
        self.assertIn("listing", data)
        
        # Verify the listing is deleted
        get_response = requests.get(f"{API_BASE_URL}/api/listings/{listing_id}")
        self.assertEqual(get_response.status_code, 404)
    
    def test_error_handling(self):
        """Test API error handling"""
        # Test invalid listing ID
        response = requests.get(f"{API_BASE_URL}/api/listings/nonexistent-id")
        self.assertEqual(response.status_code, 404)
        
        # Test invalid request data
        response = requests.post(
            f"{API_BASE_URL}/api/listings",
            json={"title": "Incomplete Data"}  # Missing required fields
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
