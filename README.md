# Purpose

Find the companies in France and its distance from your location

# setup

Install virtualenv and python 3 on your PC. Then run the following in the projet folder:

    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

# usage

run to get the different options:

    python list_firms.py -h 

The script will search from a latitude and a longitude for a specific radius in km (default 5km) a list of companies in activities. Example:

    python list_firms.py -l 50.8010900 -L 2.4852700 

The output will be written in a file named output followed by the provided arguments like:
'output_Namespace(latitude='50.8010900', longitude='2.4852700', radius='10', retry=3, section=None, activite='10.11Z,10.12Z,10.13A,10.13B', wait=10)'

The content will be like:

    (.venv) jem@jem-macbook map_firm % head -n 2 output_Namespace\(latitude=\'50.8010900\',\ longitude=\'2.4852700\',\ radius=\'10\',\ retry=3,\ section=None,\ activite=\'10.11Z,10.12Z,10.13A,10.13B\',\ wait=10\)
    nombre_etablissements_ouverts,activite_principale,longitude,etablissement_tranche_effectif_salarie,latitude,distance_to_ref,code_postal,dirigeants,siege_activite_principale,nom_complet,siege_adresse,firm_tranche_effectif_salarie,date_fermeture,etat_administratif,adresse,activite_descr,categorie_entreprise
    1,10.13A,2.543734,10-19,50.721212,9.7967265967429,59190,siren:413686692;denomination:MEDITERRANEENNE DE SALAISONS;qualite:Directeur Général;type_dirigeant:personne morale||siren:920690237;denomination:KORMOBOIS;qualite:Président de SAS;type_dirigeant:personne morale||,10.13A,BOIZET NORD (BOIZET JAMBONS),30 RUE D'HOLLEBECQUE 59190 HAZEBROUCK,10-19,,A,30 RUE D'HOLLEBECQUE 59190 HAZEBROUCK,Préparation industrielle de produits à base de viande,PME

The program computes the geo distance between the ref point and the company. The owners are all concatenate in 1 field but can be further expended at a later stage.


