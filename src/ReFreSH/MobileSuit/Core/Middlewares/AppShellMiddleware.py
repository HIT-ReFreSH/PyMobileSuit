from .. import SuitBuildUtils
from ..ISuitMiddleware import ISuitMiddleware, SuitRequestDelegate
from ..Services.SuitAppShell import SuitAppShell
from ..Services.TaskService import ITaskService
from ..SuitContext import SuitContext
from ...RequestStatus import RequestStatus


class AppShellMiddleware(ISuitMiddleware):
    """Middleware to execute command over suit server shell."""

    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate) -> None:
        """Inherited from base class."""
        # if context.CancellationToken.IsCancellationRequested:
        #     context.RequestStatus = RequestStatus.Interrupt
        #     await nextStep(context)

        if context.RequestStatus != RequestStatus.NotHandled:
            await nextStep(context)
            return

        tasks = context.ServiceProvider.GetRequiredService(ITaskService)
        client = context.ServiceProvider.GetRequiredService(SuitAppShell)
        asTask = context.Properties.get(SuitBuildUtils.SuitCommandTarget) == SuitBuildUtils.SuitCommandTargetAppTask
        forceClient = context.Properties.get(SuitBuildUtils.SuitCommandTarget) == SuitBuildUtils.SuitCommandTargetApp
        if asTask:
            context.RequestStatus = RequestStatus.Running
            tasks.AddTask(client.Execute(context), context)
        else:
            await tasks.RunTaskImmediately(client.Execute(context))
            if forceClient and context.RequestStatus == RequestStatus.NotHandled:
                context.RequestStatus = RequestStatus.CommandNotFound

        await nextStep(context)
