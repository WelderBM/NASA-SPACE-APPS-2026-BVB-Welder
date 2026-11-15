defs=open('defs.svg').read(); world=open('world.svg').read(); parts=open('parts.svg').read(); js=open('script.js').read()
html=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#000;overflow:hidden}}svg{{display:block}}text{{font-family:'Inter','Inter Display',Arial,sans-serif}}</style></head><body>
<svg id="v" width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
{defs}
{world}
{parts}
<g id="tag" opacity="0" transform="translate(110,110)"><rect x="0" y="0" width="640" height="70" rx="35" fill="#1C2620" opacity=".85"/><text x="34" y="46" font-size="32" font-weight="700" fill="#F5F0E6">Cantá, Roraima · Brazilian Amazon</text></g>
<g id="subBox" opacity="0"><rect id="subBg" x="460" y="966" width="1000" height="80" rx="20" fill="#0E1512" opacity=".8"/><text id="sub" x="960" y="1020" text-anchor="middle" font-size="44" font-weight="600" fill="#FFFFFF"></text></g>
<text x="1880" y="52" text-anchor="end" font-size="22" font-weight="600" fill="#FFFFFF" opacity=".85" style="paint-order:stroke" stroke="#000" stroke-opacity=".35" stroke-width="3">AI-generated: animation by Claude · voice by Kokoro TTS</text>
</svg><script>{js}</script></body></html>'''
open('scene3.html','w').write(html)
