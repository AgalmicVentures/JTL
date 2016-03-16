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

## Syntax
The basic syntax of a JTL transformation is a JSON dictionary with the same structure as the output, where all  values are strings are JTL expressions.

JTL expressions are of the form `<SELECTOR> [$ <FUNCTION> <ARG1>*]*`.

Selectors are `.` separated paths: for example, `a.b.c` would return `3` from `{"a": {"b": {"c": 3}}}`.

Functions (and operators) transform data extracted by selectors.

## Operators
JTL supports the following operators in [Polish notation](https://en.wikipedia.org/wiki/Polish_notation) with the same semantics as Python:

* Arithmetic: `+`, `-`, `*`, `/`, `**`, `%`
* Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`

For example:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.temp $ words $ first $ toFloat $ + 3.0 $ / 23"}'
    {
        "x": 3.0
    }

## Functions
JTL has a wide variety of built in transformations. In order to easily handle missing values, all functions will pass through null unless otherwise indicated (much like an option monad).

### Basic

#### `default <VALUE>`
Returns the input value or the first argument if the input is `null` (this is the one case with special `null` handling).

#### `defaultNan`
Returns the input value or `NaN` if the input is `null`.

#### `isNull`
Returns true if the value is `null`.

#### `toBool`
Converts the input value to a boolean.

#### `toFloat`
Converts the input value to a float, returning `null` if it is not a valid number.

#### `toInt`
Converts the input value to an integer, returning `null` if it is not a valid integer.

#### `toString`
Converts the input value to a string.

### Bool

#### `not`
Inverts the boolean value.

### Dictionary

#### `keys`
Returns the keys of the dictionary as a list.

#### `values`
Returns the values of the dictionary as a list.

### Hashing
JTL supports a variety of cryptographic hash functions: `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`. In addition, [HMAC's](https://en.wikipedia.org/wiki/Hash-based_message_authentication_code) are supported for each of these hash types (e.g. `hmac_md5`).

### Math

* Basics: `abs`, `ceil`, `floor`
* Exponentials: `exp`, `lg`, `ln`, `log`, `sqrt`
* Flags: `isFinite`, `isNan`
* Trigonometry: `sin`, `cos`, `tan`
* Hyperbolic trigonometry: `sinh`, `cosh`, `tanh`
* Advanced: `erf`

### Sequence

#### `count <ELEMENT>`
Returns the number of times the element appears in the list.

#### `first`
Returns the first element of the list, or `null` if the list is empty.

#### `init`
Returns all of the elements of the list except the last one.

#### `last`
Returns the last element of the list, or `null` if the list is empty.

#### `rest`
Returns the rest of the list after the first element.

#### `length`
Returns the length of the list.

#### `max`
Finds the maximum value in the list.

#### `min`
Finds the minimum value in the list.

#### `sorted`
Returns a sorted version of the list.

#### `sum`
Takes the sum of values in the list.

#### `unique`
Returns a copy of the list with duplicates removed.

### String

* Case transformation: `capitalize`, `lower`, `swapCase`, `upper`
* Search: `find`, `replace`, `startsWith`, `endsWith`
* Split / join: `join`, `split`, `lines`, `unlines`, `words`, `unwords`
* Whitespace: `lstrip`, `rstrip`, `strip`
