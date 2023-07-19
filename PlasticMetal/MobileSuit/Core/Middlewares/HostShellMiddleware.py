from ..ISuitMiddleware import SuitRequestDelegate, ISuitMiddleware
from ..Services.SuitHostShell import SuitHostShell
from ..Services.TaskService import ITaskService
from ..SuitBuildUtils import SuitCommandTarget, SuitCommandTargetHost, SuitCommandTargetApp, SuitCommandTargetAppTask
from ..SuitContext import SuitContext
from ...RequestStatus import RequestStatus


class HostShellMiddleware(ISuitMiddleware):
    """Middleware to execute command over suit server shell."""

    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate) -> None:
        """Inherited from base class."""

        # TODO: CancellationToken
        # if context.CancellationToken.IsCancellationRequested:
        #     context.Status = RequestStatus.Interrupt
        #     await next(context)

        if context.Status != RequestStatus.NotHandled:
            await nextStep(context)
            return

        tasks = context.ServiceProvider.GetRequiredService(ITaskService)
        force = context.Properties.get(SuitCommandTarget) == SuitCommandTargetHost
        forceClient = context.Properties.get(SuitCommandTarget) in (SuitCommandTargetApp, SuitCommandTargetAppTask)
        if forceClient:
            await nextStep(context)
            return

        server = context.ServiceProvider.GetRequiredService(SuitHostShell)
        await tasks.RunTaskImmediately(server.Execute(context))
        if force and context.Status == RequestStatus.NotHandled:
            context.Status = RequestStatus.CommandNotFound
        await nextStep(context)
