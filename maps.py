import folium

def generer_carte_multicouches(latitude, longitude, rayon_macro, rayon_micro):
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    folium.Marker([latitude, longitude], tooltip="Site central").add_to(m)
    
    # Couverture macro
    folium.Circle(
        [latitude, longitude], 
        radius=rayon_macro * 1000, 
        color="blue", fill=True, fill_opacity=0.2, 
        popup="Macro-cellule"
    ).add_to(m)
    
    # Couverture micro
    folium.Circle(
        [latitude, longitude], 
        radius=rayon_micro * 1000, 
        color="red", fill=True, fill_opacity=0.1,
        popup="Small-cells"
    ).add_to(m)
    
    return m._repr_html_()
