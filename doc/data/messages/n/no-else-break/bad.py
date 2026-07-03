def next_seven_elements(iterator):
    for i, item in enumerate(iterator):
        if i == 7:  # [no-else-break]
            break
        else:
            yield item
