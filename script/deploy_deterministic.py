import boa
from boa.util.abi import Address, abi_encode
import pathlib
from vyper.utils import keccak256  # type: ignore

proxy_address = "0x4e59b44847b379578588920cA78FbF26c0B4956C"

factory_salt = bytes.fromhex(
    "0000000000000000000000000000000000000000a0c12da352d6a86617080018"
)

def proxy_deploy(initcode: bytes, constructor_schema = None, *constructor_args, deployment_salt: bytes = bytes(32)) -> Address:
    if len(deployment_salt) != 32:
        raise ValueError("Deployment salt must be exactly 32 bytes long")

    if constructor_schema is not None:
        initcode += abi_encode(constructor_schema, *constructor_args)

    address = keccak256(b"\xff" + bytes.fromhex(proxy_address.strip("0x")) + deployment_salt + keccak256(initcode))[12:]
    if boa.env.get_code(address) == b"":
        boa.env.raw_call(to_address=proxy_address, data=deployment_salt + initcode)
    return Address(address)

def compile_vy(src: str) -> bytes:
    import vyper
    from vyper.compiler import compile_from_file_input
    from vyper.compiler.input_bundle import FilesystemInputBundle

    input_bundle = FilesystemInputBundle(search_paths=[pathlib.Path("contracts/")])
    compiled = compile_from_file_input(input_bundle.load_file(src), output_formats=["bytecode"])
    if "bytecode" not in compiled:
        raise ValueError("Compilation failed")
    
    return bytes.fromhex(compiled["bytecode"].strip("0x"))

def moccasin_main():
    raffle_implementation = proxy_deploy(compile_vy("RaffleImplementation.vy"))
    print(f"{raffle_implementation}")
    raffle_factory = proxy_deploy(compile_vy("RaffleFactory.vy"), "address", raffle_implementation, deployment_salt=factory_salt)
    print(f"{raffle_factory}")
