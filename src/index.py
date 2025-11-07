from varasto import Varasto

def show(label, varasto):
    print(f"{label}: {varasto}")

def luonti(mehu, olut):
    print("Luonnin jälkeen")
    show("Mehuvarasto: ", mehu)
    show("Olutvarasto: ", olut)

def getterit(olut: Varasto):
    print("Olut getterit:")
    print(f"saldo = {olut.saldo}")
    print(f"tilavuus = {olut.tilavuus}")
    print(f"paljonko mahtuu = {olut.paljonko_mahtuu()}")

def mehu_setterit(mehu:Varasto):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehu.lisaa_varastoon(50.7)
    show("Mehuvarasto", mehu)
    print("Otetaan 3.14")
    mehu.ota_varastosta(3.14)
    show("Mehuvarasto", mehu)

def virhetilanne():
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)
    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)

def ylivuoto_lisays(olut:Varasto):
    show("Olutvarasto: ", olut)
    print("olutta.lisaa_varastoon(1000)")
    olut.lisaa_varastoon(1000)
    show("Olutvarasto", olut)

def negatiivinen_lisays(mehu:Varasto):
    show("Mehuvarasto", mehu)
    print("mehua.lisaa_varastoon(-666.0)")
    mehu.lisaa_varastoon(-666.0)
    show("Mehuvarasto", mehu)

def ylisuuri_otto(olut:Varasto):
    show("Olutvarasto", olut)
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olut.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    show("Olutvarasto", olut)

def negatiivinen_otto(mehu:Varasto):
    show("Mehuvarasto", mehu)
    print("mehua.ota_varastosta(-32.9)")
    saatiin = mehu.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    show("Mehuvarasto", mehu)

def demo(mehua:Varasto, olutta:Varasto):
    luonti(mehua, olutta)
    getterit(olutta)
    mehu_setterit(mehua)
    virhetilanne()
    ylivuoto_lisays(olutta)
    negatiivinen_lisays(mehua)
    ylisuuri_otto(olutta)
    negatiivinen_otto(mehua)

def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)
    demo(mehua, olutta)
    print("Testataan pylintin toimivuus githubissa tekemällä todella pitkä rivi tekstiä!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    main()
