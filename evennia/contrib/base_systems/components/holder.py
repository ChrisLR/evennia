"""
Components - ChrisLR 2022

This file contains the classes that allow a typeclass to use components.
"""

from evennia.contrib.base_systems import components
from evennia.contrib.base_systems.components import signals, exceptions


class ComponentProperty:
    """
    This allows you to register a component on a typeclass.
    Components registered with this property are automatically added
    to any instance of this typeclass.

    Defaults can be overridden for this typeclass by passing kwargs
    """

    def __init__(self, component_key, **kwargs):
        """
        Initializes the descriptor

        Args:
            component_key (str): The key of the component
            **kwargs (any): Key=Values overriding default values of the component
        """
        self.component_key = component_key
        self.values = kwargs

    def __get__(self, instance, owner):
        component = instance.components.get_by_key(self.component_key)
        return component

    def __set__(self, instance, value):
        raise Exception("Cannot set a class property")

    def __set_name__(self, owner, name):
        # Retrieve the class_components set on the direct class only
        class_components = owner.__dict__.get("_class_components")
        if not class_components:
            # Create a new list, including inherited class components
            class_components = list(getattr(owner, "_class_components", []))
            setattr(owner, "_class_components", class_components)

        class_components.append((self.component_key, self.values))


class ComponentHandler:
    """
    This is the handler that will be added to any typeclass that inherits from ComponentHolder.
    It lets you add or remove components and will load components as needed.
    It stores the list of registered components on the host .db with component_names as key.
    """

    def __init__(self, host):
        self.host = host
        self._loaded_components = {}

    def add(self, component: components.Component):
        """
        Method to add a Component to a host.
        It caches the loaded component and appends its name to the host's component name list.
        It will also call the component's 'at_added' method, passing its host.

        Args:
            component (object): The 'loaded' component instance to add.

        """
        component_key = component.get_component_key()
        self.db_keys.append(component_key)
        self._set_component(component)
        self._add_component_tags(component)
        component.at_added(self.host)

    def add_default(self, key):
        """
        Method to add a Component initialized to default values on a host.
        It will retrieve the proper component and instantiate it with 'default_create'.
        It will cache this new component and add it to its list.
        It will also call the component's 'at_added' method, passing its host.

        Args:
            key (str): The key of the component class to add.

        """
        component_class = components.get_component_class(key)
        component_instance = component_class.default_create(self.host)
        self.add(component_instance)

    def remove(self, component: components.Component):
        """
        Method to remove a component instance from a host.
        It removes the component from the cache and listing.
        It will call the component's 'at_removed' method.

        Args:
            component (object): The component instance to remove.

        """
        slot_key = component.get_component_slot()
        if not self.has_slot(slot_key):
            message = (
                f"Cannot remove {slot_key} from {self.host.name} as it is not registered."
            )
            raise exceptions.ComponentIsNotRegistered(message)

        component.at_removed(self.host)
        if component.cmd_set:
            self.host.cmdset.remove(component.cmd_set)

        self._remove_component_tags(component)
        self.host.signals.remove_object_listeners_and_responders(component)
        self.db_keys.remove(slot_key)
        del self._loaded_components[slot_key]

    def remove_by_slot_key(self, slot_key):
        """
        Method to remove a component instance from a host.
        It removes the component from the cache and listing.
        It will call the component's 'at_removed' method.

        Args:
            slot_key (str): The slot_key of the component to remove.

        """
        instance = self.get_by_slot(slot_key)
        if not instance:
            message = f"Cannot remove {slot_key} from {self.host.name} as it is not registered."
            raise exceptions.ComponentIsNotRegistered(message)

        self.remove(instance)

    def _remove_component_tags(self, component: components.Component):
        """
        Private method that will remove the Tags set on a Component via TagFields
        It will also remove the component name tag.

        Args:
            component (object): The component instance that is removed.
        """
        self.host.tags.remove(component.get_component_key(), category="components")
        for tag_field_name in component.tag_field_names:
            delattr(component, tag_field_name)

    def get_by_key(self, component_key):
        return self._loaded_components.get(component_key)

    def get_by_slot(self, slot_key) -> components.Component | None:
        """
        Method to retrieve a cached Component instance by its name.

        Args:
            slot_key (str): The slot key of the component to retrieve.

        """
        return self._loaded_components.get(slot_key)

    def has_slot(self, slot_key: str) -> bool:
        """
        Method to check if a component is registered and ready.

        Args:
            slot_key (str): The name of the component.

        """
        return slot_key in self._loaded_components

    def initialize(self):
        """
        Method that loads and caches each component currently registered on the host.
        It retrieves the names from the registered listing and calls 'load' on each
        prototype class that can be found from this listing.

        """
        component_keys = self.db_keys
        if not component_keys:
            return

        for component_key in component_keys:
            component = components.get_component_class(component_key)
            if component:
                component_instance = component.load(self.host)
                self._set_component(component_instance)
            else:
                message = (
                    f"Could not initialize runtime component {component_key} of {self.host.name}"
                )
                raise exceptions.ComponentDoesNotExist(message)

    def _set_component(self, component):
        """
        Sets the loaded component in this instance.
        """
        component_key = component.get_component_key()
        slot_key = component.get_component_slot()
        self._loaded_components[slot_key] = component
        self._loaded_components[component_key] = component
        self.host.signals.add_object_listeners_and_responders(component)

    @property
    def db_keys(self):
        """
        Property shortcut to retrieve the registered component keys

        Returns:
            component_names (iterable): The key of each component that is registered

        """
        component_keys = self.host.attributes.get("component_keys")
        if component_keys is None:
            self.host.db.component_keys = []
            component_keys = self.host.db.component_keys
            if legacy_names := self.host.attributes.get("component_names"):
                component_keys.extend(legacy_names)

        return component_keys

    def _add_component_tags(self, component: components.Component):
        """
        Private method that adds the Tags set on a Component via TagFields
        It will also add the name of the component so objects can be filtered
        by the components the implement.

        Args:
            component (object): The component instance that is added.
        """
        slot_key = component.get_component_slot()
        self.host.tags.add(slot_key, category="components")
        for tag_field_name in component.tag_field_names:
            default_tag = type(component).__dict__[tag_field_name]._default
            if default_tag:
                setattr(component, tag_field_name, default_tag)

    def __getattr__(self, slot_key):
        return self.get_by_slot(slot_key)


class ComponentHolderMixin:
    """
    Mixin to add component support to a typeclass

    Components are set on objects using the component.name as an object attribute.
    All registered components are initialized on the typeclass.
    They will be of None value if not present in the class components or runtime components.
    """

    def at_init(self):
        """
        Method that initializes the ComponentHandler.
        """
        super(ComponentHolderMixin, self).at_init()
        setattr(self, "_component_handler", ComponentHandler(self))
        setattr(self, "_signal_handler", signals.SignalsHandler(self))
        self.components.initialize()
        self.signals.trigger("at_after_init")

    def at_post_puppet(self, *args, **kwargs):
        super().at_post_puppet(*args, **kwargs)
        self.signals.trigger("at_post_puppet", *args, **kwargs)

    def at_post_unpuppet(self, *args, **kwargs):
        super().at_post_unpuppet(*args, **kwargs)
        self.signals.trigger("at_post_unpuppet", *args, **kwargs)

    def basetype_setup(self):
        """
        Method that initializes the ComponentHandler, creates and registers all
        components that were set on the typeclass using ComponentProperty.
        """
        super().basetype_setup()
        setattr(self, "_component_handler", ComponentHandler(self))
        setattr(self, "_signal_handler", signals.SignalsHandler(self))
        class_components = getattr(self, "_class_components", ())
        for component_key, values in class_components:
            component_class = components.get_component_class(component_key)
            component = component_class.create(self, **values)
            self.components.add(component)

        self.signals.trigger("at_basetype_setup")

    @property
    def components(self) -> ComponentHandler:
        """
        Property getter to retrieve the component_handler.
        Returns:
            ComponentHandler: This Host's ComponentHandler
        """
        return getattr(self, "_component_handler", None)

    @property
    def cmp(self) -> ComponentHandler:
        """
        Shortcut Property getter to retrieve the component_handler.
        Returns:
            ComponentHandler: This Host's ComponentHandler
        """
        return self.components

    @property
    def signals(self) -> signals.SignalsHandler:
        return getattr(self, "_signal_handler", None)
