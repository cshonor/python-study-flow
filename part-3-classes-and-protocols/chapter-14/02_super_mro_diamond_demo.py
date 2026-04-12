from __future__ import annotations


def log(msg: str) -> None:
    print(msg)


class A:
    def ping(self) -> None:
        log("A.ping start")
        log("A.ping end")


class B(A):
    def ping(self) -> None:
        log("B.ping start")
        super().ping()
        log("B.ping end")


class C(A):
    def ping(self) -> None:
        log("C.ping start")
        super().ping()
        log("C.ping end")


class D(B, C):
    def ping(self) -> None:
        log("D.ping start")
        super().ping()
        log("D.ping end")


def main() -> None:
    print("MRO for D:")
    print(" -> ".join(cls.__name__ for cls in D.__mro__))

    print("\nCall order with cooperative super():")
    D().ping()


if __name__ == "__main__":
    main()

