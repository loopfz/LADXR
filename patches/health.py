from assembler import ASM
from utils import formatText


def setStartHealth(rom, amount):
    rom.patch(0x01, 0x0B1C, ASM("ld  [hl], $03"), ASM("ld  [hl], $%02X" % (amount)))  # max health of new save
    rom.patch(0x01, 0x0B14, ASM("ld  [hl], $18"), ASM("ld  [hl], $%02X" % (amount * 8)))  # current health of new save


def upgradeHealthContainers(rom):
    # Reuse 2 unused shop messages for the heart containers.
    rom.texts[0x2A] = formatText(b"You found an extra heart!")
    rom.texts[0x2B] = formatText(b"You lost a heart!")

    rom.patch(0x03, 0x19DC, ASM("""
        ld   de, $59D8
        call $3BC0
    """), ASM("""
        ld  a, $05  ; renderHeartPiece
        rst 8
    """), fill_nop=True)
    rom.patch(0x03, 0x19F0, ASM("""
        ld  hl, $DB5B
        inc [hl]
        ld  hl, $DB93
        ld   [hl], $FF
    """), ASM("""
        ld  a, $06 ; giveItemMultiworld
        rst 8
    """), fill_nop=True)  # add heart->remove heart on heart container
    rom.patch(0x03, 0x19D8, "AA14AA34", "AA17AA37")  # Change color of the heart containers
