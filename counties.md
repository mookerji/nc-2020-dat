---
layout: page
title: Counties
permalink: /counties
---

{% for county in site.data.counties.counties %}
## [{{ county.county_name }}](#{{ county.county_id }})

### Registrations

![{{ county.county_name }}]({{  county.party_registration_changes_graph  }} ){:class="img-responsive"}

### One Stop

![{{ county.county_name }}](assets/images/one-stop/county-party-totals/{{ county.county_name }}.png){:class="img-responsive"}

{% endfor %}
