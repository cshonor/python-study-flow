"""
对应笔记：05-共享传参与可变默认参数.md

Run:
  python part-1-data-structures/chapter-06/05_call_by_sharing_mutable_defaults_demo.py

脚本说明：
- 教学演示：原地修改 vs 形参重绑定、`+=`、可变默认参数、HauntedBus/TwilightBus、dataclass `default_factory`；请与笔记对照。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ch06_demo_support import safe, section


def demo_parameter_mutate_vs_rebind() -> None:
    section("14) Call by sharing: mutate shared list vs rebind parameter")

    def append99(x: list[int]) -> None:
        x.append(99)

    def clear_by_rebind(x: list[int]) -> None:
        x = []

    a = [1, 2]
    append99(a)
    print("after append99(a):", a)

    b = [1, 2]
    clear_by_rebind(b)
    print("after clear_by_rebind(b):", b)


def f_iadd(a: object, b: object) -> object:
    a += b  # type: ignore[operator]
    return a


def demo_call_by_sharing_iadd() -> None:
    section("16) Call by sharing: `+=` differs for int/list/tuple")

    x = 1
    y = 2
    r1 = f_iadd(x, y)
    print("int -> f_iadd(x,y):", r1, "| x,y:", x, y)

    a = [1, 2]
    b = [3, 4]
    r2 = f_iadd(a, b)
    print("list -> f_iadd(a,b):", r2, "| a,b:", a, b)

    t = (10, 20)
    u = (30, 40)
    r3 = f_iadd(t, u)
    print("tuple -> f_iadd(t,u):", r3, "| t,u:", t, u)


def f_bad(a: list[int] = []) -> list[int]:
    a.append(1)
    return a


def f_good(a: list[int] | None = None) -> list[int]:
    if a is None:
        a = []
    a.append(1)
    return a


def demo_mutable_default_argument() -> None:
    section("11) Mutable default argument pitfall")
    print("f_bad() #1:", f_bad())
    print("f_bad() #2:", f_bad())
    print("f_bad() #3:", f_bad())
    print("f_good() #1:", f_good())
    print("f_good() #2:", f_good())


class HauntedBus:
    def __init__(self, passengers: list[str] = []) -> None:
        self.passengers = passengers

    def pick(self, name: str) -> None:
        self.passengers.append(name)

    def drop(self, name: str) -> None:
        self.passengers.remove(name)

    def __repr__(self) -> str:
        return f"HauntedBus(passengers={self.passengers!r})"


class TwilightBus:
    def __init__(self, passengers: list[str] | None = None) -> None:
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name: str) -> None:
        self.passengers.append(name)

    def drop(self, name: str) -> None:
        self.passengers.remove(name)

    def __repr__(self) -> str:
        return f"TwilightBus(passengers={self.passengers!r})"


def demo_hauntedbus_mutable_default_and_defaults_evidence() -> None:
    section("17) Mutable default argument pitfall: HauntedBus")

    bus1 = HauntedBus(["Alice", "Bill"])
    bus1.pick("Charlie")
    bus1.drop("Alice")
    print("bus1:", bus1)

    bus2 = HauntedBus()
    bus2.pick("Carrie")
    print("bus2:", bus2)

    bus3 = HauntedBus()
    bus3.pick("Dave")
    print("bus3:", bus3)

    print("bus2.passengers is bus3.passengers:", bus2.passengers is bus3.passengers)
    print("HauntedBus.__init__.__defaults__:", HauntedBus.__init__.__defaults__)
    if HauntedBus.__init__.__defaults__:
        shared_default = HauntedBus.__init__.__defaults__[0]
        print("__defaults__[0] is bus2.passengers:", shared_default is bus2.passengers)


def demo_twilightbus_defensive_copy() -> None:
    section("18) Defensive copy: TwilightBus does not mutate the caller")

    basketball_team = ["Sue", "Tina", "Maya", "Diana", "Pat"]
    bus = TwilightBus(basketball_team)
    bus.drop("Tina")
    bus.drop("Pat")
    print("bus.passengers:", [safe(x) for x in bus.passengers])
    print("basketball_team (unchanged):", [safe(x) for x in basketball_team])


def demo_dataclass_default_factory_echo() -> None:
    section("15) Dataclass: mutable defaults must use default_factory")

    @dataclass
    class Member:
        name: str
        guests: list[str] = field(default_factory=list)

    m1 = Member("A")
    m2 = Member("B")
    m1.guests.append("Eve")
    print("m1.guests:", [safe(x) for x in m1.guests])
    print("m2.guests:", [safe(x) for x in m2.guests])


def main() -> None:
    demo_parameter_mutate_vs_rebind()
    demo_call_by_sharing_iadd()
    demo_mutable_default_argument()
    demo_dataclass_default_factory_echo()
    demo_hauntedbus_mutable_default_and_defaults_evidence()
    demo_twilightbus_defensive_copy()


if __name__ == "__main__":
    main()
