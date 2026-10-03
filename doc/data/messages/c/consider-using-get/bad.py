knights = {"Gallahad": "the pure", "Robin": "the brave"}

if "Gallahad" in knights:  # [consider-using-get]
    DESCRIPTION = knights["Gallahad"]
else:
    DESCRIPTION = ""
