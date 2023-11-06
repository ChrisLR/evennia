from evennia.contrib.base_systems.components import exceptions

COMPONENT_LISTING = {}


def get_component_class(component_key):
    component_class = COMPONENT_LISTING.get(component_key)
    if component_class is None:
        message = (
            f"Component with key {component_key} has not been found. "
            f"Make sure it has been imported before being used."
        )
        raise exceptions.ComponentDoesNotExist(message)

    return component_class
