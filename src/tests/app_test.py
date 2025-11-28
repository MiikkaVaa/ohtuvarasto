import unittest
from app import app, varastot


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        varastot.clear()

    def tearDown(self):
        varastot.clear()

    def test_index_nayttaa_tyhjan_listan(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Varastot", response.data)

    def test_luo_varasto_get_nayttaa_lomakkeen(self):
        response = self.client.get("/luo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Luo uusi varasto", response.data)

    def test_luo_varasto_post_luo_uuden_varaston(self):
        response = self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Testi", varastot)
        self.assertAlmostEqual(varastot["Testi"].tilavuus, 100)
        self.assertAlmostEqual(varastot["Testi"].saldo, 50)

    def test_luo_varasto_ilman_nimea_nayttaa_virheen(self):
        response = self.client.post("/luo", data={
            "nimi": "",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nimi on pakollinen".encode("utf-8"), response.data)

    def test_luo_varasto_duplikaattinimi_nayttaa_virheen(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        response = self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "50",
            "alku_saldo": "0"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("jo olemassa".encode("utf-8"), response.data)

    def test_nayta_varasto(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "30"
        })
        response = self.client.get("/varasto/Testi")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Testi", response.data)
        self.assertIn(b"30.00", response.data)

    def test_nayta_olematon_varasto_ohjaa_etusivulle(self):
        response = self.client.get("/varasto/Olematon", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Varastot", response.data)

    def test_lisaa_varastoon(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "10"
        })
        self.client.post("/varasto/Testi/lisaa", data={"maara": "20"})
        self.assertAlmostEqual(varastot["Testi"].saldo, 30)

    def test_ota_varastosta(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        self.client.post("/varasto/Testi/ota", data={"maara": "20"})
        self.assertAlmostEqual(varastot["Testi"].saldo, 30)

    def test_poista_varasto(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.assertIn("Testi", varastot)
        self.client.post("/varasto/Testi/poista")
        self.assertNotIn("Testi", varastot)

    def test_muokkaa_varasto_get(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        response = self.client.get("/varasto/Testi/muokkaa")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Muokkaa", response.data)

    def test_muokkaa_varasto_post(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        self.client.post("/varasto/Testi/muokkaa", data={"tilavuus": "200"})
        self.assertAlmostEqual(varastot["Testi"].tilavuus, 200)
        self.assertAlmostEqual(varastot["Testi"].saldo, 50)

    def test_muokkaa_varasto_pienentaa_saldoa(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "80"
        })
        self.client.post("/varasto/Testi/muokkaa", data={"tilavuus": "50"})
        self.assertAlmostEqual(varastot["Testi"].tilavuus, 50)
        self.assertAlmostEqual(varastot["Testi"].saldo, 50)

    def test_lisaa_virheellinen_maara(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "10"
        })
        self.client.post("/varasto/Testi/lisaa", data={"maara": "abc"})
        self.assertAlmostEqual(varastot["Testi"].saldo, 10)

    def test_ota_virheellinen_maara(self):
        self.client.post("/luo", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        self.client.post("/varasto/Testi/ota", data={"maara": "abc"})
        self.assertAlmostEqual(varastot["Testi"].saldo, 50)

    def test_muokkaa_olematon_varasto(self):
        response = self.client.get("/varasto/Olematon/muokkaa",
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_lisaa_olematon_varasto(self):
        response = self.client.post("/varasto/Olematon/lisaa",
                                    data={"maara": "10"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ota_olematon_varasto(self):
        response = self.client.post("/varasto/Olematon/ota",
                                    data={"maara": "10"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
