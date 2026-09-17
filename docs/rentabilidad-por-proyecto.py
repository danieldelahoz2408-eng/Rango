# v2: precios por proyecto (no por hora), calibrados con fuentes 2025-2026. COP miles.
projects = {
 'Pack anuncios pauta (5 piezas, ½ día)': (3000, {'DOP ½ jornada':350,'Edición pack':500,'Motion 1 pieza':300,'Logística':150}, 16),
 'Video de marca / corporativo 2–3 min (½–1 día)': (4000, {'DOP jornada':600,'Sonido':300,'Edición':700,'Motion':200,'Logística':200}, 18),
 'Clip musical indie (1 jornada)': (5500, {'DOP jornada':600,'Asistente':200,'Equipo extra':250,'Edición clip':700,'Color':250,'Locación':200,'Maquillaje':200,'Logística':250}, 30),
 'Comercial 30 s + 3 cutdowns (1 jornada)': (10000, {'DOP jornada':700,'Gaffer':200,'Sonido':350,'Equipo extra':300,'Locación':400,'Talento':500,'Maquillaje':200,'Edición':1000,'Color':400,'Motion':400,'Logística':300}, 40),
 'Branding completo (freelance diseño)': (4000, {'Diseño identidad + manual':1500,'Animación de logo':300,'Mockups':100}, 20),
 'Landing + identidad express': (2500, {'Web no-code landing':800,'Diseño express':400}, 10),
 'Sitio corporativo 5–7 páginas': (7000, {'Web no-code sitio':1800,'Diseño':800,'Copy':400,'Fotos':450}, 20),
 'Retainer Rango Lab (8 piezas/mes)': (3000, {'DOP ½ jornada':350,'Edición 8 piezas':700,'Diseño':250,'Logística':100}, 16),
}
T=60
print(f"{'Proyecto':50}{'Precio':>7}{'Freel':>7}{'MB%':>5}{'Hrs':>4}{'Contrib':>8}")
for n,(p,c,h) in projects.items():
    cc=sum(c.values()); print(f"{n:50}{p:7}{cc:7}{(p-cc)/p*100:5.0f}{h:4}{p-cc-h*T:8}")
k=list(projects)
def pl(name, idx, fijos, sueldo, hon):
    ing=sum(projects[k[i]][0] for i in idx); fr=sum(sum(projects[k[i]][1].values()) for i in idx); hrs=sum(projects[k[i]][2] for i in idx)
    mb=ing-fr; h=ing*hon; u=mb-fijos-sueldo-h
    print(f"{name:62} ing {ing:6} freel {fr:6} MB {mb:6} ({mb/ing*100:.0f}%) fijos {fijos} sueldo {sueldo} honor {h:.0f} UTIL {u:.0f} hrs {hrs}")
pl('F1 · 2 proy (pack + clip)', [0,2], 2200, 0, .15)
pl('F1 · 3 proy (pack + clip + landing)', [0,2,5], 2200, 0, .15)
pl('F1 · 4 proy (pack, clip, landing, video marca)', [0,2,5,1], 2200, 0, .15)
pl('F2a · 5 proy (clip, comercial, branding, retainer, pack)', [2,3,4,7,0], 4900, 5200, .05)
pl('F2a · 6 proy (comercial, comercial, clip, branding, 2 retainers)', [3,3,2,4,7,7], 4900, 5200, .05)
pl('F2b · 9 proy (3 comerciales, clip, branding, sitio, 3 retainers)', [3,3,3,2,4,6,7,7,7], 7700, 11700, 0)
