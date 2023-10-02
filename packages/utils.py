from packages.models import Package


def get_most_popular_packages() -> list:
    queryset = Package.objects.all()
    #Todos: filter the packages by most viewed, top bookings and most inquired

    return queryset