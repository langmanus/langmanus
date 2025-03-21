from langchain_community.chat_models import ChatLiteLLM

from operator import itemgetter
from typing import (
    Any,
    Dict,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from langchain_core.language_models import LanguageModelInput


from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.output_parsers.openai_tools import (
    JsonOutputKeyToolsParser,
    PydanticToolsParser,
)
from langchain_core.runnables import (
    Runnable,
    RunnableMap,
    RunnablePassthrough,
)
from langchain_core.utils.function_calling import (
    convert_to_openai_tool,
)
from langchain_core.utils.pydantic import (
    is_basemodel_subclass,
)
from pydantic import BaseModel

_BM = TypeVar("_BM", bound=BaseModel)
_DictOrPydanticClass = Union[Dict[str, Any], Type[_BM], Type]
_DictOrPydantic = Union[Dict, _BM]


def _is_pydantic_class(obj: Any) -> bool:
    return isinstance(obj, type) and is_basemodel_subclass(obj)


class ChatLiteLLMV2(ChatLiteLLM):
    def with_structured_output(
        self,
        schema: Optional[_DictOrPydanticClass] = None,
        *,
        method: Literal["function_calling", "json_mode"] = "function_calling",
        include_raw: bool = False,
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, _DictOrPydantic]:
        if kwargs:
            raise ValueError(f"Received unsupported arguments {kwargs}")
        if strict is not None and method == "json_mode":
            raise ValueError(
                "Argument `strict` is not supported with `method`='json_mode'"
            )
        is_pydantic_schema = _is_pydantic_class(schema)

        if method == "function_calling":
            if schema is None:
                raise ValueError(
                    "schema must be specified when method is not 'json_mode'. "
                    "Received None."
                )
            tool_name = convert_to_openai_tool(schema)["function"]["name"]
            bind_kwargs = self._filter_disabled_params(
                tool_choice='auto',
                parallel_tool_calls=False,
                strict=strict,
                ls_structured_output_format={
                    "kwargs": {"method": method},
                    "schema": schema,
                },
            )
            print(f"bind_kwargs: {bind_kwargs}")
            llm = self.bind_tools([schema], **bind_kwargs)
            if is_pydantic_schema:
                output_parser: Runnable = PydanticToolsParser(
                    tools=[schema],  # type: ignore[list-item]
                    first_tool_only=True,  # type: ignore[list-item]
                )
            else:
                output_parser = JsonOutputKeyToolsParser(
                    key_name=tool_name, first_tool_only=True
                )
        elif method == "json_mode":
            llm = self.bind(
                response_format={"type": "json_object"},
                ls_structured_output_format={
                    "kwargs": {"method": method},
                    "schema": schema,
                },
            )
            output_parser = (
                PydanticOutputParser(pydantic_object=schema)  # type: ignore[arg-type]
                if is_pydantic_schema
                else JsonOutputParser()
            )
        else:
            raise ValueError(
                f"Unrecognized method argument. Expected one of 'function_calling' or "
                f"'json_mode'. Received: '{method}'"
            )

        if include_raw:
            parser_assign = RunnablePassthrough.assign(
                parsed=itemgetter("raw") | output_parser, parsing_error=lambda _: None
            )
            parser_none = RunnablePassthrough.assign(parsed=lambda _: None)
            parser_with_fallback = parser_assign.with_fallbacks(
                [parser_none], exception_key="parsing_error"
            )
            return RunnableMap(raw=llm) | parser_with_fallback
        else:
            return llm | output_parser

    def _filter_disabled_params(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Filter parameters that are not supported by the underlying model.

        Args:
            **kwargs: Parameters to be filtered.

        Returns:
            Dict[str, Any]: Dictionary containing only the supported parameters.
        """
        # Get the parameters supported by the underlying model
        supported_params = self.llm_kwargs()

        # Filter parameters, keeping only the supported ones
        filtered_kwargs = {}

        for key, value in kwargs.items():
            # Check if the underlying model supports this parameter
            if key in supported_params or key.startswith("ls_"):
                filtered_kwargs[key] = value

        return filtered_kwargs

    def llm_kwargs(self) -> Dict[str, Any]:
        """
        Returns a dictionary with the parameters supported by the underlying LLM model.

        Returns:
            Dict[str, Any]: Dictionary containing the parameters supported by the model.
        """
        # Common parameters supported by Groq models
        supported_params = {
            "model",
            "temperature",
            "top_p",
            "n",
            "stream",
            "stop",
            "max_tokens",
            "user",
            "tool_choice",
            "tools",
            "tool-use",
            "response_format",
        }
        return supported_params
