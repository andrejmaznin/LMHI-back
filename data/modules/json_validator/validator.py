def validate_payload(payload, schema):
    if type(payload) is None:
        assert schema == 'None'

    if type(payload) == int:
        assert schema == 'int'

    if type(payload) == str:
        assert schema == 'str'

    if type(payload) == dict:
        if not schema.keys():
            pass
        else:
            assert payload.keys() == schema.keys()
            for key in payload.keys():
                validate_payload(payload[key], schema[key])

    if type(payload) == list:
        for elem in payload:
            validate_payload(elem, schema[0])
