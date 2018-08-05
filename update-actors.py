#!/usr/bin/env python3
"""
Creates a new utils/actors.ts from the misp-galaxy threat actor cluster.
"""
import json
import io
import os

try:
    import iso3166
except:
    print(
        "You need to have the iso3166 module installed:\npip install -r requirements.txt"
    )


if __name__ == "__main__":
    try:
        os.remove("src/utils/actors.ts")
    except FileNotFoundError:
        pass
    with io.open("resources/misp-galaxy/clusters/threat-actor.json", "r") as handle:
        data = json.loads(handle.read())

        # Convert country code
        print("Converting country codes...")
        count = 0
        for actor in data["values"]:
            actor.update({"aptmap": {"operatingFrom": None, "victims": []}})

            if actor["meta"].get("country", None):
                c = actor["meta"]["country"]
                actor["meta"]["country"] = iso3166.countries.get(c)[0]
                actor["aptmap"]["operatingFrom"] = iso3166.countries.get(c)[2]

            for v in actor["meta"].get("cfr-suspected-victims", []):
                try:
                    actor["aptmap"]["victims"].append(iso3166.countries.get(v)[2])
                except:
                    count += 1
                    if (
                        "U.S." in v
                        or "US " in v
                        or "United States" in v
                        or "America" in v
                        or "Fifth Third Bank" in v
                        or "PNC" in v
                        or "BB&T" in v
                        or "Wells Fargo" in v
                        or "Capital One" in v
                        or "Citigroup" in v
                        or "Sony Pictures" in v
                    ):
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("USA")[2]
                        )
                        print("Mapped {} to USA.".format(v))
                    elif "Rus" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("RUS")[2]
                        )
                    elif "United Kingdom" in v or "HSBC" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("GB")[2]
                        )
                    elif "South Korea" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("KR")[2]
                        )
                    elif "Ministry of Unification" in v or "Sejong" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("KR")[2]
                        )
                        print("Mapped {} to South Korea.".format(v))
                    elif "Korea" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("KP")[2]
                        )
                    elif "Vietnam" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("VNM")[2]
                        )
                    elif "Phillipines" in v or "The Philippines" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("PHL")[2]
                        )
                    elif "Laos" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("LAO")[2]
                        )
                    elif "Iran" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("IRN")[2]
                        )
                    elif "Syria" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("SYR")[2]
                        )
                    elif "Tajikstan" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("TJK")[2]
                        )
                    elif "Venezuela" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("VEN")[2]
                        )
                    elif "World Anti-Doping Agency" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("CAN")[2]
                        )
                        print("Mapped {} to Canada.".format(v))
                    elif "Asia Pacific Economic Cooperation" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("SGP")[2]
                        )
                        print("Mapped {} to Singapur.".format(v))
                    elif "International Association of Athletics Federations" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("MCO")[2]
                        )
                        print("Mapped {} to Monaco.".format(v))
                    elif "Bangladesh" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("BGD")[2]
                        )
                        print("Mapped {} to Bangladesh.".format(v))
                    elif "OSCE" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("AT")[2]
                        )
                        print("Mapped {} to Austria.".format(v))
                    elif "Ivory Coast" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("CIV")[2]
                        )
                    elif "Association of Southeast Asian Nations" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("IDN")[2]
                        )
                        print("Mapped {} to Indonesia.".format(v))
                    elif "Brunei" in v:
                        actor["aptmap"]["victims"].append(
                            iso3166.countries.get("BRN")[2]
                        )
                    else:
                        print("Could not get iso3166 code for {}.".format(v))

        print("ℹ️  Needed to remap {} victim entries.".format(count))
        if not os.path.isdir("src/utils"):
            os.mkdir("src/utils")
        with io.open("src/utils/actors.ts", "w") as output:
            output.write("let actors = ")
            output.write(json.dumps(data, indent=4))
            output.write(";\n\nexport default actors;")
    if os.path.isfile("src/utils/actors.ts"):
        print("✔️  New threat actor file was written.")
        print(
            "ℹ️  Above errors about iso3166 codes are related to currently not available mapping between iso3166 country names and CFR victim property."
        )
    else:
        print("Could not update threat actors.")
        exit(1)
