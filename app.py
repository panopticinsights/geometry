# ============================================
# БЛОК 1: ИМПОРТЫ
# ============================================
import dash
from dash import html, dcc, Input, Output, callback, ctx, ALL
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots  # Явный импорт (был пропущен)

# ============================================
# БЛОК 2: ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ
# ============================================
# Инициализация с MathJax 2.7.7 (исправлено для лучшей совместимости)
app = dash.Dash(__name__, external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML'
])

# ============================================
# БЛОК 3: БАЗА ДАННЫХ (ТЕКСТОВЫЕ ОПИСАНИЯ)
# ============================================
materials_db = {
    "Точки, прямые, отрезки": "Точка — базовая фигура. Прямая бесконечна. Отрезок — часть прямой, ограниченная двумя точками, имеет длину.",
    # ... (контент без изменений)
    "Вписанная и описанная окружности": "Окружность внутри (касается сторон) или снаружи (проходит через вершины)."
}

# ============================================
# БЛОК 4: СТРУКТУРА ДЕРЕВА ЗНАНИЙ
# ============================================
knowledge_tree = {
    "Начальные сведения": ["Точки, прямые, отрезки", "Луч и угол", "Сравнение и измерение отрезков", "Измерение углов", "Смежные и вертикальные углы", "Перпендикулярные прямые"],
    # ... (контент без изменений)
    "Окружность (доп)": ["Касательная к окружности", "Центральные и вписанные углы", "Вписанная и описанная окружности"]
}

# ============================================
# БЛОК 5: ФУНКЦИЯ ГЕНЕРАЦИИ ГРАФИКОВ (get_plot)
# ============================================
def get_plot(topic):
    """
    Генерирует Plotly фигуру для выбранной темы.
    Возвращает компонент dcc.Graph.
    """
    fig = go.Figure()

    # Стандартная конфигурация для всех графиков
    fig.update_xaxes(visible=False, range=[-1, 5])
    fig.update_yaxes(visible=False, range=[-1, 5])
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        showlegend=False,
        template="simple_white",
        # Единый размер шрифта для аннотаций (исправление)
        font=dict(size=12)
    )

    # --- БЛОК 5.1: ОБРАБОТКА КОНКРЕТНЫХ ТЕМ ---
    if topic == "Точки, прямые, отрезки":
        # ... (код без изменений)
        pass
        
    elif topic == "Сравнение и измерение отрезков":
        # ... (код без изменений)
        pass
        
    elif topic == "Измерение углов":
        # ... (код без изменений)
        pass
        
    elif topic == "Равнобедренный треугольник":
        # ... (код без изменений)
        pass
        
    # Пример блока с исправлением размера кегля (шрифта)
    elif topic == "Площадь квадрата и прямоугольника":
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Прямоугольник (S = a · b)", "Квадрат (S = a²)"),
                            horizontal_spacing=0.2)

        # --- 1. ПРЯМОУГОЛЬНИК (3x2) ---
        for i in range(4):
            fig.add_trace(go.Scatter(x=[i, i], y=[0, 2], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=1)
        for j in range(3):
            fig.add_trace(go.Scatter(x=[0, 3], y=[j, j], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=1)

        fig.add_trace(go.Scatter(x=[0, 3, 3, 0, 0], y=[0, 0, 2, 2, 0],
                                 fill="toself", fillcolor="rgba(0, 0, 255, 0.1)",
                                 mode='lines', line=dict(color='blue', width=3)), row=1, col=1)

        # ИСПРАВЛЕНО: textangle вынесен из font, добавлен единый размер шрифта
        fig.add_annotation(x=1.5, y=-0.3, text="a = 3", showarrow=False, row=1, col=1, font=dict(size=14)) # Увеличен размер для наглядности
        fig.add_annotation(x=-0.4, y=1, text="b = 2", showarrow=False, row=1, col=1, textangle=-90, font=dict(size=14))
        fig.add_annotation(x=1.5, y=1, text="S = 3 · 2 = 6", showarrow=False, row=1, col=1, font=dict(size=16, weight="bold"))

        # --- 2. КВАДРАТ (2x2) ---
        for i in range(3):
            fig.add_trace(go.Scatter(x=[i, i], y=[0, 2], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=2)
        for j in range(3):
            fig.add_trace(go.Scatter(x=[0, 2], y=[j, j], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=2)

        fig.add_trace(go.Scatter(x=[0, 2, 2, 0, 0], y=[0, 0, 2, 2, 0],
                                 fill="toself", fillcolor="rgba(255, 0, 0, 0.1)",
                                 mode='lines', line=dict(color='crimson', width=3)), row=1, col=2)

        fig.add_annotation(x=1, y=-0.3, text="a = 2", showarrow=False, row=1, col=2, font=dict(size=14))
        fig.add_annotation(x=1, y=1, text="S = 2² = 4", showarrow=False, row=1, col=2, font=dict(size=16, weight="bold"))

        # Настройка осей и единого размера шрифта для подзаголовков
        fig.update_xaxes(range=[-1, 4], showticklabels=False, showgrid=False, zeroline=False)
        fig.update_yaxes(range=[-1, 3], showticklabels=False, showgrid=False, zeroline=False)
        fig.update_layout(height=400, showlegend=False, font=dict(size=12)) # Единый базовый шрифт

    # ... (остальные блоки elif для других тем без изменений)
    elif topic == "Окружность":
        # ... (код без изменений)
        pass
        
    else:
        # Заглушка для тем без специфической графики
        fig.add_annotation(x=2, y=2, text="Визуализация в процессе разработки", showarrow=False, font=dict(size=14, color="gray"))

    # Возвращаем компонент графика
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

# ============================================
# БЛОК 6: ФУНКЦИЯ СОЗДАНИЯ ДЕРЕВА НАВИГАЦИИ
# ============================================
def create_tree():
    """Создает аккордеон с навигацией по темам."""
    return [
        dmc.AccordionItem([
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
        ], value=section) for section, topics in knowledge_tree.items()
    ]

# ============================================
# БЛОК 7: LAYOUT (ВЕРСТКА ПРИЛОЖЕНИЯ)
# ============================================
app.layout = dmc.MantineProvider(
    theme={  # Добавлена глобальная тема для единообразия шрифтов
        "fontFamily": "'Arial', sans-serif",
        "headings": {"fontFamily": "'Arial', sans-serif"},
    },
    children=dmc.Container([
        dmc.Grid([
            # Левая колонка (навигация)
            dmc.GridCol([
                dmc.Paper([
                    dmc.Title("Геометрия 7-9", order=2, mb="md", ta="center"),
                    dmc.Accordion(variant="contained", children=create_tree()),
                ], p="md", withBorder=True, radius="md", shadow="sm")
            ], span=5),

            # Правая колонка (контент)
            dmc.GridCol([
                dmc.Paper([
                    dmc.Title("Справочник и Визуализация", order=3, mb="sm", c="indigo"),
                    dmc.Divider(mb="md"),
                    dmc.ScrollArea(
                        id="material-content",
                        children=dmc.Text("Выберите тему из списка слева.", c="dimmed", fs="italic"),
                        h=750,
                        offsetScrollbars=True
                    ),
                    html.Div(id="mathjax-trigger", style={"display": "none"})
                ], withBorder=True, p="xl", radius="md", shadow="md", style={"backgroundColor": "#fafafa"})
            ], span=7)
        ], gutter="xl")
    ], size="lg", mt="xl")
)

# ============================================
# БЛОК 8: CALLBACK (ОБРАБОТКА КЛИКОВ)
# ============================================
@app.callback(
    Output("material-content", "children"),
    Input({"type": "topic-link", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def display_material(n_clicks):
    """
    Обновляет контент в правой панели при клике на тему.
    """
    # ИСПРАВЛЕНИЕ ОШИБКИ №1: ctx.triggered_id не существует, используем dash.callback_context
    triggered = dash.callback_context.triggered_id
    if not triggered or not any(n_clicks):
        return dash.no_update

    # Получаем название темы из id компонента
    topic_name = triggered['index']
    content = materials_db.get(topic_name, "Материал скоро появится.")

    # Возвращаем структуру с контентом
    return html.Div([
        dmc.Title(topic_name, order=4, mb="xs", c="indigo"),
        dmc.Text(content, size="lg", mb="xl", style={"lineHeight": "1.6"}),
        dmc.Divider(label="Интерактивная модель", labelPosition="center", mb="md"),
        get_plot(topic_name),
        # Скрипт для обновления MathJax
        html.Script("if(window.MathJax){MathJax.Hub.Queue(['Typeset', MathJax.Hub]);}")
    ])

# ============================================
# БЛОК 9: ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================
if __name__ == "__main__":
    # ИСПРАВЛЕНИЕ УЯЗВИМОСТИ: debug=True только для разработки
    # В продакшене должно быть debug=False
    app.run(debug=False) # Изменено с True на False для безопасности