"""Example of key derivation using Cardano (Byron addresses)."""

from bip_utils import (
    Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator,
    Bip44Changes, Bip44Coins, Bip44, CardanoBip39SeedGenerator
)

ADDR_NUM: int = 5

# Generate random mnemonic
mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
print(f"Mnemonic string: {mnemonic}")

#
# Cardano Byron Icarus
#

print("BYRON-ICARUS")
print("")

# Generate seed from mnemonic
seed_bytes = CardanoBip39SeedGenerator(mnemonic).Generate()

# Construct from seed
bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.CARDANO_BYRON_ICARUS)
# Print master key
print(f"Master chain code (bytes): {bip44_mst_ctx.PrivateKey().Bip32Key().Data().ChainCode().ToHex()}")
print(f"Master private key (bytes): {bip44_mst_ctx.PrivateKey().Raw().ToHex()}")

# Generate chain keys
bip44_chg_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)

# Generate addresses
print("Addresses:")
for i in range(ADDR_NUM):
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
    print(f"  {i}. Address chain code (bytes): {bip44_addr_ctx.PublicKey().Bip32Key().Data().ChainCode().ToHex()}")
    print(f"  {i}. Address public key (bytes): {bip44_addr_ctx.PublicKey().RawCompressed().ToHex()[2:]}")
    print(f"  {i}. Address private key (bytes): {bip44_addr_ctx.PrivateKey().Raw().ToHex()}")
    print(f"  {i}. Address: {bip44_addr_ctx.PublicKey().ToAddress()}")

#
# Cardano Byron Ledger
#

print("")
print("BYRON-LEDGER")
print("")

# Generate seed from mnemonic
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

# Construct from seed
bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.CARDANO_BYRON_LEDGER)
# Print master key
print(f"Master chain code (bytes): {bip44_mst_ctx.PrivateKey().Bip32Key().Data().ChainCode().ToHex()}")
print(f"Master private key (bytes): {bip44_mst_ctx.PrivateKey().Raw().ToHex()}")

# Generate chain keys
bip44_chg_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)

# Generate addresses
print("Addresses:")
for i in range(ADDR_NUM):
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
    print(f"  {i}. Address chain code (bytes): {bip44_addr_ctx.PublicKey().Bip32Key().Data().ChainCode().ToHex()}")
    print(f"  {i}. Address public key (bytes): {bip44_addr_ctx.PublicKey().RawCompressed().ToHex()[2:]}")
    print(f"  {i}. Address private key (bytes): {bip44_addr_ctx.PrivateKey().Raw().ToHex()}")
    print(f"  {i}. Address: {bip44_addr_ctx.PublicKey().ToAddress()}")