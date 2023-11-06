from django.test import TestCase
from packages.models import (
    Destination, 
    Type, 
    Package,
    TourTimeline
) 
from django.urls import reverse

class DestinationModelTestCase(TestCase):
    """ Test for Destionation Model """

    def setUp(self) -> None:
        self.destination = Destination.objects.create(
            name = "Test Name"
        )
    
    def test_str_method(self) -> None:
        self.assertEqual(str(self.destination).lower(), "test name")



class TypeModelTestCase(TestCase):
    """ Test form Type Model """

    def setUp(self) -> None:
        self.type = Type.objects.create(
            name = "Test Name"
        )
    
    def test_str_method(self) -> None:
        self.assertEqual(str(self.type).lower(), "test name")


class PackageModelTestCase(TestCase): 
    """ Test for Packages Model """

    def setUp(self) -> None:
        self.destination1 = Destination.objects.create(name="Destination 1")
        self.destination2 = Destination.objects.create(name="Destination 2")
        self.type1 = Type.objects.create(name="Type 1")
        self.type2 = Type.objects.create(name="Type 2")

        self.package1 = Package.objects.create(
            destination=self.destination1,
            name="Package 1",
            price=100.00,
            discount= 10.00,
            active=True,
        )
        self.package1.type.add(self.type1, self.type2)  

        self.package2 = Package.objects.create(
            destination=self.destination2,
            name="Package 2",
            price=150.00,
            active=False,  # This package is not active
        )
        self.package2.type.add(self.type2)


    def test_str_method(self) -> None:
        self.assertEqual(str(self.package1), f"{self.package1.destination.name} | {self.package1.name}")

    def test_slug_created(self) -> None:
        self.assertEqual(self.package2.slug, "package-2")

    def test_package_absolute_url(self) -> None:
        actual_url = self.package1.get_absolute_url()
        expected_url = reverse('package-detail', kwargs={
            'package_slug': self.package1.slug
            })

        self.assertEqual(expected_url, actual_url)


    def test_get_final_price_after_discount(self) -> None:
        final_price = self.package1.get_final_price_after_discount
        self.assertEqual(final_price, self.package1.price - self.package1.discount)
        

    def test_filter_by_destination(self) -> None:
        results = Package.objects.filter_by_destination("Destination 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.package1)
    
    def test_filter_by_type_does_not_return_inactive_packages(self) -> None:
        results = Package.objects.filter_by_destination("destination 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.package1)



class TourTimelineModelTestCase(TestCase):

    def setUp(self) -> None:
        self.destination = Destination.objects.create(name="Destination 1")
        self.package = Package.objects.create(
            destination=self.destination,
            name="Test Package",
            description="Description for Test Package",
            price=100.00,
            active=True,
        )
        
        self.timeline1 = TourTimeline.objects.create(
            tour_timeline=self.package,
            stop_name="Stop 1",
            description="Description for Stop 1",
            day=1
        )
        self.timeline2 = TourTimeline.objects.create(
            tour_timeline=self.package,
            stop_name="Stop 2",
            description="Description for Stop 2",
            day=2
        )

    
    def test_filter_instance_related_to_package(self) -> None:
        results = TourTimeline.objects.filter_instance_related_to_package(
            package_slug=self.package.slug
            )
        self.assertIn(self.timeline1, results)
        self.assertIn(self.timeline2, results)

    
    def test_filter_instance_related_to_package_with_decending_order(self) -> None:
        results = TourTimeline.objects.filter_instance_related_to_package(
            package_slug=self.package.slug, 
            ascending=False
            )
        self.assertEqual(self.timeline2, results[0])


