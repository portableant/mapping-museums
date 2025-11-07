import csv
import json

def convert_csv_to_geojson(csv_file, geojson_file):
    """
    Converts a CSV file with lat/lon coordinates into a GeoJSON file.
    """
    geojson = {
        "type": "FeatureCollection",
        "indexing": {
            "@context": "https://schema.org/",
            "@type": "Dataset",
            "name": "Mapping Museums Dataset from Birkbeck, University of London",
            "description": "Data downloaded from the Mapping Museums website at www.mappingmuseums.org Accessed on 7th November 2025.",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "identifier": "https://museweb.dcs.bbk.ac.uk/"
        },
        "features": []
    }

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create a new, cleaned row dictionary
                cleaned_row = {key: value.replace(u'\xa0', u' ') if isinstance(value, str) else value for key, value in row.items()}
                print(row.get('Year_closed'))
                try:
                    # Clean up and validate coordinates
                    lat_str = cleaned_row.get('Latitude', '').strip()
                    lon_str = cleaned_row.get('Longitude', '').strip()

                    # Skip records with empty or invalid coordinates
                    if not lat_str or not lon_str:
                        print(f"Skipping row with id '{cleaned_row.get('museum_id', 'N/A')}' due to missing coordinates.")
                        continue

                    lat = float(lat_str)
                    lon = float(lon_str)

                    # Create a GeoJSON Feature
                    # Format 'Year_opened' date to YYYY
                    created_raw = cleaned_row.get('Year_opened')
                    created_year = None
                    if created_raw:
                        try:
                            created_year = str(created_raw).strip()[:4]
                            if not created_year.isdigit():
                                created_year = None
                        except Exception:
                            created_year = None
                    
                    closed_raw = cleaned_row.get('Year_closed')
                    closed_year = None
                    if closed_raw:
                        try:
                            closed_year = str(closed_raw).strip()[:4]
                            if not closed_year.isdigit() or closed_year == '9999':
                                closed_year = None
                        except Exception:
                            closed_year = None
                    
                    feature = {
                        "@id": f"https://museweb.dcs.bbk.ac.uk/Museum/{cleaned_row.get('museum_id')}",
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        },
                        "properties": {
                            "museum_id": cleaned_row.get('museum_id'),
                            "name": cleaned_row.get('Name_of_museum'),
                            "title": cleaned_row.get('Name_of_museum'),
                            "address_line_1": cleaned_row.get('Address_line_1'),
                            "address_line_2": cleaned_row.get('Address_line_2'),
                            "village_town_city": cleaned_row.get('Village,_Town_or_City'),
                            "postcode": cleaned_row.get('Postcode'),
                            "latitude": cleaned_row.get('Latitude'),
                            "longitude": cleaned_row.get('Longitude'),
                            "admin_area": cleaned_row.get('Admin_area'),
                            "accreditation": cleaned_row.get('Accreditation'),
                            "governance": cleaned_row.get('Governance'),
                            "size": cleaned_row.get('Size'),
                            "size_provenance": cleaned_row.get('Size_provenance'),
                            "subject_matter": cleaned_row.get('Subject_Matter'),
                            "year_opened": created_year,
                            "year_closed": row.get('Year_closed'),
                            "domus_subject_matter": cleaned_row.get('DOMUS_Subject_Matter'),
                            "domus_identifier": cleaned_row.get('DOMUS_identifier'),
                            "primary_provenance_of_data": cleaned_row.get('Primary_provenance_of_data'),
                            "identifier_used_in_primary_data_source": cleaned_row.get('Identifier_used_in_primary_data_source'),
                            "area_deprivation_index": cleaned_row.get('Area_Deprivation_index'),
                            "area_deprivation_index_crime": cleaned_row.get('Area_Deprivation_index_crime'),
                            "area_deprivation_index_education": cleaned_row.get('Area_Deprivation_index_education'),
                            "area_deprivation_index_employment": cleaned_row.get('Area_Deprivation_index_employment'),
                            "area_deprivation_index_health": cleaned_row.get('Area_Deprivation_index_health'),
                            "area_deprivation_index_housing": cleaned_row.get('Area_Deprivation_index_housing'),
                            "area_deprivation_index_income": cleaned_row.get('Area_Deprivation_index_income'),
                            "area_deprivation_index_services": cleaned_row.get('Area_Deprivation_index_services'),
                            "area_geodemographic_group": cleaned_row.get('Area_Geodemographic_group'),
                            "area_geodemographic_group_code": cleaned_row.get('Area_Geodemographic_group_code'),
                            "area_geodemographic_subgroup": cleaned_row.get('Area_Geodemographic_subgroup'),
                            "area_geodemographic_subgroup_code": cleaned_row.get('Area_Geodemographic_subgroup_code'),
                            "area_geodemographic_supergroup": cleaned_row.get('Area_Geodemographic_supergroup'),
                            "area_geodemographic_supergroup_code": cleaned_row.get('Area_Geodemographic_supergroup_code'),
                            "notes": cleaned_row.get('Notes'),
                            "created": created_year,
                            "closed": closed_year
                        }
                    }
                    
                    description = cleaned_row.get('Notes', '').strip()
                    if description:
                        feature['descriptions'] = [
                            {
                                "value": description
                            }
                        ]
                    
                    # Add 'when' key only if 'fromDate' is present
                    from_date = cleaned_row.get('fromdate', '').strip().split('.')[0]
                    if from_date:
                        to_date = cleaned_row.get('todate', '').strip().split('.')[0]
                        if to_date:
                            feature['when'] = {
                                "timespans": [
                                    {
                                        "start": {
                                            "in": f"{from_date}" if from_date else ""
                                        },
                                        "end": {
                                            "in": f"{to_date}" if to_date else "",
                                        }
                                    }
                                ]
                            }

                    
                    geojson['features'].append(feature)
                except (ValueError, TypeError) as e:
                    print(f"Skipping row with ID '{cleaned_row.get('museum_id', 'N/A')}' due to invalid coordinate data: {e}")
                    continue

        with open(geojson_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
            
        print(f"\nSuccessfully converted {len(geojson['features'])} valid records to {geojson_file}")
            
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
            
if __name__ == "__main__":
    input_csv = "data/MappingMuseumsData2021_09_30.csv"
    output_geojson = "data/museums.geojson"
    convert_csv_to_geojson(input_csv, output_geojson)
