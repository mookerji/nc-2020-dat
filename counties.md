---
layout: page
title: Counties
permalink: /counties
---

{% for county in site.data.counties.counties %}

## [{{ county.county_name }}](#{{ county.county_id }})

### [Registrations](#{{ county.county_id }}-registrations)

![{{ county.county_name }}]({{  county.party_registration_changes_graph  }} ){:class="img-responsive"}


### [Votes Cast (By Demographic)](#{{ county.county_id }}-dempgrahic)

![{{ county.county_name }}](assets/images/accepted/demographic-cumulative-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}
<br/><br/>
![{{ county.county_name }}](assets/images/accepted/demographic-per-week-totals//{{ county.county_name | downcase }}.png){:class="img-responsive"}


### [Votes Cast (By Request Type)](#{{ county.county_id }}-accepted)

![{{ county.county_name }}](assets/images/accepted/type-per-week-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### [One Stop (By Day)](#{{ county.county_id }}-one-stop-by-day)

![{{ county.county_name }}](assets/images/one-stop/per-week-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### [One Stop (By Polling Location)](#{{ county.county_id }}-one-stop-locations)

![{{ county.county_name }}](assets/images/one-stop/county-party-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}
<br/><br/>
![{{ county.county_name }}](assets/images/one-stop/county-race-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}
<br/><br/>
![{{ county.county_name }}](assets/images/one-stop/county-age-totals/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### [Days to Send Requested Absentee-by-Mail (ABM) Ballot](#{{ county.county_id }}-latency)

![{{ county.county_name }}](assets/images/abm-latency/request-to-mail/{{ county.county_name | downcase }}.png){:class="img-responsive"}


### [Days from Request to Return ABM Ballot](#{{ county.county_id }}-latency)

![{{ county.county_name }}](assets/images/abm-latency/request-to-return/{{ county.county_name | downcase }}.png){:class="img-responsive"}

---------------------------------------
{% endfor %}
