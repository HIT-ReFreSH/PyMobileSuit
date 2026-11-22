import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from ReFreSH.MobileSuit.Core.Services.TaskService import TaskRecorder, TaskService
from ReFreSH.MobileSuit.RequestStatus import RequestStatus


class TestTaskServiceGetTasks(unittest.TestCase):
    def setUp(self):
        self.service = TaskService(TaskRecorder())

    def add_task(self, request, response, status=RequestStatus.Running):
        context = SimpleNamespace(
            ServiceProvider=Mock(), Request=request, Response=response,
            RequestStatus=status,
        )
        self.service.AddTask(Mock(), context)
        return context

    def test_empty_collection(self):
        self.assertEqual(list(self.service.GetTasks()), [])

    def test_index_is_integer_and_can_be_used_for_lookup(self):
        self.add_task(["hello"], "world")
        info = next(self.service.GetTasks())
        self.assertIs(type(info.Index), int)
        self.assertTrue(self.service.HasTask(info.Index))

    def test_request_is_joined_string(self):
        self.add_task(["hello", "Alice"], "ok")
        info = next(self.service.GetTasks())
        self.assertEqual(info.Request, "hello Alice")
        self.assertIsInstance(info.Request, str)

    def test_response_preserves_string_and_none(self):
        for response in ("done", "", None):
            with self.subTest(response=response):
                self.service = TaskService(TaskRecorder())
                self.add_task([], response)
                info = next(self.service.GetTasks())
                self.assertEqual(info.Response, response)
                self.assertEqual(info.Request, "")

    def test_multiple_tasks_preserve_order_and_status(self):
        self.add_task(["first"], "one", RequestStatus.Running)
        self.add_task(["second"], "two", RequestStatus.Ok)
        infos = list(self.service.GetTasks())
        self.assertEqual([info.Index for info in infos], [0, 1])
        self.assertEqual([info.Request for info in infos], ["first", "second"])
        self.assertEqual([info.Status for info in infos],
                         [RequestStatus.Running, RequestStatus.Ok])


if __name__ == "__main__":
    unittest.main()
