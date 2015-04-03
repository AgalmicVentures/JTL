# JTL

JSON Transformation Language, henceforth JTL, is a simple language for transforming JSON values
into other JSON values. The syntax of the language itself is also JSON:

    in = {"a": "3.25", "b": 4134}
    transform = {
        "parsed": "a $ parseDouble",
        "digits": "b $ show $ length"
    }

    out = jtl.transform(in, transform)

    out == {
        "parsed": 3.25,
        "digits": 4
    }
