from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing, Booking, Review
from datetime import datetime, timedelta
import random
import uuid


class Command(BaseCommand):
    help = 'Populate the database with sample listings, bookings, and reviews data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create (default: 25)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        listings_count = options['listings']
        bookings_count = options['bookings']
        reviews_count = options['reviews']
        
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared existing data')
            )

        # Sample data for listings
        titles = [
            "Luxury Downtown Apartment",
            "Cozy Beach House", 
            "Modern City Loft",
            "Charming Cottage",
            "Spacious Family Home",
            "Beachfront Villa",
            "Mountain Cabin Retreat",
            "Historic Townhouse",
            "Studio in Arts District",
            "Garden View Apartment",
            "Penthouse Suite",
            "Rustic Country House",
            "Contemporary Condo",
            "Elegant Victorian Home",
            "Minimalist Urban Space",
            "Lakefront Property",
            "Desert Oasis Villa",
            "Ski Lodge Chalet",
            "Tropical Paradise",
            "Metropolitan High-Rise"
        ]

        descriptions = [
            "Beautiful property with stunning views and modern amenities perfect for your stay.",
            "Ideal for families and groups, featuring spacious rooms and excellent location.",
            "Prime location with easy access to attractions, shopping and entertainment venues.",
            "Newly renovated with high-end finishes and all the comforts of home.",
            "Quiet neighborhood setting with peaceful surroundings and great accessibility.",
            "Open floor plan perfect for relaxation and entertaining during your visit.",
            "Fully equipped property with everything you need for a memorable stay.",
            "Historic charm combined with modern conveniences and unique character.",
            "Perfect for business travelers and tourists seeking comfort and convenience.",
            "Exceptional property offering luxury amenities and unforgettable experiences."
        ]

        locations = [
            "Downtown Manhattan, New York",
            "Santa Monica, Los Angeles", 
            "Lincoln Park, Chicago",
            "South Beach, Miami",
            "Capitol Hill, Seattle",
            "French Quarter, New Orleans",
            "Nob Hill, San Francisco",
            "Back Bay, Boston",
            "Uptown, Dallas",
            "Pearl District, Portland",
            "Midtown, Atlanta",
            "Gaslamp Quarter, San Diego",
            "River North, Chicago",
            "SoHo, New York",
            "Venice Beach, Los Angeles",
            "Georgetown, Washington DC",
            "Fisherman's Wharf, San Francisco",
            "Wynwood, Miami",
            "Capitol Hill, Denver",
            "Old Town, Scottsdale"
        ]

        guest_names = [
            "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis",
            "David Wilson", "Jessica Garcia", "Christopher Miller", "Amanda Taylor",
            "Matthew Anderson", "Ashley Thomas", "James Jackson", "Jennifer White",
            "Robert Harris", "Lisa Martin", "William Thompson", "Michelle Garcia",
            "Daniel Rodriguez", "Laura Martinez", "Joseph Robinson", "Karen Clark"
        ]

        booking_statuses = ["confirmed", "pending", "cancelled", "completed"]
        
        # Create Listings
        self.stdout.write('Creating listings...')
        listings_created = 0
        
        for i in range(listings_count):
            try:
                title = random.choice(titles)
                description = random.choice(descriptions)
                location = random.choice(locations)
                is_available = random.choice([True, True, True, False])  # 75% available
                
                listing = Listing.objects.create(
                    title=title,
                    description=description,
                    location=location,
                    is_available=is_available
                )
                
                listings_created += 1
                
                if listings_created % 5 == 0:
                    self.stdout.write(f'Created {listings_created} listings...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating listing {i+1}: {str(e)}')
                )

        # Create Bookings
        if listings_created > 0:
            self.stdout.write('Creating bookings...')
            bookings_created = 0
            all_listings = list(Listing.objects.all())
            
            for i in range(bookings_count):
                try:
                    listing = random.choice(all_listings)
                    guest_name = random.choice(guest_names)
                    status = random.choice(booking_statuses)
                    
                    # Generate random check-in and check-out dates
                    check_in_days = random.randint(-30, 60)  # 30 days ago to 60 days future
                    check_in = timezone.now() + timedelta(days=check_in_days)
                    check_out = check_in + timedelta(days=random.randint(1, 14))  # 1-14 day stays
                    
                    booking = Booking.objects.create(
                        listing=listing,
                        guest_name=guest_name,
                        status=status,
                        check_in=check_in,
                        check_out=check_out
                    )
                    
                    bookings_created += 1
                    
                    if bookings_created % 10 == 0:
                        self.stdout.write(f'Created {bookings_created} bookings...')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating booking {i+1}: {str(e)}')
                    )

            # Create Reviews
            self.stdout.write('Creating reviews...')
            reviews_created = 0
            
            review_comments = [
                "Amazing place! Everything was perfect and exactly as described.",
                "Great location and very clean. Would definitely stay again.",
                "Host was very responsive and helpful. Highly recommended!",
                "Beautiful property with stunning views. Loved every minute.",
                "Perfect for our family vacation. Very comfortable and well-equipped.",
                "Excellent value for money. Great amenities and location.",
                "The photos don't do it justice - even better in person!",
                "Wonderful stay, everything we needed was provided.",
                "Very peaceful and relaxing environment. Just what we needed.",
                "Outstanding property with exceptional attention to detail."
            ]
            
            for i in range(reviews_count):
                try:
                    listing = random.choice(all_listings)
                    guest_name = random.choice(guest_names)
                    rating = str(random.randint(3, 5))  # 3-5 star ratings mostly
                    comment = random.choice(review_comments)
                    
                    review = Review.objects.create(
                        listing=listing,
                        guest_name=guest_name,
                        rating=rating,
                        comment=comment
                    )
                    
                    reviews_created += 1
                    
                    if reviews_created % 10 == 0:
                        self.stdout.write(f'Created {reviews_created} reviews...')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating review {i+1}: {str(e)}')
                    )

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:'
                f'\n  - {listings_created} listings'
                f'\n  - {bookings_created if listings_created > 0 else 0} bookings'
                f'\n  - {reviews_created if listings_created > 0 else 0} reviews'
            )
        )
        
        # Display statistics
        total_listings = Listing.objects.count()
        available_listings = Listing.objects.filter(is_available=True).count()
        total_bookings = Booking.objects.count()
        total_reviews = Review.objects.count()
        
        self.stdout.write(f'\nDatabase totals:')
        self.stdout.write(f'  - Total listings: {total_listings}')
        self.stdout.write(f'  - Available listings: {available_listings}')
        self.stdout.write(f'  - Total bookings: {total_bookings}')
        self.stdout.write(f'  - Total reviews: {total_reviews}')