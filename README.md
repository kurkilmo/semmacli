# Semmacli
Komentonlinjaohjelma Semman ruokalistojen hakemiseen.

## Asennus
Riippuvuuksien asennus komennolla
```
poetry install
```
Tämän jälkeen ohjelman voi ajaa komennolla
```
poetry run semmacli
```

pip-asennettavan paketin voi muodostaa komennolla
```
poetry build
```
Luodun paketin voi asentaa komennolla
```
pip install dist/*.whl
```

Mikäli järjestelmäsi ei tue Python-pakettien asennusta järjestelmän pipillä, voit käyttää [pipx](https://github.com/pypa/pipx):ää tai virtuaaliympäristöjä:
```
python -m venv venv
source venv/bin/activate
```

# Käyttö
```
semmacli [valinnat] [ravintolat]
```
Esimerkiksi `semmacli piato maija` tulostaa Piaton ja Maijan päivän ruokalistat.

## Valinnat
Saatavilla olevat valinnat:
| Valinta | Kuvaus |
| ------- | ------ |
| -l, --list | Tulostaa saatavilla olevat ravintolat |
| -w, --week | Tulostaa koko viikon ruokalistan |
| -a, --all | Tulostaa kaikkien saatavilla olevien ravintoloiden ruokalistat |
| --set-default <oletusravintola> | Asettaa oletusarvoisen ravintolan. Oletuksen asettamisen jälkeen pelkkä komento `semmacli` tulostaa oletusravintolan päivän ruokalistan.
| -d | Tulostaa annettujen ravintoloiden lisäksi oletusravintolan |

Tieto oletusravintolasta tallennetaan tiedostoon `~/.config/semmacli.json`.

