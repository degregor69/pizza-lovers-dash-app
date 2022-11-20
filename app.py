import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from methods.basic_data_functions import nb_pizzerias, average_rate_pizzerias

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
	html.H1('Pizza Lovers'),
    html.H6("Les pizzas les meilleures pour les visiteurs venus d'ailleurs"),
    html.H6(children=["Nous avons actuellement " + str(nb_pizzerias()) + " pizzerias dans notre base."]),
    html.H6(children=["Leur note moyenne est de : " + str(average_rate_pizzerias()) + " étoiles." ]),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    html.Div(className='separation_div'),

	dash.page_container,
    html.Div(className='separation_div'),
    html.Footer('Bientôt, ici, un vrai footer, quand on aura un designer.', className='footer')
], className='centering_div')

if __name__ == '__main__':
	app.run_server(debug=True)