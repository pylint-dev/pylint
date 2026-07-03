Having too many public methods is an indication that you might not be respecting
the Single-responsibility principle (S of SOLID).

The class should have only one reason to change, but in the example the
spaceship has at least 4 persons that could ask for change to it
(laser manager, shield manager, missile manager, teleportation officer...).
