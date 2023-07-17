from inspect import Parameter, signature, getmembers
from typing import Optional, Callable, Iterable, Any, get_args, get_origin

from PyMobileSuit.CSharp import null_collapsed, linq_first_or_default, INT_MAX

from PyMobileSuit.Core.SuitContext import SuitContext
from PyMobileSuit.Core.SuitMethodParameterInfo import SuitMethodParameterInfo, TailParameterType

from PyMobileSuit.Core.Services.ParsingService import IParsingService

from PyMobileSuit.Decorators.SuitArgParser import SuitArgParserInfo
from PyMobileSuit.Decorators.DecoratorUtils import get_parser, get_injected

SuitCommandTarget = "suit-cmd-target"
SuitCommandTargetApp = "app"
SuitCommandTargetHost = "suit"
SuitCommandTargetAppTask = "app-task"


def CreateConverterFactory(T, parserInfo: SuitArgParserInfo) -> Callable[[SuitContext], Callable[[str], Optional[object]]]:
    def converter(context: SuitContext):

        if parserInfo.Converter is not None:
            return parserInfo
        if issubclass(get_origin(T), List):
            T = get_args(T)[0]

        if issubclass(T, str):
            return lambda s: s
        return context.GetRequiredService(IParsingService).Get(T, null_collapse(parserInfo.Name, ''))
    return converter


def GetArg(parameter: Parameter, function: Callable, arg: Optional[str],  context: SuitContext) -> tuple[object, int]:

    if arg is None:
        step = 0
        if parameter.annotation == Parameter.empty and parameter.default == Parameter.empty:
            raise ValueError
        if issubclass(parameter.annotation, SuitContext):
            return context

        service = context.TryGetRequiredService(parameter.annotation)
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


def __GetParametersFromFunc(func: Callable) -> Iterable[Parameter]:
    sig = signature(func)
    parameters = sig.parameters
    if 'self' in parameters:
        del parameters['self']
    return parameters.values()


def GetMethodParameterInfo(func: Callable) -> SuitMethodParameterInfo:
    parameters = __GetParametersFromFunc(func)
    suitMethodParameterInfo = SuitMethodParameterInfo()
    originCount = len(parameters)
    parameters = [p for p in parameters if not get_injected(func, p.name)]
    if originCount == 0:
        suitMethodParameterInfo.TailParameterType = TailParameterType.NoParameter
    else:
        if len(parameters) == 0:
            suitMethodParameterInfo.TailParameterType = TailParameterType.Normal
        elif parameters[-1].ParameterType.IsArray:
            suitMethodParameterInfo.TailParameterType = TailParameterType.Array
        # TODO: DynamicParameter support
        # elif parameters[-1].ParameterType.GetInterface("IDynamicParameter") is not None:
        #     suitMethodParameterInfo.TailParameterType = TailParameterType.DynamicParameter
        else:
            suitMethodParameterInfo.TailParameterType = TailParameterType.Normal

        suitMethodParameterInfo.MaxParameterCount = parameters.Count if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else INT_MAX
        suitMethodParameterInfo.NonArrayParameterCount = parameters.Count if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else parameters.Count - 1
        i = suitMethodParameterInfo.NonArrayParameterCount - 1
        while i >= 0 and parameters[i].default != Parameter.empty:
            i -= 1

        suitMethodParameterInfo.MinParameterCount = i + 1
        suitMethodParameterInfo.NonArrayParameterCount = originCount if suitMethodParameterInfo.TailParameterType == TailParameterType.Normal else originCount - 1

    return suitMethodParameterInfo


def CreateInstance(type: Type, s: SuitContext) -> Optional[Any]:
    if type in s.ServiceProvider:
        return s.GetService(type)
    constructor = linq_first_or_default(
        getmembers(type), lambda x: x[0] == '__init__')
    args = GetArgs(constructor, [], s)

    return type(*args)


def __GetArgsInternal(func: Callable, parameterInfo: SuitMethodParameterInfo,
                      args: List[str], context: SuitContext) -> Optional[List[Optional[Any]]]:
    parameters = __GetParametersFromFunc(func)
    pass_ = [None] * len(parameters)
    i = 0
    j = 0
    try:
        for i in range(parameterInfo.NonArrayParameterCount):
            if j < len(args):
                pass_[i], step = GetArg(parameters[i], args[j], context)
                j += step
            else:
                pass_[i], _ = GetArg(parameters[i], None, context)

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
            pass_[i] = GetArrayArg(parameters[-1], args[i:], context)
        else:
            pass_[i] = []

        return pass_
    except ValueError:
        return None


def GetArgs(func: Callable, args: List[str], context: SuitContext) -> Optional[List[Optional[Any]]]:
    return __GetArgsInternal(parameters, GetMethodParametersInfo(parameters), args, context)
