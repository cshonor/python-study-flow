from __future__ import annotations


class Root:
    def ping(self) -> None:
        print(f"{self}.ping() in Root")

    def pong(self) -> None:
        print(f"{self}.pong() in Root")

    def __repr__(self) -> str:
        return f"<instance of {type(self).__name__}>"


class A(Root):
    def ping(self) -> None:
        print(f"{self}.ping() in A")
        super().ping()

    def pong(self) -> None:
        print(f"{self}.pong() in A")
        super().pong()


class B(Root):
    def ping(self) -> None:
        print(f"{self}.ping() in B")
        super().ping()

    def pong(self) -> None:
        print(f"{self}.pong() in B")
        # Intentionally NOT cooperative: no super().pong()


class Leaf(A, B):
    def ping(self) -> None:
        print(f"{self}.ping() in Leaf")
        super().ping()


class U:
    def ping(self) -> None:
        print(f"{self}.ping() in U")
        super().ping()


class LeafUA(U, A):
    def ping(self) -> None:
        print(f"{self}.ping() in LeafUA")
        super().ping()


def show_mro(cls: type) -> None:
    print(" -> ".join(c.__name__ for c in cls.__mro__))


def main() -> None:
    print("MROs")
    print("Leaf:", end=" ")
    show_mro(Leaf)
    print("LeafUA:", end=" ")
    show_mro(LeafUA)
    print("U:", end=" ")
    show_mro(U)

    print("\nleaf1.ping() call chain")
    leaf1 = Leaf()
    leaf1.ping()

    print("\nleaf1.pong() call chain (B breaks cooperation)")
    leaf1.pong()

    print("\nleaf2 = LeafUA(); leaf2.ping() call chain")
    leaf2 = LeafUA()
    leaf2.ping()

    print("\nU().ping() (U alone has no next ping in MRO)")
    try:
        U().ping()
    except AttributeError as e:
        print("AttributeError:", e)


if __name__ == "__main__":
    main()

