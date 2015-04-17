from chrome import panel

stats_template = """
<div class="stats-container">
  <table class="stats-table">
    <tr><th>Members</th><th>Subscribers</th></tr>
    <tr class="text-info"><td>{members}</td><td>{subscribers}</td></tr>
  </table>
  <div class="pull-right"><button class="btn btn-info">Subscribe</button></div>
</div>
<style>
  .stats-table {{
    width: 180px
    padding: 0px;
    margin: 0px;
    display: inline-block;
  }}
  .stats-table th {{
    text-transform: uppercase;
    font-size: 80%;
    padding-right: 10px;
    color: #797a7c;
  }}
  .stats-table td {{
    font-size: 32pt;
  }}

</style>
"""

@panel()
def render(request, session, widget):
    return stats_template.format(
        members=len(widget.hub.members),
        subscribers=len(widget.hub.subscribers),
    )