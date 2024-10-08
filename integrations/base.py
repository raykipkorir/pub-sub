from abc import ABC, abstractmethod


class MessageBrokerInterface(ABC):
    """Message broker interface."""

    @abstractmethod
    def _connect(self, *args, **kwargs):
        """Connect to a broker instance."""
        pass

    @abstractmethod
    def subscribe(self, channel_name, *args, **kwargs):
        """Subscribe to a channel."""
        pass

    @abstractmethod
    def publish(self, channel_name, json_data, *args, **kwargs):
        """Publish to a channel."""
        pass
