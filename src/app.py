from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# Store varastos in memory with names as keys
varastot = {}


def _validoi_luo_lomake(nimi, tilavuus_str, alku_saldo_str):
    """Validate and parse create form data. Returns (error, tilavuus, saldo)."""
    error = None
    if not nimi:
        error = "Nimi on pakollinen"
    elif nimi in varastot:
        error = "Varasto tällä nimellä on jo olemassa"

    if error:
        return (error, None, None)

    try:
        return (None, float(tilavuus_str), float(alku_saldo_str))
    except ValueError:
        return ("Tilavuus ja alkusaldo pitää olla numeroita", None, None)


def _kasittele_luo_post():
    """Handle POST request for creating varasto. Returns (template, kwargs)."""
    nimi = request.form.get("nimi", "").strip()
    error, tilavuus, alku_saldo = _validoi_luo_lomake(
        nimi, request.form.get("tilavuus", "0"),
        request.form.get("alku_saldo", "0")
    )
    if error:
        return ("luo.html", {"error": error})

    varastot[nimi] = Varasto(tilavuus, alku_saldo)
    return (None, {"nimi": nimi})


@app.route("/")
def index():
    """List all varastos."""
    return render_template("index.html", varastot=varastot)


@app.route("/luo", methods=["GET", "POST"])
def luo_varasto():
    """Create a new varasto."""
    if request.method != "POST":
        return render_template("luo.html")

    template, kwargs = _kasittele_luo_post()
    if template:
        return render_template(template, **kwargs)
    return redirect(url_for("index"))


@app.route("/varasto/<nimi>")
def nayta_varasto(nimi):
    """View a single varasto."""
    if nimi not in varastot:
        return redirect(url_for("index"))
    return render_template("varasto.html", nimi=nimi, varasto=varastot[nimi])


def _validoi_muokkaa_lomake(tilavuus_str):
    """Validate and parse edit form. Returns (error, tilavuus)."""
    try:
        tilavuus = float(tilavuus_str)
    except ValueError:
        return ("Tilavuus pitää olla numero", None)
    if tilavuus <= 0:
        return ("Tilavuus pitää olla positiivinen", None)
    return (None, tilavuus)


def _kasittele_muokkaa_post(nimi, varasto):
    """Handle POST for editing varasto. Returns (template, kwargs) or None."""
    error, tilavuus = _validoi_muokkaa_lomake(request.form.get("tilavuus", "0"))
    if error:
        kwargs = {"nimi": nimi, "varasto": varasto, "error": error}
        return ("muokkaa.html", kwargs)

    uusi_saldo = min(varasto.saldo, tilavuus)
    varastot[nimi] = Varasto(tilavuus, uusi_saldo)
    return None


@app.route("/varasto/<nimi>/muokkaa", methods=["GET", "POST"])
def muokkaa_varasto(nimi):
    """Edit a varasto's capacity."""
    if nimi not in varastot:
        return redirect(url_for("index"))

    varasto = varastot[nimi]
    if request.method != "POST":
        return render_template("muokkaa.html", nimi=nimi, varasto=varasto)

    result = _kasittele_muokkaa_post(nimi, varasto)
    return render_template(result[0], **result[1]) if result else \
        redirect(url_for("nayta_varasto", nimi=nimi))


@app.route("/varasto/<nimi>/lisaa", methods=["POST"])
def lisaa_varastoon(nimi):
    """Add to a varasto."""
    if nimi not in varastot:
        return redirect(url_for("index"))

    maara = request.form.get("maara", "0")
    try:
        maara = float(maara)
    except ValueError:
        return redirect(url_for("nayta_varasto", nimi=nimi))

    varastot[nimi].lisaa_varastoon(maara)
    return redirect(url_for("nayta_varasto", nimi=nimi))


@app.route("/varasto/<nimi>/ota", methods=["POST"])
def ota_varastosta(nimi):
    """Take from a varasto."""
    if nimi not in varastot:
        return redirect(url_for("index"))

    maara = request.form.get("maara", "0")
    try:
        maara = float(maara)
    except ValueError:
        return redirect(url_for("nayta_varasto", nimi=nimi))

    varastot[nimi].ota_varastosta(maara)
    return redirect(url_for("nayta_varasto", nimi=nimi))


@app.route("/varasto/<nimi>/poista", methods=["POST"])
def poista_varasto(nimi):
    """Delete a varasto."""
    if nimi in varastot:
        del varastot[nimi]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
