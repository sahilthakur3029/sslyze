import unittest

import pickle

from sslyze.plugins.compression_plugin import CompressionPlugin, CompressionScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester
from tests.openssl_server import LegacyOpenSslServer, ClientAuthConfigEnum


class CompressionPluginTestCase(unittest.TestCase):

    def test_compression_disabled(self):
        server_test = ServerConnectivityTester(hostname='www.google.com')
        server_info = server_test.perform()

        plugin = CompressionPlugin()
        plugin_result = plugin.process_task(server_info, CompressionScanCommand())

        assert not plugin_result.compression_name

        assert plugin_result.as_text()
        assert plugin_result.as_xml()

        # Ensure the results are pickable so the ConcurrentScanner can receive them via a Queue
        assert pickle.dumps(plugin_result)

    @unittest.skip('Not implemented')
    def test_compression_enabled(self):
        # TODO
        pass

    @unittest.skipIf(not LegacyOpenSslServer.is_platform_supported(), 'Not on Linux 64')
    def test_succeeds_when_client_auth_failed(self):
        # Given a server that requires client authentication
        with LegacyOpenSslServer(client_auth_config=ClientAuthConfigEnum.REQUIRED) as server:
            # And the client does NOT provide a client certificate
            server_test = ServerConnectivityTester(
                hostname=server.hostname,
                ip_address=server.ip_address,
                port=server.port
            )
            server_info = server_test.perform()

            # The plugin works even when a client cert was not supplied
            plugin = CompressionPlugin()
            plugin_result = plugin.process_task(server_info, CompressionScanCommand())

        assert not plugin_result.compression_name
        assert plugin_result.as_text()
        assert plugin_result.as_xml()
