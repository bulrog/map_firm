import requests
import argparse
import time
import csv
from geopy.distance import geodesic

code_to_effectifs = {
    "00": "0",
    "01": "1-2",
    "02": "3-5",
    "03": "6-9",
    "11": "10-19",
    "12": "20-49",
    "21": "50-99",
    "22": "100-199",
    "31": "200-249",
    "32": "250-499",
    "41": "500-999",
    "42": "1000-1999",
    "51": "2000-4999",
    "52": "5000-9999",
    "53": "+10000"
}


def make_get_request(url, max_retry, wait_between_retry_in_sec):
    retry = 0
    while retry < max_retry:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            retry += 1
        time.sleep(wait_between_retry_in_sec)


def get_all_pages(url, max_retry, wait_between_retry_in_sec):
    page = 1
    all_results = []
    while page > 0:
        single_page = make_get_request(url + str(page), max_retry, wait_between_retry_in_sec)
        print(f"get page {page} on a total of {single_page.json()['total_pages']}")
        all_results.extend(single_page.json()['results'])
        if (single_page.json()['total_pages'] < page):
            page = -1
        else:
            page += 1
    return all_results


def parse_arguments():
    """Parses command-line arguments in Linux style.

    Returns:
      An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Script to give the list og firms around a position defined by its lattitude and longitude and the radius")
    parser.add_argument("-l", "--latitude", help="latitude of the position to look around", required=True)
    parser.add_argument("-L", "--longitude", help="longitude of the position to look around", required=True)
    parser.add_argument("-r", "--radius", help="radius in km to look around (max 50kms)", default="5")
    parser.add_argument("-R", "--retry", help="amount of retry in case of error from the API", default=3)
    parser.add_argument("-s", "--section", help="section activite principale de l'entreprise comma separated (A,B,..)",
                        required=False)
    parser.add_argument("-a", "--activite", help="activite principale de l'entreprise (code NAF: 10.12Z,10.20Z,...)",
                        required=False)
    parser.add_argument("-w", "--wait", help="wait between retry in seconds in case of error from the API",
                        default=10)

    return parser.parse_args()


def write_to_csv(data, filename):
    """
    Writes the flattened JSON data to a CSV file.

    Args:
      data: The flattened JSON data (list of dictionaries).
      filename: The name of the CSV file to write to.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = set()
        for row in data:
            fieldnames.update(row.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_dirigeants(dirigeants):
    result = ""
    for dirigeant in dirigeants:
        result = result + ";".join(f"{key}:{value}" for key, value in dirigeant.items()) + "||"

    return result


def filter_non_active_firm(firms):
    return [firm for firm in firms if firm['etat_administratif'] == 'A']


def enrich_distance_from_ref(refpoint, firms):
    for firm in firms:
        firm['distance_to_ref'] = geodesic(refpoint, (firm['latitude'], firm['longitude'])).km
    return firms


def enrich_activite_descr(firms):
    activite_to_map = csv_to_map('codeNaf2desc.csv')

    for firm in firms:
        if firm['activite_principale'] not in activite_to_map.keys():
            firm['activite_descr'] = None
        else:
            firm['activite_descr'] = activite_to_map[firm['activite_principale']]
    return firms


def get_effectifs(code):
    if not code:
        return None
    if code not in code_to_effectifs.keys():
        return None
    return code_to_effectifs[code]


def csv_to_map(csv_file):
    result_map = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row if present
        for row in reader:
            key = row[0]
            value = row[1]
            result_map[key] = value
    return result_map


def get_dict_firms(response):
    results = []
    for firm in response:
        for etablissement in firm['matching_etablissements']:
            result = {'nom_complet': firm['nom_complet'],
                      'nombre_etablissements_ouverts': firm['nombre_etablissements_ouverts'],
                      'siege_adresse': firm['siege']['adresse'],
                      'siege_activite_principale': firm['siege']['activite_principale'],
                      'categorie_entreprise': firm['categorie_entreprise'],
                      'date_fermeture': firm['date_fermeture'],
                      'firm_tranche_effectif_salarie': get_effectifs(firm['tranche_effectif_salarie']),
                      'activite_principale': etablissement['activite_principale'],
                      'adresse': etablissement['adresse'],
                      'code_postal': etablissement['code_postal'],
                      'etat_administratif': etablissement['etat_administratif'],
                      'latitude': etablissement['latitude'],
                      'longitude': etablissement['longitude'],
                      'etablissement_tranche_effectif_salarie': get_effectifs(
                          etablissement['tranche_effectif_salarie']),
                      'dirigeants': get_dirigeants(firm['dirigeants'])

                      }
            results.append(result)

    return results


def build_url(args):
    url = f"https://recherche-entreprises.api.gouv.fr/near_point?lat={args.latitude}&long={args.longitude}&radius={args.radius}"
    if args.section:
        url = url + f"&section_activite_principale={args.section}"
    if args.activite:
        url = url + f"&activite_principale={args.activite}"
    print(f"url used to get the data:{url}")
    return url + "&page="


if __name__ == "__main__":
    args = parse_arguments()

    response = get_all_pages(build_url(args), args.retry, args.wait)
    write_to_csv(
        enrich_activite_descr(enrich_distance_from_ref((args.latitude, args.longitude),
                                                       filter_non_active_firm(get_dict_firms(response)))),
        f"output.csv")
