import dash
from dash import html, dcc, Input, Output, ALL, callback_context
import dash_mantine_components as dmc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================
# БЛОК 1: ИНИЦИАЛИЗАЦИЯ (Критично для Render)
# ============================================
app = dash.Dash(
    __name__, 
    external_scripts=[
        'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML'
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Переменная для Gunicorn (Укажите в Render Start Command: gunicorn app:server)
server = app.server 
app.title = "Геометрия 7-9: Справочник"

# ============================================
# БЛОК 2: ДАННЫЕ
# ============================================
materials_db = {
    "Точки, прямые, отрезки": "Точка — простейшая геометрическая фигура. Прямая не имеет начала и конца. Отрезок — это часть прямой, ограниченная двумя точками.",
    "Луч и угол": "Луч — часть прямой, имеющая начало, но не имеющая конца. Угол — фигура, образованная двумя лучами с общим началом.",
    "Смежные и вертикальные углы": "Сумма смежных углов равна 180°. Вертикальные углы равны между собой.",
    "Равнобедренный треугольник": "Треугольник называется равнобедренным, если две его стороны равны. Углы при основании равны.",
    "Площадь квадрата и прямоугольника": "Площадь прямоугольника: $S = a \cdot b$. Площадь квадрата: $S = a^2$.",
    "Вписанная и описанная окружности": "Окружность называется вписанной, если она касается всех сторон многоугольника. Описанной — если проходит через все вершины."
}

knowledge_tree = {
    "Начальные сведения": ["Точки, прямые, отрезки", "Луч и угол", "Смежные и вертикальные углы"],
    "Треугольники": ["Равнобедренный треугольник"],
    "Площади фигур": ["Площадь квадрата и прямоугольника"],
    "Окружность": ["Вписанная и описанная окружности"]
}

# ============================================
# БЛОК 3: ГЕНЕРАЦИЯ ГРАФИКОВ
# ============================================
def get_plot(topic):
    fig = go.Figure()
    
    # Стандартные настройки макета
    layout_cfg = dict(
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        showlegend=False,
        template="simple_white",
        font=dict(size=12)
    )

    if topic == "Площадь квадрата и прямоугольника":
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Прямоугольник", "Квадрат"))
        # Прямоугольник
        fig.add_trace(go.Scatter(x=[0, 3, 3, 0, 0], y=[0, 0, 2, 2, 0], fill="toself", fillcolor="rgba(0, 0, 255, 0.1)", line=dict(color='blue', width=3)), row=1, col=1)
        fig.add_annotation(x=1.5, y=1, text="S = a·b", showarrow=False, row=1, col=1, font=dict(size=16))
        # Квадрат
        fig.add_trace(go.Scatter(x=[0, 2, 2, 0, 0], y=[0, 0, 2, 2, 0], fill="toself", fillcolor="rgba(255, 0, 0, 0.1)", line=dict(color='crimson', width=3)), row=1, col=2)
        fig.add_annotation(x=1, y=1, text="S = a²", showarrow=False, row=1, col=2, font=dict(size=16))
        fig.update_xaxes(visible=False, range=[-0.5, 3.5])
        fig.update_yaxes(visible=False, range=[-0.5, 2.5])
        
    elif topic == "Смежные и вертикальные углы":
        # Смежные углы
        fig.add_trace(go.Scatter(x=[-2, 2], y=[0, 0], mode='lines', line=dict(color='black', width=2)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1.5], mode='lines', line=dict(color='red', width=3)))
        fig.add_annotation(x=-0.5, y=0.3, text="180° - α", showarrow=False)
        fig.add_annotation(x=0.5, y=0.3, text="α", showarrow=False)
        fig.update_xaxes(visible=False, range=[-2.5, 2.5])
        fig.update_yaxes(visible=False, range=[-0.5, 2])

    else:
        fig.add_annotation(x=0.5, y=0.5, text="Интерактивная модель в разработке", showarrow=False, font=dict(size=14, color="gray"))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

    fig.update_layout(**layout_cfg)
    return dcc.Graph(figure=fig, config={'displayModeBar': False}, responsive=True)

# ============================================
# БЛОК 4: ИНТЕРФЕЙС (LAYOUT)
# ============================================
def create_tree():
    return [
        dmc.AccordionItem(
            value=section,
            children=[
                dmc.AccordionControl(section),
                dmc.AccordionPanel(
                    dmc.Stack([
                        dmc.NavLink(
                            label=topic,
                            id={"type": "topic-link", "index": topic},
                            variant="subtle",
                            color="indigo"
                        ) for topic in topics
                    ], gap="xs")
                ),
            ]
        ) for section, topics in knowledge_tree.items()
    ]

app.layout = dmc.MantineProvider(
    theme={"fontFamily": "'Inter', sans-serif"},
    children=dmc.Container([
        dmc.Grid([
            # Левая колонка: Меню
            dmc.GridCol([
                dmc.Paper([
                    dmc.Title("Геометрия 7-9", order=2, mb="md", ta="center", c="indigo"),
                    dmc.Accordion(variant="contained", children=create_tree()),
                ], p="md", withBorder=True, radius="md", shadow="sm")
            ], span=12, md=4),

            # Правая колонка: Контент
            dmc.GridCol([
                dmc.Paper([
                    dmc.ScrollArea(
                        id="material-content",
                        children=dmc.Center(
                            dmc.Stack([
                                dmc.Text("Выберите тему из списка слева для изучения", c="dimmed", italic=True),
                            ], align="center"),
                            h=600
                        ),
                        h=750,
                        offsetScrollbars=True
                    ),
                    # Скрытый div для MathJax
                    html.Div(id="mathjax-trigger", style={"display": "none"})
                ], withBorder=True, p="xl", radius="md", shadow="md", style={"backgroundColor": "#ffffff"})
            ], span=12, md=8)
        ], gutter="xl")
    ], size="lg", mt="xl")
)

# ============================================
# БЛОК 5: ЛОГИКА (CALLBACK)
# ============================================
@app.callback(
    Output("material-content", "children"),
    Input({"type": "topic-link", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def display_material(n_clicks):
    # Определяем, на какую ссылку нажали
    triggered = callback_context.triggered_id
    if not triggered or not any(n_clicks):
        return dash.no_update

    topic_name = triggered['index']
    content = materials_db.get(topic_name, "Материал скоро будет добавлен.")

    return html.Div([
        dmc.Title(topic_name, order=3, mb="sm", c="indigo"),
        dmc.Divider(mb="lg"),
        dmc.Text(content, size="lg", mb="xl", style={"lineHeight": "1.7"}),
        
        dmc.Paper([
            dmc.Text("Визуализация", size="sm", fw=700, c="dimmed", mb="xs", ta="center"),
            get_plot(topic_name)
        ], withBorder=True, p="sm", radius="md", bg="#f9f9f9"),
        
        # Скрипт принудительного ререндеринга формул MathJax
        html.Script("if(window.MathJax){MathJax.Hub.Queue(['Typeset', MathJax.Hub]);}")
    ])

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=False)