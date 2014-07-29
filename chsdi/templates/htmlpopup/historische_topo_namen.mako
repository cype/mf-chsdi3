<%inherit file="base.mako"/>

<%def name="table_body(c, lang)">
  <tr><td class="cell-left">${_('tt_histnames_name')}</td>       <td>${c['attributes']['topographic_name'] or '-'}</td></tr>
  <tr><td class="cell-left">${_('tt_histnames_relation')}</td>   <td>${c['attributes']['relation_identifier'] or '-'}</td></tr>
  <tr><td class="cell-left">${_('tt_histnames_kategorie')}</td>  <td>${c['attributes']['category'] or '-'}</td></tr>
  <tr><td class="cell-left">${_('tt_histnames_yearfrom')}</td>   <td>${c['attributes']['year_from'] or '-'}</td></tr>
  <tr><td class="cell-left">${_('tt_histnames_origin')}</td>     <td>${c['attributes']['data_origin'] or '-'}</td></tr>
</%def>

<%def name="extended_info(c, lang)">
<%
    from pyramid.request import Request
    import json

    relationId = c['attributes']['relation_identifier']
    subreq = Request.blank('/rest/services/api/MapServer/find?layer=ch.kantone.historische-topografische-namen&searchText=%s&searchField=relation_identifier&returnGeometry=false&contains=false' % relationId)
    response = request.invoke_subrequest(subreq)
    j = json.loads(response.body)['results']
    names = [t['attributes']['topographic_name'] for t in j]
    years = [t['attributes']['year_from'] for t in j]
    full = dict(zip(names, years))
    sort = sorted(full.items(), key=lambda x: x[1])
%>    
    <table class="table-with-border kernkraftwerke-extended">
          <tr><td class="cell-meta-one" colspan="2"><h1>${c['attributes']['topographic_name'] or '-'}</h1></td></tr>
          <tr><td class="cell-meta-one" colspan="2">&nbsp;</td></tr>
          <tr><td class="cell-left">${_('tt_histnames_relation')}</td>   <td>${c['attributes']['relation_identifier'] or '-'}</td></tr>
          <tr><td class="cell-left">${_('tt_histnames_kategorie')}</td>  <td>${c['attributes']['category'] or '-'}</td></tr>
          <tr><td class="cell-left">${_('tt_histnames_yearfrom')}</td>   <td>${c['attributes']['year_from'] or '-'}</td></tr>
          <tr><td class="cell-left">${_('tt_histnames_origin')}</td>     <td>${c['attributes']['data_origin'] or '-'}</td></tr>
          <tr><td class="cell-meta-one" colspan="2">&nbsp;</td></tr>
% for alternative in xrange(0, len(sort)):
          <tr><td class="cell-left">${_('tt_histnames_alternatives')}</td>      <td>${"%s (%s)" % (sort[alternative][0],sort[alternative][1])}</td></tr>
% endfor
    </table>
</%def>

