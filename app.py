import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from methods.basic_data_functions import nb_pizzerias, average_rate_pizzerias

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.Div([
        html.Div(children=[
            html.H1('Pizza Lovers'),
            html.H6(children=["Les pizzas les meilleures pour les visiteurs venus d'ailleurs"], style= {'margin-right': '5px'}),
        ]),
        html.Div([
            html.Div(className="btn btn-outline-dark", style={"max-width": "20rem", 'margin-left': '50px'},children =[
                html.Div(className = "card-header", children= ["Combien de pizzerias dans la base ?",
                    html.Div(className = "card-body", children =[
                        html.H4(className = "card-title", children=str(nb_pizzerias()))
                    ])
                ])
            ]),
            html.Div(className="btn btn-outline-dark", style={"max-width": "20rem", 'margin-left': '50px'},children =[
                html.Div(className = "card-header", children= ["Note moyenne de pizzerias parisiennes",
                    html.Div(className = "card-body", children =[
                        html.H4(className = "card-title", children=[str(average_rate_pizzerias()) + " /5"])
                    ])
                ])
            ]),
            html.Div(className="btn btn-outline-dark", style={"max-width": "20rem", 'margin-left': '50px'},children =[
                html.Div(className = "card-header", children= ["Villes où nous opérons",
                    html.Div(className = "card-body", children =[
                        html.H4(className = "card-title", children=["Paris"]),
                        html.P("Bientôt le monde entier", className ="card-text")
                    ])
                ])
            ]),
            
        ], className="d-flex justify-content-around"),
    ], className="d-flex justify-content-between"),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"], style={'color': 'rgb(173, 173, 169)'}
                ), className= "btn btn-outline-dark", style= {'margin-right': '5px'}
            )
            for page in dash.page_registry.values()
        ], className="d-flex flex-row"
    ),
    html.Div(className='separation_div'),

	dash.page_container,
    html.Div(className='separation_div'),
    html.Footer('Bientôt, ici, un vrai footer, quand on aura un vrai designer.', className='footer')
], className='centering_div')

if __name__ == '__main__':
	app.run_server(debug=True)

server = app.server