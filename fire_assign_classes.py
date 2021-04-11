import geopandas as gpd

data=gpd.read_file("http://ec2-35-153-102-199.compute-1.amazonaws.com/elastic/Neighbourhoods.geojson")
print(data)
close={'Agincourt North': 4, 'Agincourt South-Malvern West': 4, 'Alderwood': 5, 'Annex': 4, 'Banbury-Don Mills': 4, 'Bathurst Manor': 4, 'Bay Street Corridor': 5, 'Bayview Village': 5, 'Bayview Woods-Steeles': 4, 'Bedford Park-Nortown': 4, 'Beechborough-Greenbrook': 5, 'Bendale': 3, 'Birchcliffe-Cliffside': 4, 'Black Creek': 3, 'Blake-Jones': 5, 'Briar Hill - Belgravia': 4, 'Bridle Path-Sunnybrook-York Mills': 5, 'Broadview North': 5, 'Brookhaven-Amesbury': 4, 'Cabbagetown-South St. James Town': 4, 'Caledonia-Fairbank': 4, 'Casa Loma': 4, 'Centennial Scarborough': 4, 'Church-Yonge Corridor': 4, 'Clairlea-Birchmount': 4, 'Clanton Park': 4, 'Cliffcrest': 4, 'Corso Italia-Davenport': 4, 'Danforth': 5, 'Danforth-East York': 4, 'Don Valley Village': 4, 'Dorset Park': 3, 'Dovercourt-Wallace Emerson-Junction': 4, 'Downsview-Roding-CFB': 1, 'Dufferin Grove': 5, 'East End-Danforth': 4, 'Edenbridge-Humber Valley': 4, 'Eglinton East': 4, 'Elms-Old Rexdale': 4, 'Englemount-Lawrence': 3, 'Eringate-Centennial-West Deane': 5, 'Etobicoke West Mall': 4, 'Flemingdon Park': 4, 'Forest Hill North': 5, 'Forest Hill South': 5, 'Glenfield-Jane Heights': 2, 'Greenwood-Coxwell': 5, 'Guildwood': 5, 'Henry Farm': 4, 'High Park North': 4, 'High Park-Swansea': 4, 'Highland Creek': 4, 'Hillcrest Village': 4, 'Humber Heights-Westmount': 4, 'Humber Summit': 4, 'Humbermede': 3, 'Humewood-Cedarvale': 4, 'Ionview': 5, 'Islington-City Centre West': 3, 'Junction Area': 5, 'Keelesdale-Eglinton West': 4, 'Kennedy Park': 4, 'Kensington-Chinatown': 4, 'Kingsview Village-The Westway': 4, 'Kingsway South': 5, "L'Amoreaux": 3, 'Lambton Baby Point': 5, 'Lansing-Westgate': 5, 'Lawrence Park North': 5, 'Lawrence Park South': 5, 'Leaside-Bennington': 4, 'Little Portugal': 4, 'Long Branch': 5, 'Malvern': 2, 'Maple Leaf': 4, 'Markland Wood': 5, 'Milliken': 4, 'Mimico (includes Humber Bay Shores)': 4, 'Morningside': 4, 'Moss Park': 4, 'Mount Dennis': 4, 'Mount Olive-Silverstone-Jamestown': 2, 'Mount Pleasant East': 5, 'Mount Pleasant West': 4, 'New Toronto': 4, 'Newtonbrook East': 5, 'Newtonbrook West': 3, 'Niagara': 4, 'North Riverdale': 5, 'North St. James Town': 4, "O'Connor-Parkview": 4, 'Oakridge': 4, 'Oakwood Village': 4, 'Old East York': 5, 'Palmerston-Little Italy': 5, 'Parkwoods-Donalda': 4, 'Pelmo Park-Humberlea': 4, 'Playter Estates-Danforth': 5, 'Pleasant View': 4, 'Princess-Rosethorn': 5, 'Regent Park': 5, 'Rexdale-Kipling': 5, 'Rockcliffe-Smythe': 4, 'Roncesvalles': 5, 'Rosedale-Moore Park': 5, 'Rouge': 2, 'Runnymede-Bloor West Village': 5, 'Rustic': 4, 'Scarborough Village': 4, 'South Parkdale': 4, 'South Riverdale': 4, 'St.Andrew-Windfields': 5, 'Steeles': 3, 'Stonegate-Queensway': 4, "Tam O'Shanter-Sullivan": 4, 'Taylor-Massey': 4, 'The Beaches': 5, 'Thistletown-Beaumond Heights': 4, 'Thorncliffe Park': 3, 'Trinity-Bellwoods': 5, 'University': 5, 'Victoria Village': 4, 'Waterfront Communities-The Island': 4, 'West Hill': 4, 'West Humber-Clairville': 2, 'Westminster-Branson': 3, 'Weston': 4, 'Weston-Pellam Park': 4, 'Wexford/Maryvale': 4, 'Willowdale East': 4, 'Willowdale West': 5, 'Willowridge-Martingrove-Richview': 4, 'Woburn': 1, 'Woodbine Corridor': 5, 'Woodbine-Lumsden': 5, 'Wychwood': 4, 'Yonge-Eglinton': 5, 'Yonge-St.Clair': 5, 'York University Heights': 3, 'Yorkdale-Glen Park': 4}

cl=[]
#data["class"].apply(lambda x: "AREA_NAME"*10)
for item in data.iterrows():
    if len(item[1]["AREA_NAME"].split(" ("))==2:
        cl.append(close[item[1]["AREA_NAME"].split(" (")[0]])
    else:
        try:
            if item[1]["AREA_NAME"]=="Mimico (includes Humber Bay Shores) (17)":
                cl.append(close["Mimico (includes Humber Bay Shores)"])
            else:    
                mm=""
                ll=item[1]["AREA_NAME"].split(" (")
                for el in ll:
                    if ll.index(el)<len(ll)-2:     
                        mm +=el
                print(mm)         
                cl.append(close[mm])
        except:
            print(item[1]["AREA_NAME"])
print(cl)        
print(len(cl))
data["cl"]=cl
print(data)
data.to_file("canada/toronto/Neighbourhoods_cl.geojson", driver='GeoJSON')
