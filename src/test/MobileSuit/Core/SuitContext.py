import unittest
from unittest.mock import MagicMock, create_autospec

from ReFreSH.MobileSuit.Core.SuitContext import SuitContext
from ReFreSH.DependencyInjection import ServiceProvider
from ReFreSH.MobileSuit.RequestStatus import RequestStatus

class TestSuitContext(unittest.TestCase):

    def setUp(self):
        self.mock_service_provider = create_autospec(ServiceProvider)
        self.context = SuitContext(self.mock_service_provider)

    def test_initialization(self):
        self.assertIsInstance(self.context.Properties, dict)
        self.assertEqual(self.context.RequestStatus, RequestStatus.NoRequest)
        self.assertIsNone(self.context.Exception)
        self.assertEqual(self.context.Request, [])
        self.assertEqual(self.context.ServiceProvider, self.mock_service_provider)
        self.assertIsNone(self.context.Response)

    def test_get_required_service(self):
        # Arrange
        service_type = str  # Example service type
        service_instance = "RequiredServiceInstance"
        self.mock_service_provider.GetRequiredService.return_value = service_instance

        # Act
        result = self.context.GetRequiredService(service_type)

        # Assert
        self.mock_service_provider.GetRequiredService.assert_called_once_with(service_type)
        self.assertEqual(result, service_instance)

    def test_get_service(self):
        # Arrange
        service_type = str  # Example service type
        service_instance = "OptionalServiceInstance"
        self.mock_service_provider.GetService.return_value = service_instance

        # Act
        result = self.context.GetService(service_type)

        # Assert
        self.mock_service_provider.GetService.assert_called_once_with(service_type)
        self.assertEqual(result, service_instance)

    def test_get_service_none(self):
        # Arrange
        service_type = str  # Example service type
        self.mock_service_provider.GetService.return_value = None

        # Act
        result = self.context.GetService(service_type)

        # Assert
        self.mock_service_provider.GetService.assert_called_once_with(service_type)
        self.assertIsNone(result)

    def test_dispose(self):
        # Act
        self.context.Dispose()

        # Assert
        self.mock_service_provider.Dispose.assert_called_once()


if __name__ == '__main__':
    unittest.main()
