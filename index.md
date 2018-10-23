---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---
<table class="table-program">
<tr>
  <th class="h1 text-center">Title</th>
  <th class="h1 text-center">Date</th>
</tr>
{% for program in site.programs reversed %}
  <tr>
    <td><a href="{{ program.url }}">{{ program.title }}</a></td>
    <td>{{ program.prog.date | date: "%B %-d, %Y - %I:%M%p" }}</td>
  </tr>
{% endfor %}
</table>

{% assign all_programs = site.programs | map : "prog" | map : "tme" %}
{% for m in site.data.members %}
{{m[0]}}
{% endfor %}
{{all_programs}}