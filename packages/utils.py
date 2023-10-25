from packages.models import Package, Type


def _get_most_popular_packages() -> list:
    queryset = Package.objects.all()
    #Todos: filter the packages by most viewed, top bookings and most inquired

    return queryset


def _get_types_list() -> list:
    """ returns the list of type name """
    queryset = Type.objects.all()
    types_list = [type.name for type in queryset]
    
    return types_list