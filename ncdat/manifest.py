import click
import pandas as pd
import yaml

import sys

def make_counties_manifest(changes):
    manifest = {'counties': []}
    for county_name, county_data in changes.groupby('CountyName'):
        k =  county_name.lower().replace(' ', '_')
        image_name = 'assets/images/county-registration-by-party/' + k + '.png'
        change_name = 'assets/images/county-registration-changes/' + k + '.png'
        cumul_name = 'assets/images/cumulative-county-registration-changes/' + k + '.png'
        joined_name = 'assets/images/county-registration-and-changes-by-party/' + k + '.png'
        manifest['counties'].append({'county_name': county_name.lower().title(),
                                     'county_id': k,
                                     'party_registration_graph': image_name,
                                     'party_change_graph': change_name,
                                     'party_cumulative_change_graph': cumul_name,
                                     'party_registration_changes_graph': joined_name})
    return manifest

def make_state_manifest():
    manifest = {'state': {}}
    manifest['state']['party_registration_graph'] = 'assets/images/statewide-registrations-by-party.png'
    manifest['state']['party_new_electorate_per_county_graph'] = 'assets/images/pct-new-electorate-change-vs-population.png'
    manifest['state']['party_registration_changes_graph'] = 'assets/images/weekly-party-affiliation-changes.png'
    manifest['state']['party_cumulative_registration_changes_graph'] = 'assets/images/cumulative-party-affiliation-changes.png'
    manifest['state']['statewide_registrations_changes_by_party'] = 'assets/images/statewide-registrations-changes-by-party.png'
    manifest['state']['statewide_registrations_by_county_density'] = 'assets/images/statewide-registrations-by-county-density.png'
    manifest['state']['statewide_vbm_requests_by_demographic'] = 'assets/images/statewide-vbm-requests-by-demographic.png'
    manifest['state']['statewide_vbm_requests_by_county'] = 'assets/images/statewide-vbm-requests-by-county.png'
    manifest['state']['statewide_vbm_requests_by_demographic_weekly'] = 'assets/images/statewide-vbm-requests-by-demographic-weekly.png'
    manifest['state']['statewide_vbm_rejections_by_county'] = 'assets/images/statewide-vbm-rejections-by-county.png'
    manifest['state']['statewide_vbm_submissions_by_county'] = 'assets/images/statewide-vbm-submissions-by-county.png'
    manifest['state']['statewide_vbm_rejected_by_demographic_weekly'] = 'assets/images/statewide-vbm-rejected-by-demographic-weekly.png'
    manifest['state']['statewide_vbm_rejected_by_demographic'] = 'assets/images/statewide-vbm-rejected-by-demographic.png'
    manifest['state']['statewide_vbm_submissions_by_demographic_weekly'] = 'assets/images/statewide-vbm-submissions-by-demographic-weekly.png'
    manifest['state']['statewide_vbm_submissions_by_demographic'] = 'assets/images/statewide-vbm-submissions-by-demographic.png'
    return manifest

@click.command()
def main():
    with open('_data/counties.yml', 'w+') as f:
        f.write(yaml.dump(make_counties_manifest()))
    with open('_data/state.yml', 'w+') as f:
        f.write(yaml.dump(make_state_manifest()))

if __name__ == '__main__':
    sys.exit(main())
