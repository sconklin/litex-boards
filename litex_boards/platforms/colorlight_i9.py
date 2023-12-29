#
# This file is part of LiteX-Boards.
#
# Based on the colorlight_i9plus.py file which is:
# Copyright (c) 2023 Charles-Henri Mousset <ch.mousset@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.lattice import LatticeECP5Platform
from litex.build.lattice.programmer import EcpDapProgrammer

#from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk.
    ("clk25", 0, Pins("P3"), IOStandard("LVCMOS33")),

    # Leds.
    ("user_led_n", 0, Pins("L2"), IOStandard("LVCMOS33")),

    # Reset button
    ("cpu_reset_n", 0, Pins("L2"), IOStandard("LVCMOS33"), Misc("PULLMODE=UP")),

    # RGMII Ethernet (B50612D) PHY 0.
    ("eth_clocks", 0, # U5 is SDIO phy #0
        Subsignal("tx", Pins("U19")),
        Subsignal("rx", Pins("L19")),
        IOStandard("LVCMOS33")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("P4")),
        Subsignal("mdio",    Pins("P5")),
        Subsignal("mdc",     Pins("N5")),
        Subsignal("rx_ctl",  Pins("M20")),
        Subsignal("rx_data", Pins("P20 N19 N20 M19")),
        Subsignal("tx_ctl",  Pins("P19")),
        Subsignal("tx_data", Pins("U20 T19 T20 R20")),
        IOStandard("LVCMOS33")
    ),
    # RGMII Ethernet (B50612D) PHY 1.
    ("eth_clocks", 1, # U9 is SDIO phy #1
        Subsignal("tx", Pins("G1")),
        Subsignal("rx", Pins("H2")),
        IOStandard("LVCMOS33")
    ),
    ("eth", 1,
        Subsignal("rst_n",   Pins("P4")),
        Subsignal("mdio",    Pins("P5")),
        Subsignal("mdc",     Pins("N5")),
        Subsignal("rx_ctl",  Pins("H2")),
        Subsignal("rx_data", Pins("K2 L1 N1 P1")),
        Subsignal("tx_ctl",  Pins("K1")),
        Subsignal("tx_data", Pins("G2 H1 J1 J3")),
        IOStandard("LVCMOS33")
    ),

    # SPIFlash (W25Q64JVSIQ)
    ("spiflash", 0,
        Subsignal("cs_n", Pins("R2")),
        # https://github.com/m-labs/nmigen-boards/pull/38
        #Subsignal("clk",  Pins("")), driven through USRMCLK
        Subsignal("mosi", Pins("W2")),
        Subsignal("miso", Pins("V2")),
        IOStandard("LVCMOS33"),
    ),

    # SDRRAM (M12L64322A).
    ("sdram_clock", 0, Pins("B9"), IOStandard("LVCMOS33")),
    ("sdram", 0,
        Subsignal("a", Pins(
            "B13 C14 A16 A17 B16 B15 A14 A13 ",
            "A12 A11 B12")),  # Address pin A11 routed but NC on M12L64322A
        Subsignal("dq", Pins(
            "B6 A5 A6 A7 C7 B8 B5 A8 "
            "D8 D7 E8 D6 C6 D5 E7 C5 "
            "C10 D9 E11 D11 C11 D12 E9 C12 "
            "E14 C15 E13 D15 E12 B17 D14 D13 "
            )),
        Subsignal("we_n",  Pins("A10")),
        Subsignal("ras_n", Pins("B10")),
        Subsignal("cas_n", Pins("A9")),
        #Subsignal("cs_n", Pins("")), # GND
        #Subsignal("cke",  Pins("")), # 3V3
        Subsignal("ba",    Pins("B11 C8")),
        #Subsignal("dm",   Pins("")), # GND
        IOStandard("LVCMOS33"),
        Misc("SLEWRATE=FAST")
    ),

    ("serialx", 0, Subsignal("tx", Pins("K18")), Subsignal("rx", Pins("T18")), IOStandard("LVCMOS33")),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("dimm",
        "- "
        "    GND      5V     GND      5V     GND      5V     GND      5V     GND      5V"  #   1-10
        "    GND      5V      NC      NC ETH1_1P ETH2_1P ETH1_1N ETH2_1N      NC      NC"  #  11-20
        "ETH1_2N ETH2_2N ETH1_2P ETH2_2P      NC      NC ETH1_3P ETH2_3P ETH1_3N ETH2_3N"  #  21-30
        "     NC      NC ETH1_4N ETH2_4N ETH1_4P ETH2_4P      NC      NC     GND     GND"  #  31-40
        "     L2      R1      NC      T1      NC      U1      NC      Y2     K18      W1"  #  41-50
        "    C18      V1      NC      M1     GND     GND     T18      N2     R18      N3"  #  51-60
        "    R17      T2     P17      M3     M17      T3     T17      R3     U18      N4"  #  61-70
        "    U17      M4     P18      L4     N17      L5     N18     P16     M18     J16"  #  71-80
        "    L20     J18     L18     J17     K20     H18     K19     H17     J20     G18"  #  81-90
        "    J19     H16     H20     F18     G20     G16     G19     E18     F20     F17"  #  91-100
        "    F19     F16     E20     E16     GND     GND     GND     GND     E19     E17"  # 101-110
        "    D20     D18     D19     D17     C20      G5     B20     D16     B19      F5"  # 111-120
        "    B18      E6     A19      E5     C17      F4     A18      E4      D3      F1"  # 121-130
        "     C4      F3      B4      G3      C3      H3      E3      H4      A3      H5"  # 131-140
        "     C2      J4      B1      J5      C1      K3      D2      K4      D1      K5"  # 141-150
        "     E2      B3      E1      A2      F2      B2     GND     GND      NC      NC"  # 151-160
        "     NC      NC      NC      NC      NC      NC      NC      NC      NC      NC"  # 161-170
        "     NC      NC      NC      NC      NC      NC      NC      NC      NC      NC"  # 171-180
        "     NC      NC      NC      NC      NC      NC      NC      NC      NC      NC"  # 181-190
        "     NC      NC      NC      NC      NC      NC      NC      NC     GND     GND"  # 191-200
    )
]

# Platform -----------------------------------------------------------------------------------------
class Platform(LatticeECP5Platform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self, board="i9", revision="7.2", toolchain="trellis"):
        self.revision = revision
        device     = "LFE5U-45F-6BG381C"

        LatticeECP5Platform.__init__(self, device, _io, connectors=_connectors, toolchain=toolchain)

    def create_programmer(self):
        return EcpDapProgrammer()

    def do_finalize(self, fragment):
        LatticeECP5Platform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk25",            loose=True), 1e9/25e6)
        self.add_period_constraint(self.lookup_request("eth_clocks:rx", 0, loose=True), 1e9/125e6)
        self.add_period_constraint(self.lookup_request("eth_clocks:rx", 1, loose=True), 1e9/125e6)
