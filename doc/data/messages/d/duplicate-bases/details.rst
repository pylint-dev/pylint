.. code:: shell-session

    > python bad.py
    Traceback (most recent call last):
    File "C:\pylint\doc\data\messages\d\duplicate-bases\bad.py", line 5, in <module>
        class Cat(Animal, Animal):
    TypeError: duplicate base class Animal
