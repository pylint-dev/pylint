# pylint: disable=missing-docstring

data = {
    'abc': None,
}
data['abc'] = lambda: print("Callback called")
data['abc']()  # [not-callable] known false-positive
