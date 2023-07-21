from .. import SuitBuildUtils
from ..ISuitMiddleware import ISuitMiddleware, SuitRequestDelegate
from ..Services.HistoryService import IHistoryService
from ..SuitContext import SuitContext
from ...RequestStatus import RequestStatus


class FinalizeMiddleware(ISuitMiddleware):
    """Middleware to finalize the command execution."""

    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate) -> None:
        """Inherited from base class."""
        if context.RequestStatus == RequestStatus.NotHandled:
            context.RequestStatus = RequestStatus.CommandNotFound
        history = context.ServiceProvider.GetRequiredService(IHistoryService)
        history.Response = context.Response
        history.Status = {
            RequestStatus.Handled: RequestStatus.Ok,
            RequestStatus.OnExit: RequestStatus.OnExit,
            RequestStatus.NotHandled: RequestStatus.CommandNotFound,
            RequestStatus.Running: RequestStatus.Running,
            
        }.get(context.RequestStatus,context.RequestStatus)
        if not (context.Properties.get(SuitBuildUtils.SuitCommandTarget) == SuitBuildUtils.SuitCommandTargetAppTask):
            context.Dispose()
        await nextStep(context)
