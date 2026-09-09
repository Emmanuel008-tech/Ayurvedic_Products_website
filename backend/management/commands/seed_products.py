from django.core.management.base import BaseCommand
from backend.models import Product


class Command(BaseCommand):
    help = "Seed initial AyuDhara Ayurvedic products into database with stock levels"

    def handle(self, *args, **options):
        products_data = [
            {
                "name": "KeshVeda Herbal Hair Oil",
                "category": "hair_care",
                "price": 499.00,
                "stock_quantity": 38,
                "description": "Slow-infused Bhringraj, Amla, Brahmi, and sesame oil crafted using traditional Taila Paka Vidhi. Strengthens roots, prevents premature graying, and promotes dense hair growth.",
                "image": "products/hair_oil.jpg"
            },
            {
                "name": "Kumkumadi Radiant Face Pack",
                "category": "face_care",
                "price": 650.00,
                "stock_quantity": 24,
                "description": "Formulated with pure Kashmiri Saffron (Kumkuma), Sandalwood, Lodhra, and Licorice. Deeply brightens complexion, diminishes dark spots, and imparts a natural glow.",
                "image": "products/face_pack.jpg"
            },
            {
                "name": "Shikakai & Hibiscus Herbal Shampoo",
                "category": "hair_care",
                "price": 389.00,
                "stock_quantity": 16,
                "description": "A 100% natural, sulfate-free cleanser enriched with raw Shikakai, Reetha soapnuts, and fresh Red Hibiscus petals. Gently cleanses without stripping natural oils.",
                "image": "products/shampoo.jpg"
            },
            {
                "name": "Chandan & Eladi Body Oil",
                "category": "body_care",
                "price": 799.00,
                "stock_quantity": 9,
                "description": "Luxurious Abhyanga body massage oil featuring Red Sandalwood, Ela (Cardamom), and cold-pressed Sesame oil. Soothes dry skin, enhances elasticity, and relaxes muscle stress.",
                "image": "products/body_oil.jpg"
            }
        ]

        count = 0
        for item in products_data:
            obj, created = Product.objects.update_or_create(
                name=item["name"],
                defaults={
                    "category": item["category"],
                    "price": item["price"],
                    "stock_quantity": item["stock_quantity"],
                    "description": item["description"],
                    "image": item["image"],
                    "is_active": True
                }
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Created product: {obj.name} (Stock: {obj.stock_quantity})"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated product: {obj.name} (Stock: {obj.stock_quantity})"))

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(products_data)} AyuDhara products ({count} new)."))
