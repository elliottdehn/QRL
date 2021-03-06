# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from pyqrllib.pyqrllib import str2bin
from qrl.core import logger, config
from qrl.core.messagereceipt import MessageReceipt

logger.initialize_default(force_console_output=True)


class TestMessageReceipt(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMessageReceipt, self).__init__(*args, **kwargs)

    def test_create(self):
        mr = MessageReceipt()
        self.assertIsNotNone(mr)
        self.assertEqual(mr.allowed_types, ['TX', 'ST', 'BK', 'DT'])

    def test_register(self):
        mr = MessageReceipt()

        msg_hash = str2bin("asdf")
        msg_obj = [1, 2, 3, 4]
        msg_type = mr.allowed_types[0]

        mr.register(msg_hash, msg_obj, msg_type)

    def test_add_contains_remove(self):
        mr = MessageReceipt()
        # FIXME: Hashes being are treated as strings

        msg_hash = str2bin("hash_valid")
        msg_obj = [1, 2, 3, 4]
        msg_type = mr.allowed_types[0]
        peer = '127.0.0.1'

        mr.register(msg_hash, msg_obj, msg_type)
        mr.add_peer(msg_hash, msg_type, peer)

        self.assertTrue(mr.contains(msg_hash, msg_type))
        self.assertFalse(mr.contains('hash_invalid', msg_type))

    def test_contains(self):
        mr = MessageReceipt()

        msg_hash = str2bin("hash_valid")
        msg_obj = [1, 2, 3, 4]
        msg_type = mr.allowed_types[0]

        mr.register(msg_hash, msg_obj, msg_type)
        self.assertTrue(mr.contains(msg_hash, msg_type))

    def test_register_overflow(self):
        mr = MessageReceipt()

        msg_obj = [1, 2, 3, 4]
        msg_type = mr.allowed_types[0]

        config.dev.message_q_size = 4

        for i in range(config.dev.message_q_size * 2):
            msg_hash = str2bin(str(i))
            mr.register(msg_hash, msg_obj, msg_type)

        self.assertEqual(len(mr.hash_msg), config.dev.message_q_size)
