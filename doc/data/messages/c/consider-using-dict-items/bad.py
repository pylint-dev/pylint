ORCHESTRA = {
    "violin": "strings",
    "oboe": "woodwind",
    "tuba": "brass",
    "gong": "percussion",
}


for instrument in ORCHESTRA:  # [consider-using-dict-items]
    print(f"{instrument}: {ORCHESTRA[instrument]}")
