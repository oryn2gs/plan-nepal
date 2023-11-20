from django.test import TestCase
from django.urls import reverse
from testimonials.models import Testimonial
from packages.models import (
    Package, 
    TourTimeline, 
    Destination,
    Type
    )

from django.contrib.auth import get_user_model
User = get_user_model()

class HomepageTestCase(TestCase):
    """ Test where the needed data is present in the response """

    def setUp(self) -> None:
        
        self.url = reverse('homepage')
        
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        self.destination = Destination.objects.create(name = 'Destination 1')
        self.type1 = Type.objects.create(name="Type 1")
        self.type2 = Type.objects.create(name="Type 2")
        
        self.package1 = Package.objects.create(
            name = "Package 1",
            destination = self.destination,
            price = 100.00
        )
        self.package1.type.add(self.type1)
        
        self.package2 = Package.objects.create(
            name = "Package 2",
            destination = self.destination,
            price = 100.00
        )
        self.package2.type.add(self.type2)

        Testimonial.objects.bulk_create([
            Testimonial(user=self.user, content='test content for testimonial')
            for _ in range(7)
        ])

    def test_packages_in_context(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/homepage.html')
        self.assertTrue(response.context['packages']) 
        self.assertIn(self.package1, response.context['packages'])
        self.assertEqual(len(response.context['packages']), 2)

    def test_packages_with_type_filter_in_context(self) -> None:
        response = self.client.get(self.url, {"type_filter": "type 1"})
        
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['packages']) 
        self.assertIn(self.package1, response.context['packages'])
        self.assertEqual(len(response.context['packages']), 1)

    
    def test_popular_in_context(self)-> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['popular']) 
    
    def test_types_in_context(self)-> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['types']) 
    
    def test_testimonial_in_context(self)-> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['testimonials']) 
        self.assertEqual(len(response.context['testimonials']), 6)

class PackageDetailTestCase(TestCase):

    def setUp(self) -> None:
        self.destination = Destination.objects.create(name="Destination 1")
        self.type = Type.objects.create(name="Type 1")
        self.package = Package.objects.create(
            name = "package",
            destination = self.destination,
            price = 100.00
        )
        self.package.type.add(self.type)

        TourTimeline.objects.bulk_create([
            TourTimeline(
                tour_timeline=self.package, 
                stop_name="test_name", 
                day=f"{i}", 
                )
            for i in range(1,5)
        ])

        self.url = reverse('package-detail', kwargs={'package_slug': self.package.slug})

    def test_package_detail(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package-detail.html')
        self.assertTrue(response.context['package']) 

    
    def test_package_detail_contains_tour_timeline(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['tour_timeline']) 
        self.assertTrue(len(response.context['tour_timeline']), 5)

    
class TestFilterPackagesView(TestCase):

    def setUp(self) -> None:
        self.destination = Destination.objects.create(name = 'Destination 1')
        self.type = Type.objects.create(name="Type 1")
        
        self.package1 = Package.objects.create(
            name = "Package 1",
            destination = self.destination,
            price = 100.00
        )
        self.package1.type.add(self.type)
        
        self.package2 = Package.objects.create(
            name = "Package 2",
            destination = self.destination,
            price = 100.00
        )

        self.url = reverse("packages-filter")

    def test_filter_packages_success(self) -> None:
        response = self.client.get(self.url, {"query": "type 1"})

        self.assertEqual(response.status_code, 200)



    

    

        


