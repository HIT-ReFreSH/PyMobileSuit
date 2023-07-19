import re
from enum import Enum
from typing import List, Tuple

from ..ISuitMiddleware import SuitRequestDelegate, ISuitMiddleware
from ..SuitBuildUtils import SuitCommandTarget, SuitCommandTargetApp, SuitCommandTargetHost, SuitCommandTargetAppTask
from ..SuitContext import SuitContext
from ...IIOHub import IIOHub
from ...RequestStatus import RequestStatus


class UserInputMiddleware(ISuitMiddleware):
    """Middleware which provides user input"""

    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate):
        # if context.CancellationToken.is_cancellation_requested:
        #     context.Status = RequestStatus.Interrupt
        #     await next(context)

        if context.Status == RequestStatus.NoRequest:
            io = context.ServiceProvider.GetRequiredService(IIOHub)
            originInput = io.ReadLine()
            if originInput is None:
                context.Status = RequestStatus.OnExit
                return

            if originInput.startswith("#"):
                context.Status = RequestStatus.Ok
                return

            request, control = SplitCommandLine(originInput)
            i = 0
            while i < len(control):
                if control[i][0] == '>':
                    i += 1
                    if i < len(control):
                        io.Output = open(control[i], 'w')
                    else:
                        context.Status = RequestStatus.CommandParsingFailure
                elif control[i][0] == '<':
                    i += 1
                    if i < len(control):
                        io.Input = open(control[i], 'r')
                    else:
                        context.Status = RequestStatus.CommandParsingFailure
                elif control[i][0] == '!':
                    context.Properties[SuitCommandTarget] = SuitCommandTargetApp
                elif control[i][0] == '@':
                    context.Properties[SuitCommandTarget] = SuitCommandTargetHost
                elif control[i][0] == '&':
                    context.Properties[SuitCommandTarget] = SuitCommandTargetAppTask
                else:
                    context.Status = RequestStatus.CommandParsingFailure
                i += 1

            if len(request) == 0:
                context.Status = RequestStatus.Ok
                return

            context.Status = RequestStatus.NotHandled
            context.Request = request

        await nextStep(context)


class StackOp(Enum):
    None_ = 0
    Push1 = 1
    Push2 = 2
    Push1Then2 = 3
    Push3 = 4
    Pop = -1


class Operation:
    def __init__(self, addToControl=False, addToBuffer=False, spaceCommit=False, setQuote=False, stackOp=StackOp.None_):
        self.AddToControl = addToControl
        self.AddToBuffer = addToBuffer
        self.StackOp = stackOp
        self.SpaceCommit = spaceCommit
        self.SetQuote = setQuote


def SplitCommandLine(commandLine: str) -> Tuple[List[str], List[str]]:
    """Split a commandline string to args[] array."""

    """
    States:
        S0: WordStart
        S1: IORedirect
        S2: Word
        S3: QuotesWord
        S4: AfterBackslash
        S5: Comment

    Transitions:
        S0:
         &,!,@,<space>: S0
         <,>: S1
         #: S5
         ",': S3(S2)
         \: S4(S2)
         default: S2
        S1:
         <space>: S2(S1)
         ",': S3(S2,S1)
         \: S4(S2,S1)
         #: S5
         default: S2(S1)
        S2:
         <space>: pop
         ",': S3(S2)
         \: S4(S2)
         <,>: S1
         #: S5
         default: S2
        S3:
         ",': pop
         \: S4(S3)
         default: S3
        S4:
         default: pop, setbuf
        S5:
         default: S5
        S6: <POP-State>
    """

    if not commandLine:
        return [], []

    l = []
    ctl = []

    status = 0
    quote = "'"
    stk = []
    i = 0
    buf = []

    def commit():
        nonlocal status, i
        status = stk[-1] if stk else 0
        (ctl if status == 1 else l).append(re.sub(r'\\(.)', r'\1', ''.join(buf[:i])))
        status = 0
        i = 0

    def transitions(lastStatus: int, inputChar: str, currentQuote: str) -> Tuple[int, Operation]:
        if lastStatus == 0:
            if inputChar in '&!@':
                return 0, Operation(addToControl=True)
            elif inputChar == ' ':
                return 0, Operation()
            elif inputChar in '<>':
                return 1, Operation(addToControl=True)
            elif inputChar in '\'"':
                return 3, Operation(setQuote=True, stackOp=StackOp.Push2)
            elif inputChar == '\\':
                return 4, Operation(addToBuffer=True, stackOp=StackOp.Push2)
            elif inputChar == '#':
                return 5, Operation()
            else:
                return 2, Operation(addToBuffer=True)
        elif lastStatus == 1:
            if inputChar == ' ':
                return 2, Operation(stackOp=StackOp.Push1)
            elif inputChar in '\'"':
                return 3, Operation(setQuote=True, stackOp=StackOp.Push1Then2)
            elif inputChar == '\\':
                return 4, Operation(addToBuffer=True, stackOp=StackOp.Push1Then2)
            else:
                return 2, Operation(addToBuffer=True, stackOp=StackOp.Push1)
        elif lastStatus == 2:
            if inputChar in '\'"':
                return 3, Operation(setQuote=True, stackOp=StackOp.Push2)
            elif inputChar == '\\':
                return 4, Operation(addToBuffer=True, stackOp=StackOp.Push2)
            elif inputChar == ' ':
                return 0, Operation(spaceCommit=True)
            elif inputChar == '#':
                return 5, Operation(spaceCommit=True)
            else:
                return 2, Operation(addToBuffer=True)
        elif lastStatus == 3:
            if inputChar in '\'"' and inputChar == currentQuote:
                return 6, Operation(stackOp=StackOp.Pop)
            elif inputChar == '\\':
                return 4, Operation(addToBuffer=True, stackOp=StackOp.Push3)
            else:
                return 3, Operation(addToBuffer=True)
        elif lastStatus == 4:
            return 6, Operation(addToBuffer=True, stackOp=StackOp.Pop)

    for c in commandLine:
        newStatus, operation = transitions(status, c, quote)

        status = newStatus
        if operation.AddToControl:
            ctl.append(c)
        if operation.AddToBuffer:
            buf.append(c)
        if operation.StackOp is StackOp.Push1:
            stk.append(1)
        elif operation.StackOp is StackOp.Push2:
            stk.append(2)
        elif operation.StackOp is StackOp.Push1Then2:
            stk.extend([1, 2])
        elif operation.StackOp is StackOp.Push3:
            stk.append(3)
        elif operation.StackOp is StackOp.Pop:
            status = stk.pop()
        if operation.SpaceCommit:
            commit()
        if operation.SetQuote:
            quote = c

    if status == 2:
        commit()

    return l, ctl
