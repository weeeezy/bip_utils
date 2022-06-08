"""
Example of conversion from a BIP39 mnemonic to an Algorand mnemonic.

It replicates the functionalities of:
    https://github.com/abmera/bip39toalgo
    https://algorand.oortnet.com/
"""

import binascii
from enum import auto, Enum, unique
from bip_utils import (
    AlgorandMnemonicGenerator, Bip39SeedGenerator, Bip32Ed25519Slip, Bip32Ed25519Kholaw, Bip32Secp256k1
)


@unique
class DerivationMethods(Enum):
    BIP39_SEED = auto()
    BIP32_ED25519_KHOLAW = auto()
    BIP32_ED25519_SLIP = auto()
    BIP32_SECP256K1_SLIP = auto()


def convert_seed(bip39_seed_bytes: bytes,
                 der_method: DerivationMethods) -> str:
    # Get private key bytes depending on the derivation method
    if der_method == DerivationMethods.BIP39_SEED:
        priv_key_bytes = bip39_seed_bytes[:32]
    elif der_method == DerivationMethods.BIP32_ED25519_KHOLAW:
        bip32_ctx = Bip32Ed25519Kholaw.FromSeedAndPath(bip39_seed_bytes, "m/44'/283'/0'/0/0")
        priv_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
    elif der_method == DerivationMethods.BIP32_ED25519_SLIP:
        bip32_ctx = Bip32Ed25519Slip.FromSeedAndPath(bip39_seed_bytes, "m/44'/283'/0'/0'/0'")
        priv_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
    elif der_method == DerivationMethods.BIP32_SECP256K1_SLIP:
        bip32_ctx = Bip32Secp256k1.FromSeedAndPath(bip39_seed_bytes, "m/44'/283'/0'/0/0")
        priv_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
    else:
        raise ValueError("Invalid derivation method")

    # Encode the private key to Algorand mnemonic
    algorand_mnemonic = AlgorandMnemonicGenerator().FromEntropy(priv_key_bytes).ToStr()

    # Print result
    print(f"Derivation method: {der_method}")
    print(f"  Algorand private key: {binascii.hexlify(priv_key_bytes)}")
    print(f"  Algorand mnemonic: {algorand_mnemonic}")
    print("")

    return algorand_mnemonic


# Generate BIP39 seed from mnemonic
mnemonic = "all all all all all all all all all all all all all all all all all all all all all all all feel"
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
# Print
print(f"BIP39 mnemonic: {mnemonic}")
print(f"BIP39 seed: {binascii.hexlify(seed_bytes)}")
print("")

# Convert with all possible methods
convert_seed(seed_bytes, DerivationMethods.BIP39_SEED)
convert_seed(seed_bytes, DerivationMethods.BIP32_ED25519_SLIP)
convert_seed(seed_bytes, DerivationMethods.BIP32_ED25519_KHOLAW)
convert_seed(seed_bytes, DerivationMethods.BIP32_SECP256K1_SLIP)
