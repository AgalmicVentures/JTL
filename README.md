# JTL
JSON Transformation Language, JTL, is like `sed` and `awk` for JSON: a simple language for
transforming JSON values into other JSON values. The syntax of the language itself is also JSON
(so it can operate on itself - meta!). Command line prototyping is easy:

    > cat tests/faa1.json
    {
        ...
        "weather": {
            ...,
            "temp": "66.0 F (18.9 C)",
            ...
        }
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp"}'
    {
        "tempF": "66.0 F (18.9 C)"
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words"}'
    {
        "tempF": [
            "66.0",
            "F",
            "(18.9",
            "C)"
        ]
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words $ first"}'
    {
        "tempF": "66.0"
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words $ first $ toFloat"}'
    {
        "tempF": 66.0
    }

## Motivation
Although JSON has replaced XML as the de facto data format for structured text data, no standard suite of
supporting technologies has emerged. JTL is to JSON what XSL is to XML -- a transformation language written
in the underlying format. It allows the quick creation of format converters, adapters for 3rd party API's,
transform scripts for ETL's, and more.

JTL is designed to be simple to parse for both humans and computers. This makes the implementation simple,
and allows the creation of value-added features like query optimizers.

Because it's input and output are JSON, it's highly composable. In fact, sometimes composition is the only
way to do things. Since the code is also JSON, it can even be used self-referentially, for example to
automate refactoring.
