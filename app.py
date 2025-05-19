from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory database
listings = {}

# Helper function to generate new listing ID
def generate_id():
    return str(uuid.uuid4())

# Sample data initialization
def init_sample_data():
    sample_listings = [
        {
            "id": generate_id(),
            "title": "Cozy Apartment in Paris",
            "location": "Paris, France",
            "price_per_night": 100,
            "description": "Beautiful apartment near Eiffel Tower",
            "amenities": ["WiFi", "Kitchen", "Air conditioning"]
        },
        {
            "id": generate_id(),
            "title": "Beach House in Miami",
            "location": "Miami, USA",
            "price_per_night": 150,
            "description": "Relaxing beach house with ocean view",
            "amenities": ["WiFi", "Pool", "Beach access"]
        }
    ]
    
    for listing in sample_listings:
        listings[listing["id"]] = listing

init_sample_data()

# GET - Retrieve all listings
@app.route('/api/listings', methods=['GET'])
def get_all_listings():
    return jsonify({"listings": list(listings.values()), "count": len(listings)})

# GET - Retrieve a specific listing
@app.route('/api/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    if listing_id in listings:
        return jsonify({"listing": listings[listing_id]})
    return jsonify({"error": "Listing not found"}), 404

# POST - Create a new listing
@app.route('/api/listings', methods=['POST'])
def create_listing():
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    required_fields = ["title", "location", "price_per_night", "description"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    listing_id = generate_id()
    
    new_listing = {
        "id": listing_id,
        "title": data["title"],
        "location": data["location"],
        "price_per_night": data["price_per_night"],
        "description": data["description"],
        "amenities": data.get("amenities", [])
    }
    
    listings[listing_id] = new_listing
    
    return jsonify({"message": "Listing created successfully", "listing": new_listing}), 201

# PUT - Update a listing
@app.route('/api/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    if listing_id not in listings:
        return jsonify({"error": "Listing not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    
    # Update fields
    for key in data:
        if key != "id":  # Don't allow ID to be changed
            listings[listing_id][key] = data[key]
    
    return jsonify({"message": "Listing updated successfully", "listing": listings[listing_id]})

# DELETE - Remove a listing
@app.route('/api/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    if listing_id not in listings:
        return jsonify({"error": "Listing not found"}), 404
    
    deleted_listing = listings.pop(listing_id)
    
    return jsonify({"message": "Listing deleted successfully", "listing": deleted_listing})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Homey API is running"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
