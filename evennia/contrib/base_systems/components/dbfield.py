"""
Components - ChrisLR 2022

This file contains the Descriptors used to set Fields in Components
"""

import typing

from evennia.typeclasses.attributes import AttributeProperty, NAttributeProperty

if typing.TYPE_CHECKING:
    from .components import Component


class DBField(AttributeProperty):
    """
    Component Attribute Descriptor.
    Allows you to set attributes related to a component on the class.
    It uses AttributeProperty under the hood but prefixes the key with the component name.
    """

    def __init__(self, default=None, autocreate=False, **kwargs):
        super().__init__(default=default, autocreate=autocreate, **kwargs)

    def __set_name__(self, owner: "Component", name):
        """
        Called when descriptor is first assigned to the class.

        Args:
            owner (Component): The component classF on which this is set
            name (str): The name that was used to set the DBField.
        """
        self._key = f"{owner.get_component_slot()}::{name}"
        owner.add_field(name, self)

    def at_added(self, component):
        """
        Called when the parent component is added to a host.

        Args:
            component (Component): The component instance being added.
        """

        if self._autocreate:
            self.__get__(component, type(component))

    def at_removed(self, component):
        """
        Called when the parent component is removed from a host.

        Args:
            component (Component): The component instance being removed.
        """

        self.__delete__(component)


class NDBField(NAttributeProperty):
    """
    Component In-Memory Attribute Descriptor.
    Allows you to set in-memory attributes related to a component on the class.
    It uses NAttributeProperty under the hood but prefixes the key with the component name.
    """

    def __set_name__(self, owner: "Component", name):
        """
        Called when descriptor is first assigned to the class.

        Args:
            owner (Component): The component class on which this is set
            name (str): The name that was used to set the DBField.
        """
        self._key = f"{owner.get_component_slot()}::{name}"
        owner.add_field(name, self)

    def at_added(self, component):
        """
        Called when the parent component is added to a host.

        Args:
            component (Component): The component instance being added.
        """
        if self._autocreate:
            self.__set__(component, self._default)

    def at_removed(self, component):
        """
        Called when the parent component is removed from a host.

        Args:
            component (Component): The component instance being removed.
        """
        self.__delete__(component)


class TagField:
    """
    Component Tags Descriptor.
    Allows you to set Tags related to a component on the class.
    The tags are set with a prefixed category, so it can support
    multiple tags or enforce a single one.

    Default value of a tag is added when the component is registered.
    Tags are removed if the component itself is removed.
    """

    def __init__(self, default=None, enforce_single=False):
        self._category_key = None
        self._default = default
        self._enforce_single = enforce_single

    def __set_name__(self, owner: "Component", name):
        """
        Called when TagField is first assigned to the class.
        It is called with the component class and the name of the field.
        """
        self._category_key = f"{owner.get_component_slot()}::{name}"
        owner.add_field(name, self)

    def __get__(self, instance, owner):
        """
        Called when retrieving the value of the TagField.
        It is called with the component instance and the class.
        """
        tag_value = instance.host.tags.get(
            default=self._default,
            category=self._category_key,
        )
        return tag_value

    def __set__(self, instance, value):
        """
        Called when setting a value on the TagField.
        It is called with the component instance and the value.
        """

        tag_handler = instance.host.tags
        if self._enforce_single:
            tag_handler.clear(category=self._category_key)

        tag_handler.add(
            key=value,
            category=self._category_key,
        )

    def __delete__(self, instance):
        """
        Used when 'del' is called on the TagField.
        It is called with the component instance.
        """
        instance.host.tags.clear(category=self._category_key)

    def at_added(self, component):
        """
        Called when the parent component is added to a host.

        Args:
            component (Component): The component instance being added.
        """
        if self._default:
            self.__set__(component, self._default)

    def at_removed(self, component):
        """
        Called when the parent component is removed from a host.

        Args:
            component (Component): The component instance being removed.
        """
        self.__delete__(component)


class HostField(DBField):
    def __init__(self, default=None, autocreate=False, overridable=False, host_attribute=None, **kwargs):
        super().__init__(autocreate=autocreate, **kwargs)
        self.overridable = overridable
        self._fallback_default = default
        self.host_attribute = host_attribute

    def __set_name__(self, owner: 'Component', name):
        """
        Called when descriptor is first assigned to the class.

        Args:
            owner (object): The component class on which this is set
            name (str): The name that was used to set the DBField.
        """
        slot_name = owner.slot or owner.name
        self._key = f"{slot_name}::{name}"
        owner.add_field(name, self)
        if self.host_attribute is None:
            self.host_attribute = f"{slot_name}_{name}"

    def __get__(self, instance, owner):
        """
        Called when the attrkey is retrieved from the instance.

        """
        if self.overridable:
            override = super().__get__(instance, owner)
            if override is not None:
                return override

        value = getattr(instance.host, self.host_attribute, self._fallback_default)

        return value

    def __set__(self, instance, value):
        assert self.overridable, "Cannot set a non-overridable host field"
        return super().__set__(instance, value)


class KeyField(DBField):
    def __init__(self, listing: typing.Mapping, default=None, autocreate=False, **kwargs):
        if default is not None and not isinstance(default, str) and not isinstance(default, int):
            key = getattr(default, "key", None)
            if not key:
                raise ValueError("Only str, int, or instances with keys are supported")

            default = key

        super().__init__(default=default, autocreate=autocreate, **kwargs)
        self.listing = listing

    def __set_name__(self, owner: 'Component', name):
        """
        Called when descriptor is first assigned to the class.

        Args:
            owner (object): The component classF on which this is set
            name (str): The name that was used to set the DBField.
        """
        slot_name = owner.slot or owner.name
        self._key = f"{slot_name}::{name}_key"
        owner.add_field(name, self)

    def __get__(self, instance, owner):
        """
        Called when the attrkey is retrieved from the instance.

        """
        key = super().__get__(instance, owner)
        return self.listing.get(key)

    def __set__(self, instance, value):
        if not isinstance(value, str) and not isinstance(value, int):
            key = getattr(value, "key", None)
            if not key:
                raise ValueError("Only str, int, or instances with keys are supported")

            value = key

        return super().__set__(instance, value)
