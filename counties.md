---
layout: page
title: Counties
permalink: /counties
---

{% for county in site.data.counties.counties %}

## [{{ county.county_name }}](#{{ county.county_id }})

### Registrations

![{{ county.county_name }}]({{  county.party_registration_changes_graph  }} ){:class="img-responsive"}


### One Stop (By Day)

![{{ county.county_name }}](assets/images/one-stop/per-week-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### One Stop (By Polling Location)

![{{ county.county_name }}](assets/images/one-stop/county-party-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}

![{{ county.county_name }}](assets/images/one-stop/county-race-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}

![{{ county.county_name }}](assets/images/one-stop/county-age-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### Days to Send Requested Absentee-by-Mail Ballot

![{{ county.county_name }}](assets/images/abm-latency/request-to-mail/{{ county.county_name | downcase }}.png){:class="img-responsive"}

---------------------------------------
{% endfor %}
