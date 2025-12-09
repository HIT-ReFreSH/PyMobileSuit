import unittest
from ReFreSH.MobileSuit.Core.SuitContext import SuitContext
from ReFreSH.MobileSuit.RequestStatus import RequestStatus

class TestSuitContext(unittest.TestCase):

    def test_success_state(self):
        ctx = SuitContext()
        ctx.success("ok")
        self.assertEqual(ctx.status, RequestStatus.SUCCESS)
        self.assertEqual(ctx.message, "ok")

    def test_failure_state(self):
        ctx = SuitContext()
        ctx.fail("error")
        self.assertEqual(ctx.status, RequestStatus.FAIL)
        self.assertEqual(ctx.message, "error")

if __name__ == "__main__":
    unittest.main()
