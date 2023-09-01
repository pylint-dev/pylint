def wizard_spells(spell_book):
    # pylint: disable=maybe-no-member # [locally-disabled]
    for spell in spell_book:
        print(f"Abracadabra! {spell}.")


spell_list = ["Levitation", "Invisibility", "Fireball", "Teleportation"]
wizard_spells(spell_list)
