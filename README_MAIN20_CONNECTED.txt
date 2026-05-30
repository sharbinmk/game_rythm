MoonRhythm Main 2.0 Connected Build

Run this file:
    python "Main_2_0_connected.py"

This merged copy uses your Main 2.0.py menu as the entry point and connects it to Dylan's gameplay after the loading screen.

Original files are still included and unchanged:
    Main 2.0.py
    Main.py
    systems/*

Only Main_2_0_connected.py is the new connection file.

Current chart mapping:
    Song 1 / Freeplay Normal / Freeplay Hard -> charts/Fraq

When another song is added later, edit get_gameplay_chart() inside Main_2_0_connected.py.

Required packages:
    pip install pygame pytweening
