from django.test import TestCase
from packages.models import (
    Package, 
    Destination, 
    Type
    )
from django.template import Template, Context


class TestCustomFilters(TestCase):

    def setUp(self) -> None:
        self.context = Context({"packages": Package.objects.all()}) # create a template context with queryset objects

        self.destination1 = Destination.objects.create(name="Destination 1")
        self.destination2 = Destination.objects.create(name="Destination 2")
        self.type1 = Type.objects.create(name="Type 1")
        self.type2 = Type.objects.create(name="Type 2")

 
        self.package1 = Package.objects.create(
            destination=self.destination1,
            name="Package 1",
            price = 100.00,
            active=True,
        )
        self.package1.type.add(self.type1, self.type2)  

        self.package2 = Package.objects.create(
            destination=self.destination2,
            name="Package 2",
            price = 100.00,
            active=True,
        )
        self.package2.type.add(self.type2)

        self.package3 = Package.objects.create(
            destination=self.destination1,
            name="Package 3",
            price = 100.00,
            active=True,
        )
        self.package3.type.add(self.type1)

        self.package4 = Package.objects.create(
            destination=self.destination2,
            name="Package 4",
            price = 100.00,
            active=False,  # This package is not active
        )
        self.package4.type.add(self.type2)


    def test_filter_packages_with_destination(self):

        rendered = Template(
            "{% load custom_filters %}"
            "{% for package in packages|filter_packages_by_destination:'Destination 1' %}"
            "{{ package.name }} "
            "{% endfor %}"
        ).render(self.context)

        # render contain should have a package 1 and 3
        self.assertIn("Package 1", rendered)
        self.assertIn("Package 3", rendered)
        self.assertNotIn("Package 2", rendered)
        self.assertNotIn("Package 4", rendered)

    def test_filter_packages_with_type(self):

        rendered = Template(
            "{% load custom_filters %}"
            "{% for package in packages|filter_packages_by_type:'Type 2' %}"
            "{{ package.name }} "
            "{% endfor %}"
        ).render(self.context)

        self.assertIn("Package 1", rendered)
        self.assertIn("Package 2", rendered)
        self.assertNotIn("Package 3", rendered)
        self.assertNotIn("Package 4", rendered)


