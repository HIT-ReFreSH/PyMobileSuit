from typing import List

from ..ISuitMiddleware import ISuitMiddleware, SuitRequestDelegate
from ..Services.AppInfo import ISuitAppInfo
from ..Services.HistoryService import IHistoryService
from ..Services.TaskService import ITaskService
from ..SuitContext import SuitContext
from ...IIOHub import IIOHub
from ...OutputType import OutputType
from ...RequestStatus import RequestStatus
from ...Resources import Lang


class PromptMiddleware(ISuitMiddleware):
    """Middleware which provides the prompt output before user input."""

    def __init__(self):
        self.Lang = Lang

    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate) -> None:
        """Inherited from base class."""

        # TODO: CancellationToken
        # if context.CancellationToken.IsCancellationRequested:
        #     context.RequestStatus = RequestStatus.Interrupt
        #     await next(context)

        if context.RequestStatus == RequestStatus.NoRequest:
            io = context.ServiceProvider.GetRequiredService(IIOHub)
            tasks = context.ServiceProvider.GetRequiredService(ITaskService)
            history = context.ServiceProvider.GetRequiredService(IHistoryService)
            info = context.ServiceProvider.GetRequiredService(ISuitAppInfo)
            prompt: List = []
            if tasks.RunningCount > 0:
                prompt.append((f"{self.Lang.Tasks}{tasks.RunningCount}", io.ColorSetting.SystemColor))
            if info.AppName:
                prompt.append((info.AppName, io.ColorSetting.PromptColor))
            if history.Response is not None:
                prompt.append((history.Response, io.ColorSetting.InformationColor))
            prompt.append({
                              RequestStatus.Ok: (self.Lang.AllOK, io.ColorSetting.OkColor),
                              RequestStatus.NoRequest: (self.Lang.AllOK, io.ColorSetting.OkColor),
                              RequestStatus.Running: (self.Lang.Running, io.ColorSetting.WarningColor),
                              RequestStatus.CommandParsingFailure: (self.Lang.InvalidCommand, io.ColorSetting.ErrorColor),
                              RequestStatus.CommandNotFound: (self.Lang.MemberNotFound, io.ColorSetting.ErrorColor),
                              RequestStatus.Interrupt: (self.Lang.Interrupt, io.ColorSetting.ErrorColor),
                          }.get(history.Status, (self.Lang.OnError, io.ColorSetting.ErrorColor)))
            io.Write(prompt, OutputType.Prompt)

        await nextStep(context)
