def file_deleted(bus, body):
    print(bus, body)


HANDLERS = {"metadata": [file_deleted]}
