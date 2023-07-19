from inspect import Parameter, signature, getmembers
from typing import Optional, Callable, Any, get_args, get_origin, List

from PlasticMetal.CSharp import null_collapse, linq_first_or_default, INT_MAX
from .Services.ParsingService import IParsingService
from .SuitContext import SuitContext
from .SuitMethodParameterInfo import SuitMethodParameterInfo, TailParameterType
from ..Decorators.DecoratorUtils import get_parser, get_injected
from ..Decorators.SuitArgParser import SuitArgParserInfo

SuitCommandTarget = "suit-cmd-target"
SuitCommandTargetApp = "app"
SuitCommandTargetHost = "suit"
SuitCommandTargetAppTask = "app-task"

InstanceFactory = Callable[[SuitContext], Any]


def CreateConverterFactory(T, parserInfo: SuitArgParserInfo) -> Callable[
    [SuitContext], Callable[[str], Optional[object]]]:
    def converter(context: SuitContext):
        myT = T
        if parserInfo.Converter is not None:
            return parserInfo
        if issubclass(get_origin(myT), List):
            myT = get_args(myT)[0]

        if issubclass(myT, str):
            return lambda s: s
        return context.GetRequiredService(IParsingService).Get(myT, null_collapse(parserInfo.Name, ''))

    return converter


def GetArg(parameter: Parameter, function: Callable, arg: Optional[str], context: SuitContext) -> tuple[object, int]:
    if arg is None:
        step = 0
        if parameter.annotation == Parameter.empty and parameter.default == Parameter.empty:
            raise ValueError
        if issubclass(parameter.annotation, SuitContext):
            return context, step

        service = context.GetService(parameter.annotation)
        return parameter.default if service is None else service

    step = 1
    return CreateConverterFactory(parameter.annotation, get_parser(function, parameter.name))(context)(arg), step


def GetArrayArg(parameter: Parameter, function: Callable, argArray: list[str], context: SuitContext) -> object:
    type = get_args(parameter.annotation)[0]
    array = list[type]()
    convert = CreateConverterFactory(
        type, get_parser(function, parameter.name))(context)
    for arg in argArray:
        array.append(convert(arg))
    return array


def __GetParametersFromFunc(func: Callable) -> List[Parameter]:
    sig = signature(func)
    parameters = [param for (_, param) in filter(lambda x: x[0] != 'self', sig.parameters.items())]
    return parameters


def GetMethodParameterInfo(func: Callable) -> SuitMethodParameterInfo:
    parameters = __GetParametersFromFunc(func)
    suitMethodParameterInfo = SuitMethodParameterInfo(TailParameterType.Normal, 0, 0, 0)
    originCount = len(parameters)
    parameters = [p for p in parameters if not get_injected(func, p.name)]
    if originCount == 0:
        suitMethodParameterInfo.TailParameterType = TailParameterType.NoParameter
    else:
        if len(parameters) == 0:
            suitMethodParameterInfo.TailParameterType = TailParameterType.Normal
        if issubclass(get_origin(parameters[-1].annotation), List):
            suitMethodParameterInfo.TailParameterType = TailParameterType.Array
        # TODO: DynamicParameter support
        # elif parameters[-1].ParameterType.GetInterface("IDynamicParameter") is not None:
        #     suitMethodParameterInfo.TailParameterType = TailParameterType.DynamicParameter
        else:
            suitMethodParameterInfo.TailParameterType = TailParameterType.Normal

        suitMethodParameterInfo.MaxParameterCount = len(
            parameters) if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else INT_MAX
        suitMethodParameterInfo.NonArrayParameterCount = len(
            parameters) if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else len(
            parameters) - 1
        i = suitMethodParameterInfo.NonArrayParameterCount - 1
        while i >= 0 and parameters[i].default != Parameter.empty:
            i -= 1

        suitMethodParameterInfo.MinParameterCount = i + 1
        suitMethodParameterInfo.NonArrayParameterCount = originCount if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else originCount - 1

    return suitMethodParameterInfo


def CreateInstance(otype, s: SuitContext) -> Optional[Any]:
    if otype in s.ServiceProvider:
        return s.GetService(otype)
    constructor = linq_first_or_default(getmembers(otype), lambda x: x[0] == '__init__')
    args = GetArgs(constructor, [], s)

    return type(*args)


def __GetArgsInternal(func: Callable, parameterInfo: SuitMethodParameterInfo,
                      args: List[str], context: SuitContext) -> Optional[List[Optional[Any]]]:
    parameters = __GetParametersFromFunc(func)
    pass_: List[Any] = [None] * len(parameters)
    i = 0
    j = 0
    try:
        for i in range(parameterInfo.NonArrayParameterCount):
            if j < len(args):
                pass_[i], step = GetArg(parameters[i], func, args[j], context)
                j += step
            else:
                pass_[i], _ = GetArg(parameters[i], func, None, context)

        if parameterInfo.TailParameterType == TailParameterType.Normal:
            return pass_
        # TODO: DynamicParameter support
        # if parameterInfo.TailParameterType == TailParameterType.DynamicParameter:
        #     dynamicParameter = parameters[-1].ParameterType.Assembly.CreateInstance(
        #         parameters[-1].ParameterType.FullName or parameters[-1].ParameterType.Name)
        #     if not dynamicParameter.Parse(args[i:] if i < len(args) else [], context):
        #         return None
        #     pass_[i] = dynamicParameter
        #     return pass_

        if i < len(args):
            pass_[i], step = GetArrayArg(parameters[-1], func, args[i:], context)
            i += step
        else:
            pass_[i] = []

        return pass_
    except ValueError:
        return None


def GetArgs(func: Callable, args: List[str], context: SuitContext) -> Optional[List[Optional[Any]]]:
    return __GetArgsInternal(func, GetMethodParameterInfo(func), args, context)
