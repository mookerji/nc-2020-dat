---
layout: page
title: Counties
permalink: /counties
---

{% for county in site.data.counties.counties %}
## [{{ county.county_name | capitalize }}](#{{ county.county_name }})

![{{ county.county_name }}]({{  county.party_registration_graph}} ){:class="img-responsive"}

{% endfor %}
