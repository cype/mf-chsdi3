<%inherit file="base.mako"/>

<%def name="table_body(c, lang)">
<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
    <%
        id = c['attributes']['nummer']
    %>
<script>
$( document ).ready(function() {
    $.getJSON( "https://mf-chsdi3.dev.bgdi.ch/fap_oev_service/transports/stops/${c['attributes']['nummer']}", function(result){
      for (var i = 0; i < result.length; i++) {
        $("#numero").append(result[i].type + " " + result[i].label + " " + result[i].destination + "<br />");
        $("#departures").append(result[i].time + "<br />");
      };
    });
});
</script>
    <tr><td>Next departures</td>
        <td id="numero"></td>
        <td id="departures"></td>
    </tr>
</%def>

