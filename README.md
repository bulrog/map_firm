# Purpose

Find the companies in France and its distance from a specific GPS coordinates

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

The output will be written in a file named output.csv

This can take a while to compute due to amount of companies so you can also filter on specific activity sections, see list in field 'section_activite_principale' [here](https://recherche-entreprises.api.gouv.fr/docs/#tag/Recherche-geographique):

    python list_firms.py -l 50.8010900 -L 2.4852700 -s B,C

or even on a specific list of actitivities by using their NAF code that you can download from [here](https://www.insee.fr/fr/information/2120875)

WARNING: this only works for detail code like 10.11Z but not 10 or 10.1 or 10.11

    python list_firms.py -l 50.8010900 -L 2.4852700 -a 10.11Z,10.12Z,10.13A,10.13B

The content will be like:

    (.venv) jem@jem-macbook map_firm % head -n 2 output.csv 
    activite_descr,activite_principale,adresse,categorie_entreprise,code_postal,date_fermeture,dirigeants,distance_to_ref,etablissement_tranche_effectif_salarie,etat_administratif,firm_tranche_effectif_salarie,latitude,longitude,nom_complet,nombre_etablissements_ouverts,siege_activite_principale,siege_adresse
    Transport ferroviaire interurbain de voyageurs,49.10Z,115 RUE DU PROFESSEUR LANGEVIN 59000 LILLE,GE,59000,,nom:DAMAS;prenoms:JACQUES;annee_de_naissance:1957;date_de_naissance:1957-05;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:FANICHET;prenoms:CHRISTOPHE;annee_de_naissance:1967;date_de_naissance:1967-10;qualite:Président du conseil d'administration et directeur général;nationalite:Française;type_dirigeant:personne physique||nom:FRANCOIS;prenoms:YOHANNA;annee_de_naissance:1981;date_de_naissance:1981-07;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:LEMAIRE;prenoms:XAVIER-MARIE;annee_de_naissance:1965;date_de_naissance:1965-02;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:MASSIN;prenoms:PHILIPPE;annee_de_naissance:1974;date_de_naissance:1974-03;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:PETITOT;prenoms:JEAN-PHILIPPE;annee_de_naissance:1975;date_de_naissance:1975-01;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:PORTAL;prenoms:XAVIER;annee_de_naissance:1968;date_de_naissance:1968-09;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:PATAY (REY);prenoms:MAGALI;annee_de_naissance:1973;date_de_naissance:1973-06;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||nom:WARNIER (RISMONT);prenoms:STEPHANIE;annee_de_naissance:1965;date_de_naissance:1965-12;qualite:Administrateur;nationalite:Française;type_dirigeant:personne physique||siren:344366315;denomination:ERNST & YOUNG AUDIT;qualite:Commissaire aux comptes titulaire;type_dirigeant:personne morale||siren:672006483;denomination:PRICEWATERHOUSECOOPERS AUDIT;qualite:Commissaire aux comptes titulaire;type_dirigeant:personne morale||,2.6123966006606385,100-199,A,+10000,50.61823,3.086597,SNCF VOYAGEURS,1475,49.10Z,1 RUE CAMILLE MOKE 93210 SAINT-DENIS

The program computes the geo distance between the ref point and the company. The owners are all concatenated in 1 field but can be further expended at a later stage.


