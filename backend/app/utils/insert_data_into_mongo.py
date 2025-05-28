"""
Script to insert sample e-commerce products into MongoDB
Run this once to populate the database with sample data
"""
import pymongo
from datetime import datetime
import random

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["superapp_ecommerce"]
collection = db["products"]

# Sample product data
sample_products = [
    {
        "name": "iPhone 15 Pro Max",
        "description": "Latest Apple smartphone with A17 Pro chip, titanium design, advanced camera system with 5x telephoto zoom, Action Button, and USB-C connectivity",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "price": 1199.99,
        "currency": "USD",
        "seller": "Apple Store",
        "brand": "Apple",
        "rating": 4.8,
        "reviews_count": 2547,
        "in_stock": True,
        "stock_quantity": 50,
        "tags": ["smartphone", "apple", "5g", "camera", "premium"],
        "specifications": {
            "storage": "256GB",
            "color": "Natural Titanium",
            "display": "6.7-inch Super Retina XDR",
            "battery": "Up to 29 hours video playback"
        }
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "description": "Premium Android smartphone with S Pen, 200MP camera, AI features, titanium frame, and exceptional display quality",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "price": 1299.99,
        "currency": "USD",
        "seller": "Samsung Official",
        "brand": "Samsung",
        "rating": 4.7,
        "reviews_count": 1823,
        "in_stock": True,
        "stock_quantity": 30,
        "tags": ["smartphone", "samsung", "s-pen", "camera", "android"],
        "specifications": {
            "storage": "512GB",
            "color": "Titanium Black",
            "display": "6.8-inch Dynamic AMOLED 2X",
            "battery": "5000mAh"
        }
    },
    {
        "name": "MacBook Pro 14-inch M3",
        "description": "Professional laptop with M3 chip, Liquid Retina XDR display, up to 22 hours battery life, perfect for creative professionals",
        "category": "Electronics",
        "subcategory": "Laptops",
        "price": 1999.99,
        "currency": "USD",
        "seller": "Apple Store",
        "brand": "Apple",
        "rating": 4.9,
        "reviews_count": 892,
        "in_stock": True,
        "stock_quantity": 25,
        "tags": ["laptop", "apple", "m3", "professional", "creative"],
        "specifications": {
            "processor": "Apple M3",
            "memory": "16GB",
            "storage": "512GB SSD",
            "display": "14.2-inch Liquid Retina XDR"
        }
    },
    {
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "description": "Industry-leading noise canceling wireless headphones with exceptional sound quality, 30-hour battery life, and crystal clear call quality",
        "category": "Electronics",
        "subcategory": "Audio",
        "price": 399.99,
        "currency": "USD",
        "seller": "Sony Electronics",
        "brand": "Sony",
        "rating": 4.6,
        "reviews_count": 3421,
        "in_stock": True,
        "stock_quantity": 100,
        "tags": ["headphones", "wireless", "noise-canceling", "premium", "audio"],
        "specifications": {
            "type": "Over-ear",
            "connectivity": "Bluetooth 5.2",
            "battery": "30 hours",
            "noise_canceling": "Advanced"
        }
    },
    {
        "name": "Nike Air Jordan 1 Retro High",
        "description": "Classic basketball sneakers with premium leather construction, iconic design, and comfortable fit for everyday wear",
        "category": "Fashion",
        "subcategory": "Footwear",
        "price": 170.00,
        "currency": "USD",
        "seller": "Nike Official",
        "brand": "Nike",
        "rating": 4.5,
        "reviews_count": 5672,
        "in_stock": True,
        "stock_quantity": 75,
        "tags": ["sneakers", "basketball", "jordan", "retro", "fashion"],
        "specifications": {
            "material": "Premium Leather",
            "sole": "Rubber",
            "closure": "Lace-up",
            "gender": "Unisex"
        }
    },
    {
        "name": "LG 55-inch OLED C3 Smart TV",
        "description": "Premium OLED TV with perfect blacks, vibrant colors, α9 Gen6 AI processor, and comprehensive smart TV features",
        "category": "Electronics",
        "subcategory": "Television",
        "price": 1499.99,
        "currency": "USD",
        "seller": "LG Electronics",
        "brand": "LG",
        "rating": 4.8,
        "reviews_count": 1234,
        "in_stock": True,
        "stock_quantity": 20,
        "tags": ["tv", "oled", "smart-tv", "4k", "entertainment"],
        "specifications": {
            "size": "55 inches",
            "resolution": "4K Ultra HD",
            "refresh_rate": "120Hz",
            "smart_platform": "webOS"
        }
    },
    {
        "name": "Adidas Ultraboost 22 Running Shoes",
        "description": "High-performance running shoes with responsive BOOST midsole, Primeknit upper, and Continental rubber outsole",
        "category": "Sports",
        "subcategory": "Running",
        "price": 190.00,
        "currency": "USD",
        "seller": "Adidas Official",
        "brand": "Adidas",
        "rating": 4.4,
        "reviews_count": 2891,
        "in_stock": True,
        "stock_quantity": 60,
        "tags": ["running", "shoes", "sports", "boost", "performance"],
        "specifications": {
            "upper": "Primeknit",
            "midsole": "BOOST",
            "outsole": "Continental Rubber",
            "drop": "10mm"
        }
    },
    {
        "name": "KitchenAid Stand Mixer Artisan",
        "description": "Professional-grade stand mixer with 5-quart bowl, 10 speeds, and versatile attachments for all baking needs",
        "category": "Home & Kitchen",
        "subcategory": "Appliances",
        "price": 429.99,
        "currency": "USD",
        "seller": "KitchenAid Store",
        "brand": "KitchenAid",
        "rating": 4.7,
        "reviews_count": 8734,
        "in_stock": True,
        "stock_quantity": 40,
        "tags": ["mixer", "baking", "kitchen", "appliance", "professional"],
        "specifications": {
            "capacity": "5 Quart",
            "speeds": "10",
            "material": "Die-cast metal",
            "power": "325 Watts"
        }
    },
    {
        "name": "Levi's 501 Original Fit Jeans",
        "description": "Classic straight-leg jeans with original fit, button fly, and timeless style that never goes out of fashion",
        "category": "Fashion",
        "subcategory": "Clothing",
        "price": 69.50,
        "currency": "USD",
        "seller": "Levi's Store",
        "brand": "Levi's",
        "rating": 4.3,
        "reviews_count": 12456,
        "in_stock": True,
        "stock_quantity": 200,
        "tags": ["jeans", "denim", "classic", "fashion", "casual"],
        "specifications": {
            "fit": "Original Straight",
            "material": "100% Cotton",
            "closure": "Button Fly",
            "wash": "Medium Stonewash"
        }
    },
    {
        "name": "Dyson V15 Detect Cordless Vacuum",
        "description": "Advanced cordless vacuum with laser dust detection, powerful suction, and intelligent cleaning technology",
        "category": "Home & Kitchen",
        "subcategory": "Cleaning",
        "price": 749.99,
        "currency": "USD",
        "seller": "Dyson Official",
        "brand": "Dyson",
        "rating": 4.6,
        "reviews_count": 3421,
        "in_stock": True,
        "stock_quantity": 35,
        "tags": ["vacuum", "cordless", "cleaning", "laser", "technology"],
        "specifications": {
            "type": "Cordless",
            "battery": "Up to 60 minutes",
            "filtration": "Advanced whole-machine",
            "bin_capacity": "0.76 liters"
        }
    }
]

# Add more products to reach 50
additional_products = [
    # Electronics
    {
        "name": "iPad Pro 12.9-inch M2",
        "description": "Professional tablet with M2 chip, Liquid Retina XDR display, Apple Pencil support, perfect for creativity and productivity",
        "category": "Electronics", "subcategory": "Tablets", "price": 1099.99, "currency": "USD",
        "seller": "Apple Store", "brand": "Apple", "rating": 4.8, "reviews_count": 1547,
        "in_stock": True, "stock_quantity": 45,
        "tags": ["tablet", "apple", "m2", "creative", "professional"],
        "specifications": {"storage": "256GB", "display": "12.9-inch Liquid Retina XDR", "connectivity": "Wi-Fi + Cellular"}
    },
    {
        "name": "Bose QuietComfort Earbuds",
        "description": "Premium noise-canceling earbuds with exceptional sound quality, comfortable fit, and long battery life",
        "category": "Electronics", "subcategory": "Audio", "price": 279.99, "currency": "USD",
        "seller": "Bose Store", "brand": "Bose", "rating": 4.5, "reviews_count": 2187,
        "in_stock": True, "stock_quantity": 80,
        "tags": ["earbuds", "wireless", "noise-canceling", "premium"],
        "specifications": {"type": "In-ear", "battery": "6 hours + 18 hours case", "water_resistance": "IPX4"}
    },
    {
        "name": "Canon EOS R6 Mark II",
        "description": "Full-frame mirrorless camera with advanced autofocus, 4K video recording, and professional image quality",
        "category": "Electronics", "subcategory": "Cameras", "price": 2499.99, "currency": "USD",
        "seller": "Canon Store", "brand": "Canon", "rating": 4.9, "reviews_count": 567,
        "in_stock": True, "stock_quantity": 15,
        "tags": ["camera", "mirrorless", "professional", "full-frame"],
        "specifications": {"sensor": "24.2MP Full-frame", "video": "4K 60p", "autofocus": "Dual Pixel CMOS AF II"}
    },
    {
        "name": "Dell XPS 13 Plus Laptop",
        "description": "Premium ultrabook with Intel 12th gen processor, stunning display, and sleek modern design",
        "category": "Electronics", "subcategory": "Laptops", "price": 1299.99, "currency": "USD",
        "seller": "Dell Official", "brand": "Dell", "rating": 4.4, "reviews_count": 1123,
        "in_stock": True, "stock_quantity": 30,
        "tags": ["laptop", "ultrabook", "premium", "portable"],
        "specifications": {"processor": "Intel Core i7-1260P", "memory": "16GB", "display": "13.4-inch OLED"}
    },
    {
        "name": "PlayStation 5 Console",
        "description": "Next-generation gaming console with ultra-high speed SSD, ray tracing, and immersive gaming experience",
        "category": "Electronics", "subcategory": "Gaming", "price": 499.99, "currency": "USD",
        "seller": "Sony PlayStation", "brand": "Sony", "rating": 4.8, "reviews_count": 8934,
        "in_stock": True, "stock_quantity": 25,
        "tags": ["gaming", "console", "playstation", "next-gen"],
        "specifications": {"storage": "825GB SSD", "graphics": "AMD Radeon", "ray_tracing": "Hardware accelerated"}
    },
    
    # Fashion & Clothing
    {
        "name": "Ray-Ban Aviator Classic Sunglasses",
        "description": "Iconic aviator sunglasses with crystal lenses, gold frame, and timeless style for every occasion",
        "category": "Fashion", "subcategory": "Accessories", "price": 154.00, "currency": "USD",
        "seller": "Ray-Ban Store", "brand": "Ray-Ban", "rating": 4.6, "reviews_count": 4521,
        "in_stock": True, "stock_quantity": 120,
        "tags": ["sunglasses", "aviator", "classic", "fashion"],
        "specifications": {"lens": "Crystal", "frame": "Metal", "uv_protection": "100%"}
    },
    {
        "name": "Patagonia Down Sweater Jacket",
        "description": "Lightweight down jacket with recycled materials, excellent warmth-to-weight ratio, and packable design",
        "category": "Fashion", "subcategory": "Outerwear", "price": 229.00, "currency": "USD",
        "seller": "Patagonia Store", "brand": "Patagonia", "rating": 4.7, "reviews_count": 2341,
        "in_stock": True, "stock_quantity": 65,
        "tags": ["jacket", "down", "outdoor", "sustainable"],
        "specifications": {"fill": "800-fill down", "material": "Recycled polyester", "packable": "Yes"}
    },
    {
        "name": "Allbirds Tree Runners",
        "description": "Sustainable running shoes made from eucalyptus tree fiber, incredibly comfortable and eco-friendly",
        "category": "Fashion", "subcategory": "Footwear", "price": 98.00, "currency": "USD",
        "seller": "Allbirds Store", "brand": "Allbirds", "rating": 4.3, "reviews_count": 3456,
        "in_stock": True, "stock_quantity": 90,
        "tags": ["shoes", "sustainable", "running", "eco-friendly"],
        "specifications": {"material": "Eucalyptus tree fiber", "sole": "Bio-based", "machine_washable": "Yes"}
    },
    
    # Home & Kitchen
    {
        "name": "Instant Pot Duo 7-in-1 Pressure Cooker",
        "description": "Multi-functional electric pressure cooker that replaces 7 kitchen appliances, perfect for quick and healthy meals",
        "category": "Home & Kitchen", "subcategory": "Appliances", "price": 99.99, "currency": "USD",
        "seller": "Instant Pot Store", "brand": "Instant Pot", "rating": 4.5, "reviews_count": 15672,
        "in_stock": True, "stock_quantity": 85,
        "tags": ["pressure-cooker", "multi-cooker", "kitchen", "healthy"],
        "specifications": {"capacity": "6 Quart", "functions": "7-in-1", "programs": "13 Smart Programs"}
    },
    {
        "name": "Nespresso Vertuo Next Coffee Maker",
        "description": "Single-serve coffee maker with centrifusion technology, creates perfect crema, and brews multiple cup sizes",
        "category": "Home & Kitchen", "subcategory": "Appliances", "price": 179.99, "currency": "USD",
        "seller": "Nespresso Store", "brand": "Nespresso", "rating": 4.4, "reviews_count": 2134,
        "in_stock": True, "stock_quantity": 55,
        "tags": ["coffee", "espresso", "single-serve", "premium"],
        "specifications": {"technology": "Centrifusion", "cup_sizes": "5 sizes", "water_tank": "37 oz"}
    },
    {
        "name": "Le Creuset Dutch Oven 5.5 Qt",
        "description": "Premium enameled cast iron Dutch oven, perfect for braising, roasting, and slow cooking",
        "category": "Home & Kitchen", "subcategory": "Cookware", "price": 349.99, "currency": "USD",
        "seller": "Le Creuset Store", "brand": "Le Creuset", "rating": 4.8, "reviews_count": 1876,
        "in_stock": True, "stock_quantity": 40,
        "tags": ["cookware", "dutch-oven", "premium", "cast-iron"],
        "specifications": {"material": "Enameled Cast Iron", "capacity": "5.5 Quart", "oven_safe": "500°F"}
    },
    
    # Sports & Fitness
    {
        "name": "Peloton Bike+",
        "description": "Premium exercise bike with rotating touchscreen, live and on-demand classes, and immersive fitness experience",
        "category": "Sports", "subcategory": "Fitness", "price": 2495.00, "currency": "USD",
        "seller": "Peloton Store", "brand": "Peloton", "rating": 4.6, "reviews_count": 3421,
        "in_stock": True, "stock_quantity": 10,
        "tags": ["exercise-bike", "fitness", "smart", "premium"],
        "specifications": {"display": "23.8-inch HD touchscreen", "resistance": "Magnetic", "classes": "Live + On-demand"}
    },
    {
        "name": "Hydro Flask Water Bottle 32oz",
        "description": "Insulated stainless steel water bottle that keeps drinks cold for 24 hours or hot for 12 hours",
        "category": "Sports", "subcategory": "Accessories", "price": 44.95, "currency": "USD",
        "seller": "Hydro Flask Store", "brand": "Hydro Flask", "rating": 4.7, "reviews_count": 8765,
        "in_stock": True, "stock_quantity": 150,
        "tags": ["water-bottle", "insulated", "stainless-steel", "outdoor"],
        "specifications": {"capacity": "32 oz", "material": "Stainless Steel", "insulation": "TempShield"}
    },
    {
        "name": "Garmin Forerunner 255 GPS Watch",
        "description": "Advanced GPS running watch with training metrics, music storage, and up to 14 days battery life",
        "category": "Sports", "subcategory": "Wearables", "price": 349.99, "currency": "USD",
        "seller": "Garmin Store", "brand": "Garmin", "rating": 4.5, "reviews_count": 1234,
        "in_stock": True, "stock_quantity": 45,
        "tags": ["smartwatch", "gps", "running", "fitness-tracker"],
        "specifications": {"battery": "14 days", "gps": "Multi-band", "music": "Storage + streaming"}
    },
    
    # Beauty & Personal Care
    {
        "name": "Dyson Airwrap Hair Styler",
        "description": "Revolutionary hair styling tool that uses air to curl, wave, smooth, and dry hair without extreme heat",
        "category": "Beauty", "subcategory": "Hair Care", "price": 599.99, "currency": "USD",
        "seller": "Dyson Store", "brand": "Dyson", "rating": 4.4, "reviews_count": 5432,
        "in_stock": True, "stock_quantity": 25,
        "tags": ["hair-styler", "beauty", "technology", "premium"],
        "specifications": {"technology": "Coanda airflow", "heat_damage": "No extreme heat", "attachments": "Multiple"}
    },
    {
        "name": "Glossier Cloud Paint Blush",
        "description": "Seamless gel-cream blush that blends into skin for a natural, dewy flush that looks like it's coming from within",
        "category": "Beauty", "subcategory": "Makeup", "price": 20.00, "currency": "USD",
        "seller": "Glossier Store", "brand": "Glossier", "rating": 4.3, "reviews_count": 2876,
        "in_stock": True, "stock_quantity": 200,
        "tags": ["blush", "makeup", "natural", "cream"],
        "specifications": {"type": "Gel-cream", "finish": "Dewy", "application": "Buildable"}
    },
    
    # Books & Media
    {
        "name": "Kindle Paperwhite 11th Generation",
        "description": "Waterproof e-reader with adjustable warm light, weeks of battery life, and access to millions of books",
        "category": "Books", "subcategory": "E-readers", "price": 139.99, "currency": "USD",
        "seller": "Amazon Store", "brand": "Amazon", "rating": 4.6, "reviews_count": 12543,
        "in_stock": True, "stock_quantity": 70,
        "tags": ["e-reader", "books", "waterproof", "kindle"],
        "specifications": {"display": "6.8-inch E Ink", "storage": "8GB", "battery": "Up to 10 weeks"}
    },
    
    # Automotive
    {
        "name": "Tesla Model S Plaid",
        "description": "High-performance electric sedan with tri-motor all-wheel drive, 1,020 horsepower, and 390-mile range",
        "category": "Automotive", "subcategory": "Electric Vehicles", "price": 135999.99, "currency": "USD",
        "seller": "Tesla Store", "brand": "Tesla", "rating": 4.8, "reviews_count": 234,
        "in_stock": True, "stock_quantity": 5,
        "tags": ["electric-car", "luxury", "performance", "tesla"],
        "specifications": {"range": "390 miles", "acceleration": "0-60 mph in 1.99s", "top_speed": "200 mph"}
    },
    
    # Toys & Games
    {
        "name": "LEGO Creator Expert Taj Mahal",
        "description": "Detailed architectural LEGO set with 5923 pieces, perfect for display and a rewarding building experience",
        "category": "Toys", "subcategory": "Building Sets", "price": 369.99, "currency": "USD",
        "seller": "LEGO Store", "brand": "LEGO", "rating": 4.9, "reviews_count": 876,
        "in_stock": True, "stock_quantity": 20,
        "tags": ["lego", "building", "architecture", "collectible"],
        "specifications": {"pieces": "5923", "age": "18+", "dimensions": "20 x 20 x 16 inches"}
    },
    
    # Additional products to reach 50 total
    {
        "name": "Vitamix A3500 Ascent Blender",
        "description": "Professional-grade blender with smart technology, variable speed control, and self-cleaning program",
        "category": "Home & Kitchen", "subcategory": "Appliances", "price": 549.99, "currency": "USD",
        "seller": "Vitamix Store", "brand": "Vitamix", "rating": 4.7, "reviews_count": 1987,
        "in_stock": True, "stock_quantity": 35,
        "tags": ["blender", "smoothies", "professional", "healthy"],
        "specifications": {"container": "64 oz", "programs": "5 program settings", "technology": "Smart-detect"}
    },
    {
        "name": "Herman Miller Aeron Chair",
        "description": "Ergonomic office chair with advanced PostureFit SL back support, breathable mesh, and 12-year warranty",
        "category": "Furniture", "subcategory": "Office", "price": 1395.00, "currency": "USD",
        "seller": "Herman Miller Store", "brand": "Herman Miller", "rating": 4.8, "reviews_count": 3421,
        "in_stock": True, "stock_quantity": 15,
        "tags": ["office-chair", "ergonomic", "premium", "work-from-home"],
        "specifications": {"size": "Size B (Medium)", "material": "8Z Pellicle mesh", "warranty": "12 years"}
    },
    {
        "name": "Weber Genesis II E-335 Gas Grill",
        "description": "Premium 3-burner gas grill with porcelain-enameled cast iron grates and Weber CONNECT smart technology",
        "category": "Home & Garden", "subcategory": "Grills", "price": 899.99, "currency": "USD",
        "seller": "Weber Store", "brand": "Weber", "rating": 4.6, "reviews_count": 1543,
        "in_stock": True, "stock_quantity": 20,
        "tags": ["grill", "gas", "outdoor", "cooking"],
        "specifications": {"burners": "3", "cooking_area": "669 sq inches", "technology": "Weber CONNECT"}
    },
    {
        "name": "Ninja Foodi Personal Blender",
        "description": "Compact personal blender with Auto-iQ technology, perfect for smoothies, shakes, and nutrient extraction",
        "category": "Home & Kitchen", "subcategory": "Small Appliances", "price": 79.99, "currency": "USD",
        "seller": "Ninja Store", "brand": "Ninja", "rating": 4.4, "reviews_count": 2876,
        "in_stock": True, "stock_quantity": 85,
        "tags": ["blender", "personal", "smoothie", "compact"],
        "specifications": {"capacity": "18 oz", "technology": "Auto-iQ", "cups": "2 Nutrient Extraction cups"}
    },
    {
        "name": "Fitbit Charge 5 Fitness Tracker",
        "description": "Advanced fitness tracker with built-in GPS, stress management, and up to 7 days battery life",
        "category": "Sports", "subcategory": "Wearables", "price": 179.95, "currency": "USD",
        "seller": "Fitbit Store", "brand": "Fitbit", "rating": 4.2, "reviews_count": 4321,
        "in_stock": True, "stock_quantity": 95,
        "tags": ["fitness-tracker", "health", "gps", "wearable"],
        "specifications": {"battery": "7 days", "gps": "Built-in", "sensors": "Heart rate, SpO2, stress"}
    },
    {
        "name": "Breville Smart Oven Air Fryer Pro",
        "description": "Countertop convection oven with air fry function, 13 cooking presets, and Element iQ technology",
        "category": "Home & Kitchen", "subcategory": "Appliances", "price": 399.99, "currency": "USD",
        "seller": "Breville Store", "brand": "Breville", "rating": 4.5, "reviews_count": 1876,
        "in_stock": True, "stock_quantity": 30,
        "tags": ["oven", "air-fryer", "convection", "smart"],
        "specifications": {"capacity": "1 cubic foot", "functions": "13", "technology": "Element iQ"}
    },
    {
        "name": "Patagonia Houdini Jacket",
        "description": "Ultra-lightweight windbreaker made from recycled nylon, packable design, and DWR finish",
        "category": "Fashion", "subcategory": "Outerwear", "price": 99.00, "currency": "USD",
        "seller": "Patagonia Store", "brand": "Patagonia", "rating": 4.4, "reviews_count": 1234,
        "in_stock": True, "stock_quantity": 70,
        "tags": ["jacket", "windbreaker", "lightweight", "packable"],
        "specifications": {"material": "Recycled nylon", "weight": "3.1 oz", "packable": "Into chest pocket"}
    },
    {
        "name": "Yeti Rambler 20oz Tumbler",
        "description": "Insulated stainless steel tumbler with MagSlider lid, keeps drinks cold or hot for hours",
        "category": "Home & Kitchen", "subcategory": "Drinkware", "price": 34.99, "currency": "USD",
        "seller": "Yeti Store", "brand": "Yeti", "rating": 4.6, "reviews_count": 5432,
        "in_stock": True, "stock_quantity": 120,
        "tags": ["tumbler", "insulated", "stainless-steel", "travel"],
        "specifications": {"capacity": "20 oz", "material": "Stainless steel", "lid": "MagSlider"}
    },
    {
        "name": "Apple AirPods Pro 2nd Generation",
        "description": "Premium wireless earbuds with active noise cancellation, spatial audio, and adaptive transparency",
        "category": "Electronics", "subcategory": "Audio", "price": 249.99, "currency": "USD",
        "seller": "Apple Store", "brand": "Apple", "rating": 4.7, "reviews_count": 8765,
        "in_stock": True, "stock_quantity": 100,
        "tags": ["earbuds", "wireless", "noise-canceling", "apple"],
        "specifications": {"chip": "H2", "battery": "6 hours + 24 hours case", "features": "Spatial Audio, ANC"}
    },
    {
        "name": "REI Co-op Merino Wool Long-Sleeve Base Layer",
        "description": "Premium merino wool base layer with odor resistance, temperature regulation, and comfortable fit",
        "category": "Fashion", "subcategory": "Activewear", "price": 84.95, "currency": "USD",
        "seller": "REI Co-op", "brand": "REI Co-op", "rating": 4.5, "reviews_count": 987,
        "in_stock": True, "stock_quantity": 80,
        "tags": ["base-layer", "merino-wool", "outdoor", "activewear"],
        "specifications": {"material": "100% Merino Wool", "weight": "195 gsm", "care": "Machine washable"}
    },
    {
        "name": "Sonos Beam Gen 2 Soundbar",
        "description": "Compact smart soundbar with Dolby Atmos, voice control, and seamless music streaming",
        "category": "Electronics", "subcategory": "Audio", "price": 449.99, "currency": "USD",
        "seller": "Sonos Store", "brand": "Sonos", "rating": 4.6, "reviews_count": 2341,
        "in_stock": True, "stock_quantity": 40,
        "tags": ["soundbar", "smart", "dolby-atmos", "streaming"],
        "specifications": {"audio": "Dolby Atmos", "voice_control": "Alexa, Google", "connectivity": "Wi-Fi, HDMI eARC"}
    },
    {
        "name": "Allbirds Tree Dasher 2",
        "description": "Performance running shoes made from eucalyptus tree fiber with responsive midsole and breathable design",
        "category": "Sports", "subcategory": "Running", "price": 128.00, "currency": "USD",
        "seller": "Allbirds Store", "brand": "Allbirds", "rating": 4.3, "reviews_count": 1876,
        "in_stock": True, "stock_quantity": 75,
        "tags": ["running", "sustainable", "performance", "eco-friendly"],
        "specifications": {"upper": "Tree fiber", "midsole": "SweetFoam", "outsole": "Natural rubber"}
    },
    {
        "name": "Stanley Adventure Quencher 40oz",
        "description": "Insulated stainless steel tumbler with handle, straw lid, and all-day ice retention",
        "category": "Home & Kitchen", "subcategory": "Drinkware", "price": 44.99, "currency": "USD",
        "seller": "Stanley Store", "brand": "Stanley", "rating": 4.8, "reviews_count": 12345,
        "in_stock": True, "stock_quantity": 200,
        "tags": ["tumbler", "insulated", "large-capacity", "travel"],
        "specifications": {"capacity": "40 oz", "insulation": "Double-wall vacuum", "ice_retention": "11+ hours"}
    },
    {
        "name": "Patagonia Better Sweater Fleece Jacket",
        "description": "Classic fleece jacket made from recycled polyester with full-zip design and comfortable fit",
        "category": "Fashion", "subcategory": "Outerwear", "price": 139.00, "currency": "USD",
        "seller": "Patagonia Store", "brand": "Patagonia", "rating": 4.6, "reviews_count": 3421,
        "in_stock": True, "stock_quantity": 60,
        "tags": ["fleece", "jacket", "recycled", "outdoor"],
        "specifications": {"material": "Recycled polyester fleece", "closure": "Full-zip", "pockets": "2 zippered handwarmer"}
    },
    {
        "name": "Theragun Elite Massage Gun",
        "description": "Professional-grade percussive therapy device with smart app integration and customizable speed range",
        "category": "Sports", "subcategory": "Recovery", "price": 399.99, "currency": "USD",
        "seller": "Therabody Store", "brand": "Therabody", "rating": 4.5, "reviews_count": 2187,
        "in_stock": True, "stock_quantity": 35,
        "tags": ["massage-gun", "recovery", "therapy", "fitness"],
        "specifications": {"battery": "120 minutes", "speed_range": "1750-2400 PPM", "app": "Therabody app"}
    },
    {
        "name": "Ember Temperature Control Smart Mug",
        "description": "App-controlled heated mug that maintains your perfect drinking temperature for hot beverages",
        "category": "Home & Kitchen", "subcategory": "Drinkware", "price": 129.95, "currency": "USD",
        "seller": "Ember Store", "brand": "Ember", "rating": 4.3, "reviews_count": 1543,
        "in_stock": True, "stock_quantity": 50,
        "tags": ["smart-mug", "temperature-control", "app-controlled", "coffee"],
        "specifications": {"capacity": "14 oz", "battery": "80 minutes", "app_control": "Yes", "temp_range": "120°F - 145°F"}
    }
]

# Combine all products
all_products = sample_products + additional_products

# Add timestamps and product IDs
for i, product in enumerate(all_products):
    product["product_id"] = f"PROD_{str(i+1).zfill(4)}"
    product["created_at"] = datetime.utcnow()
    product["updated_at"] = datetime.utcnow()
    product["views"] = random.randint(100, 5000)
    product["sales_count"] = random.randint(10, 500)
    product["featured"] = random.choice([True, False])
    product["free_shipping"] = random.choice([True, False])
    product["returnable"] = True
    product["warranty_months"] = random.choice([6, 12, 24, 36])

# Insert products into MongoDB
try:
    # Clear existing data
    collection.delete_many({})
    
    # Insert new products
    result = collection.insert_many(all_products)
    print(f"Successfully inserted {len(result.inserted_ids)} products into MongoDB")
    
    # Create indexes for better search performance
    collection.create_index([("name", "text"), ("description", "text"), ("tags", "text")])
    collection.create_index("category")
    collection.create_index("subcategory")
    collection.create_index("brand")
    collection.create_index("price")
    collection.create_index("rating")
    
    print("Indexes created successfully")
    
except Exception as e:
    print(f"Error inserting products: {e}")

finally:
    client.close()