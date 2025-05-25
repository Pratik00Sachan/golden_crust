from golden_crust_bakery.app import app, db, Product

def seed_products():
    """Seeds the database with initial product data."""
    products_data = [
        {
            "name": "Classic Sourdough",
            "description": "Traditional sourdough with a crisp crust and tangy flavor. Made with organic flour and a long fermentation process.",
            "price": 7.00,
            "variety": "Sourdough",
            "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec"
        },
        {
            "name": "Whole Wheat Wonder",
            "description": "Nutritious whole wheat bread packed with fiber and natural goodness. Hearty and wholesome.",
            "price": 6.00,
            "variety": "Whole Wheat",
            "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73"
        },
        {
            "name": "Multigrain Medley",
            "description": "A hearty blend of grains and seeds (flax, sesame, sunflower) for maximum flavor and texture.",
            "price": 7.50,
            "variety": "Multigrain",
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff"
        },
        {
            "name": "French Baguette",
            "description": "Classic French baguette with a crispy crust and soft, chewy interior. Perfect for sandwiches or with cheese.",
            "price": 5.00,
            "variety": "Artisan",
            "image_url": "https://images.unsplash.com/photo-1517686469429-8bdb88b9f907"
        },
        {
            "name": "Rye Resilience",
            "description": "A dark and flavorful rye bread with a dense texture. Great for savory pairings.",
            "price": 6.50,
            "variety": "Rye",
            "image_url": "https://via.placeholder.com/300x200.png?text=Rye+Resilience"
        },
        {
            "name": "Ciabatta Cloud",
            "description": "An Italian white bread with a light, airy crumb and a slightly crisp crust. Ideal for dipping in olive oil.",
            "price": 5.50,
            "variety": "Artisan",
            "image_url": "https://via.placeholder.com/300x200.png?text=Ciabatta+Cloud"
        }
    ]

    with app.app_context():
        for p_data in products_data:
            existing_product = Product.query.filter_by(name=p_data["name"]).first()
            if not existing_product:
                product = Product(
                    name=p_data["name"],
                    description=p_data["description"],
                    price=p_data["price"],
                    variety=p_data["variety"],
                    image_url=p_data["image_url"]
                )
                db.session.add(product)
        
        db.session.commit()
    print("Products seeded successfully!")

if __name__ == '__main__':
    seed_products()
