import asyncio
from typing import List

from .Core.ISuitMiddleware import ISuitMiddleware, SuitRequestDelegate
from .Core.Services.SuitExceptionHandler import ISuitExceptionHandler
from .Core.Services.TaskService import TaskRecorder
from .Core.SuitContext import SuitContext
from .RequestStatus import RequestStatus
from ..DependencyInjection import ServiceProvider
from .Core.Services.AppInfo import ISuitAppInfo


class SuitHost:
    """A entity, which serves the shell functions of a mobile-suit program."""

    def __init__(self, services: ServiceProvider, middleware: List[ISuitMiddleware], cancellationTasks: TaskRecorder):
        self.Services = services
        self._suitApp = middleware
        self._cancellationTasks = cancellationTasks
        self._exceptionHandler = services.GetRequiredService(ISuitExceptionHandler)
        self._rootScope = services
        self._hostTask = None

    @staticmethod
    def CreateMiddlewareInvocation(m: ISuitMiddleware, nxt: SuitRequestDelegate) -> SuitRequestDelegate:
        async def invocation(context: SuitContext):
            await m.InvokeAsync(context, nxt)

        return invocation

    @staticmethod
    async def EmptyMiddlewareInvocation(c: SuitContext):
        pass

    async def Start(self):
        if self._hostTask is not None:
            return

        requestStack = [SuitHost.EmptyMiddlewareInvocation]
        for middleware in reversed(self._suitApp):
            nextStep = requestStack[-1]
            requestStack.append(SuitHost.CreateMiddlewareInvocation(middleware, nextStep))

        handleRequest = requestStack[-1]
        # TODO: startup arg support -- Done
        appInfo = self._rootScope.GetRequiredService(ISuitAppInfo)
        if appInfo.StartArgs:
            requestScope = self.Services.CreateScope()
            context = SuitContext(requestScope)
            context.RequestStatus = RequestStatus.NotHandled
            context.Request = appInfo.StartArgs
        #
            try:
                await handleRequest(context)
            except Exception as ex:
                context.Exception = ex
                context.RequestStatus = RequestStatus.Faulted
                await self._exceptionHandler.InvokeAsync(context)
            return 

        self._hostTask = asyncio.create_task(self.HandleRequest(handleRequest))

    def Stop(self):
        if self._hostTask is None:
            return
        self._hostTask.cancel()
        self._rootScope.Dispose()
        self._hostTask = None

    async def HandleRequest(self, requestHandler: SuitRequestDelegate):
        while True:
            requestScope = self.Services.CreateScope()
            context = SuitContext(requestScope)
            # TODO: cancel key
            # cancelKeyHandler = SuitHost.CreateCancelKeyHandler(context)

            try:
                await requestHandler(context)
            except Exception as ex:
                context.Exception = ex
                context.RequestStatus = RequestStatus.Faulted
                await self._exceptionHandler.InvokeAsync(context)
                continue

            if context.RequestStatus == RequestStatus.OnExit:
                break

    # TODO: cancel key
    # @staticmethod
    # def CreateCancelKeyHandler(context: SuitContext):
    #     def cancelKeyHandler(sender, e):
    #         e.Cancel = True
    #         context.CancellationToken.cancel()
    #
    #     return cancelKeyHandler

    def Dispose(self):
        self._rootScope.Dispose()

    async def RunAsync(self):
        await self.Start()
        if self._hostTask:
            await self._hostTask

    def Run(self):
        asyncio.run(self.RunAsync())
