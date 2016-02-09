# JTL
JSON Transformation Language, henceforth JTL, is like awk for JSON: a simple language for
transforming JSON values into other JSON values. The syntax of the language itself is also JSON
(so it can operate on itself!). Command line prototyping is easy:

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
JTL is for any time the data you have doesn't quite match the data you need. It's perfect for situations
like the transform layer of an ETL system.

It's designed to be simple to parse for both humans and computers. This makes the implementation simple,
and allows the creation of value-added tools like optimizers.

Because it's input and output are JSON, it's highly composable. In fact, sometimes that's the only
way to do things. Since the code is also JSON, it can even be used self-referentially, for example to
automate version updates.
