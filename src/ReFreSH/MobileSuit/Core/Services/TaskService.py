from abc import ABC
from asyncio import Task
from collections.abc import Iterable as IterableABC
from typing import List, Tuple, Iterable, Optional


from ..SuitContext import SuitContext
from ...IIOHub import IIOHub
from ...RequestStatus import RequestStatus


class TaskInfo:
    """Information of Suit Task"""

    def __init__(self):
        self.Index: int = 0
        self.Status: RequestStatus = RequestStatus.NotHandled
        self.Response: Optional[str] = None
        self.Request: str = ""


class ITaskService(ABC):
    """Provides task system."""

    @property
    def RunningCount(self) -> int:
        """Number of Tasks that are running."""
        raise NotImplementedError

    def HasTask(self, index: int) -> bool:
        """Has a task with given index"""
        raise NotImplementedError

    def AddTask(self, task: Task, context: SuitContext) -> None:
        """Add a task to Task Collection"""
        raise NotImplementedError

    def GetTasks(self) -> Iterable[TaskInfo]:
        """Get All tasks in Collection."""
        raise NotImplementedError

    async def RunTaskImmediately(self, task: Task) -> None:
        """Run some task immediately"""
        raise NotImplementedError

    def Stop(self, index: int) -> None:
        """Stop the task with certain index."""
        raise NotImplementedError

    async def Join(self, index: int, newContext: SuitContext) -> None:
        """Join the task with certain index."""
        raise NotImplementedError

    def ClearCompleted(self) -> None:
        """Remove the completed tasks."""
        raise NotImplementedError


class TaskRecorder(IterableABC):
    def __init__(self):
        self.IsLocked: bool = False
        self._tasks: List[Task] = []

    def __iter__(self):
        return iter(self._tasks)

    def Add(self, task: Task) -> bool:
        if not self.IsLocked:
            self._tasks.append(task)
        return not self.IsLocked

    def Remove(self, task: Task) -> bool:
        if not self.IsLocked:
            self._tasks.remove(task)
        return not self.IsLocked


class TaskService(ITaskService):
    def __init__(self, cancelTasks: TaskRecorder):
        self._cancelTasks = cancelTasks
        self._tasks: List[Tuple[Task, SuitContext]] = []

    def HasTask(self, index: int) -> bool:
        return 0 <= index < len(self._tasks)

    @property
    def RunningCount(self) -> int:
        return sum(1 for _, context in self._tasks if context.RequestStatus == RequestStatus.Running)

    def AddTask(self, task: Task, context: SuitContext) -> None:
        io = context.ServiceProvider.GetRequiredService(IIOHub)
        io.AppendWriteLinePrefix((str(len(self._tasks)), io.ColorSetting.SystemColor, None))
        self._tasks.append((task, context))
        self._cancelTasks.Add(task)

    def GetTasks(self) -> Iterable[TaskInfo]:
        for i, (_, context) in enumerate(self._tasks):
            ti = TaskInfo()
            ti.Index = i,
            ti.Request = " ".join(context.Request),
            ti.Response = context.Response,
            ti.Status = context.RequestStatus

            yield ti

    async def RunTaskImmediately(self, task: Task) -> None:
        self._cancelTasks.Add(task)
        await task
        self._cancelTasks.Remove(task)

    def Stop(self, index: int) -> None:
        task, context = self._tasks[index]
        task.cancel("Manually stopped")

    async def Join(self, index: int, newContext: SuitContext) -> None:
        task, context = self._tasks[index]
        self._cancelTasks.Remove(task)
        await task
        newContext.RequestStatus = context.RequestStatus
        newContext.Response = context.Response

    def ClearCompleted(self) -> None:
        for i in range(len(self._tasks) - 1, -1, -1):
            if self._tasks[i][1].RequestStatus == RequestStatus.Running:
                continue
            task, context = self._tasks[i]
            context.Dispose()
            del self._tasks[i]
