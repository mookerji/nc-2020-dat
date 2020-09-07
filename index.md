---
layout: page
title: Statewide Overview
---

![under construction](http://textfiles.com/underconstruction/mamagnolia_acresunderconstruction.gif){:class="img-responsive"}

## [Summary](#summary)

{% include tables/totals_summary.html %}

- Registrations since 2020-02-28 (before COVID-19 shelter-in-place), absentee
  registrations since 2020-01-01.
- 'Other' = Registrations for Constitution, Green, Libertarian Parties

## [Registration](#registrations)

### [By Week](#registrations)

![registration count and changes]({{ site.data.state.state.statewide_registrations_changes_by_party }} ){:class="img-responsive"}

### [By County](#counties)

![registration count and density]({{ site.data.state.state.statewide_registrations_by_county_density }} ){:class="img-responsive"}
<br/><br/>
![registration normalized]({{ site.data.state.state.party_new_electorate_per_county_graph }} ){:class="img-responsive"}

## [Absentee/VBM Requests](#absentee)

![vbm_demographics]({{ site.data.state.state.statewide_vbm_requests_by_demographic }} ){:class="img-responsive"}
<br/><br/>
![vbm county]({{ site.data.state.state.statewide_vbm_requests_by_county }} ){:class="img-responsive"}

## [Maps](#maps)

### Most Registrants By County

{% include images/bokeh/state-party-registration-change.html %}
