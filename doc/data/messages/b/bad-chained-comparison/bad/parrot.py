shop = {
    # animal: (specie, descriptions)
    "parrot": ("Norvegian blue", ("restin'", "remarkable", "beautiful plumage")),
}

if "parrot" in shop is "restin'":  # [bad-chained-comparison]
    print("Hellooooo, Pooolllllyyy ! WAAAAKEEY, WAKKEEEY !")
