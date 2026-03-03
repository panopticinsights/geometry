import dash
from dash import html, dcc, Input, Output, ctx, ALL
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np

# Инициализация с MathJax 3 (более современная версия)
app = dash.Dash(__name__, external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML'
])

# База данных материалов (без изменений контента)
materials_db = {
    "Точки, прямые, отрезки": "Точка — базовая фигура. Прямая бесконечна. Отрезок — часть прямой, ограниченная двумя точками, имеет длину.",
    "Луч и угол": "Луч имеет начало, но не имеет конца. Угол — фигура, образованная двумя лучами (сторонами), выходящими из одной точки (вершины).",
    "Сравнение и измерение отрезков": "Длина отрезка — положительное число. Равные отрезки имеют равные длины.",
    "Измерение углов": "Углы измеряются в градусах. Развернутый угол равен 180°. Прямой угол равен 90°.",
    "Смежные и вертикальные углы": "Сумма смежных углов равна 180°. Вертикальные углы равны между собой.",
    "Перпендикулярные прямые": "Две прямые пересекаются под прямым углом (90°).",
    "Признаки равенства": "Три признака: 1) по двум сторонам и углу, 2) по стороне и двум углам, 3) по трем сторонам.",
    "Медианы, биссектрисы и высоты": "Медиана делит сторону пополам, биссектриса делит угол пополам, высота — перпендикуляр к прямой.",
    "Равнобедренный треугольник": "Две стороны равны. Углы при основании равны. Медиана к основанию — это также высота и биссектриса.",
    "Окружность": "Точки, равноудаленные от центра. Расстояние до центра — радиус ($R$).",
    "Задачи на построение": "Задачи, решаемые циркулем и линейкой без делений.",
    "Признаки параллельности": "Параллельны, если накрест лежащие углы равны или сумма односторонних равна 180°.",
    "Аксиома параллельных прямых": "Через точку вне прямой проходит только одна параллельная ей прямая.",
    "Углы при параллельных и секущей": "При пересечении параллельных прямых секущей образуются равные накрест лежащие углы.",
    "Сумма углов треугольника": "Всегда равна 180°.",
    "Внешний угол": "Равен сумме двух внутренних углов, не смежных с ним.",
    "Прямоугольный треугольник": "Один угол 90°. Гипотенуза и катеты.",
    "Теорема Пифагора": "В прямоугольном треугольнике: $$a^2 + b^2 = c^2$$.",
    "Тригонометрия (синус, косинус, тангенс)": "Sin — отношение противолежащего катета к гипотенузе, Cos — прилежащего к гипотенузе.",
    "Признаки равенства прямоугольных треугольников": "По гипотенузе и катету, по двум катетам, по гипотенузе и острому углу.",
    "Многоугольники": "Сумма углов выпуклого $n$-угольника: $$(n-2) \\times 180^\\circ$$.",
    "Параллелограмм": "Стороны попарно параллельны. Противоположные стороны и углы равны.",
    "Трапеция": "Две стороны параллельны (основания). Средняя линия: $$\\frac{a+b}{2}$$.",
    "Прямоугольник, ромб, квадрат": "Специальные виды параллелограммов с особыми свойствами углов и сторон.",
    "Осевая и центральная симметрия": "Отражение относительно прямой или точки.",
    "Свойства площадей": "Равные фигуры имеют равные площади.",
    "Площадь квадрата и прямоугольника": "$$S = a \\times b$$ или $$S = a^2$$.",
    "Площадь параллелограмма": "$$S = a \\times h$$.",
    "Площадь треугольника": "$$S = \\frac{1}{2} a \\times h$$.",
    "Площадь трапеции": "$$S = \\frac{a+b}{2} \\times h$$.",
    "Определение подобия": "Одинаковая форма, пропорциональные стороны ($k$).",
    "Признаки подобия": "1) по двум углам, 2) по двум сторонам и углу, 3) по трем сторонам.",
    "Средняя линия треугольника": "Параллельна основанию и равна его половине.",
    "Замечательные точки треугольника": "Центроид, инцентр, ортоцентр, центр описанной окружности.",
    "Касательная к окружности": "Перпендикулярна радиусу в точке касания.",
    "Центральные и вписанные углы": "Центральный равен дуге, вписанный — половине дуги.",
    "Вписанная и описанная окружности": "Окружность внутри (касается сторон) или снаружи (проходит через вершины)."
}

knowledge_tree = {
    "Начальные сведения": ["Точки, прямые, отрезки", "Луч и угол", "Сравнение и измерение отрезков", "Измерение углов", "Смежные и вертикальные углы", "Перпендикулярные прямые"],
    "Треугольники": ["Признаки равенства", "Медианы, биссектрисы и высоты", "Равнобедренный треугольник", "Окружность", "Задачи на построение"],
    "Параллельные прямые": ["Признаки параллельности", "Аксиома параллельных прямых", "Углы при параллельных и секущей"],
    "Соотношения в треугоринике": ["Сумма углов треугольника", "Внешний угол", "Прямоугольный треугольник", "Теорема Пифагора", "Тригонометрия (синус, косинус, тангенс)", "Признаки равенства прямоугольных треугольников"],
    "Четырёхугольники": ["Многоугольники", "Параллелограмм", "Трапеция", "Прямоугольник, ромб, квадрат", "Осевая и центральная симметрия"],
    "Площадь": ["Свойства площадей", "Площадь квадрата и прямоугольника", "Площадь параллелограмма", "Площадь треугольника", "Площадь трапеции"],
    "Подобные треугольники": ["Определение подобия", "Признаки подобия", "Средняя линия треугольника", "Замечательные точки треугольника"],
    "Окружность (доп)": ["Касательная к окружности", "Центральные и вписанные углы", "Вписанная и описанная окружности"]
}

def get_plot(topic):
    fig = go.Figure()
    
    # Конфигурация по умолчанию
    fig.update_xaxes(visible=False, range=[-1, 5])
    fig.update_yaxes(visible=False, range=[-1, 5])
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        height=350, 
        showlegend=False, 
        template="simple_white"
    )

    # Использование словаря функций или if-elif для логики отрисовки
    if topic == "Точки, прямые, отрезки":
        fig.add_trace(go.Scatter(x=[0, 4], y=[1, 1], mode='lines+markers+text', text=["A", "B"], textposition="bottom center"))
        fig.add_trace(go.Scatter(x=[-1, 5], y=[2, 2], mode='lines', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=[0.5, 2, 4.5], y=[0.5, 1, 0.8], mode='markers+text', text=["C", "D", "E"], textposition="bottom center", marker=dict(size=10, color='crimson')))

    elif topic == "Сравнение и измерение отрезков":
        # Отрезок AB
        fig.add_trace(go.Scatter(
            x=[0.5, 3.5], y=[3, 3], 
            mode='lines+markers+text', 
            text=["A", "B"], 
            textposition="top center",
            line=dict(color='indigo', width=4),
            marker=dict(size=10)
        ))
        
        # Отрезок CD (такой же длины)
        fig.add_trace(go.Scatter(
            x=[0.5, 3.5], y=[1.5, 1.5], 
            mode='lines+markers+text', 
            text=["C", "D"], 
            textposition="bottom center",
            line=dict(color='crimson', width=4),
            marker=dict(size=10)
        ))

        # Обозначение равенства (черточки посередине отрезков)
        fig.add_annotation(x=2, y=3, text="|", showarrow=False, font=dict(size=20, color="indigo"))
        fig.add_annotation(x=2, y=1.5, text="|", showarrow=False, font=dict(size=20, color="crimson"))

        # Итоговая надпись под ними
        fig.add_annotation(
            x=2, y=0.2, 
            text="отрезок АВ = отрезку СD", 
            showarrow=False, 
            font=dict(size=16, color="black", family="Arial")
        )
        
        # Фиксируем масштаб, чтобы отрезки не растягивались
        fig.update_xaxes(range=[0, 4])
        fig.update_yaxes(range=[0, 4])

    elif topic == "Медианы, биссектрисы и высоты":
        # Вершины треугольника
        ax, ay = 0, 0
        bx, by = 4, 0
        cx, cy = 1, 3.5

        # Основной треугольник
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ax], y=[ay, by, cy, ay], mode='lines', line=dict(color='black', width=3), name="Треугольник"))

        # --- ВЫСОТА (красная) ---
        fig.add_trace(go.Scatter(x=[1, 1], y=[3.5, 0], mode='lines', line=dict(color='red', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=[1, 1.2, 1.2], y=[0.2, 0.2, 0], mode='lines', line=dict(color='red', width=1), showlegend=False))
        
        # --- МЕДИАНА (синяя) ---
        fig.add_trace(go.Scatter(x=[1, 2], y=[3.5, 0], mode='lines', line=dict(color='blue', width=2)))
        fig.add_annotation(x=1, y=-0.2, text="|", showarrow=False, font=dict(color="blue", size=18))
        fig.add_annotation(x=3, y=-0.2, text="|", showarrow=False, font=dict(color="blue", size=18))

        # --- БИССЕКТРИСА (зеленая) ---
        fig.add_trace(go.Scatter(x=[1, 1.5], y=[3.5, 0], mode='lines', line=dict(color='green', width=2)))
        fig.add_annotation(x=0.95, y=3.1, text=")", showarrow=False, textangle=110, font=dict(color="green", size=12))
        fig.add_annotation(x=1.1, y=3.1, text=")", showarrow=False, textangle=70, font=dict(color="green", size=12))

        # --- ТЕКСТОВОЕ ОПИСАНИЕ РЯДОМ (ЛЕГЕНДА) ---
        # Размещаем текст справа от треугольника (x=4.5)
        fig.add_annotation(
            x=4.5, y=3, text="— Высота", 
            showarrow=False, xanchor="left", font=dict(color="red", size=14)
        )
        fig.add_annotation(
            x=4.5, y=2.5, text="— Медиана", 
            showarrow=False, xanchor="left", font=dict(color="blue", size=14)
        )
        fig.add_annotation(
            x=4.5, y=2, text="— Биссектриса", 
            showarrow=False, xanchor="left", font=dict(color="green", size=14)
        )

        # Расширяем диапазон X, чтобы описание влезло
        fig.update_xaxes(range=[-0.5, 8.5])
        fig.update_yaxes(range=[-0.5, 4.5])
    
    elif topic == "Измерение углов":
        # --- Развернутый угол ---
        # Линия проходит через вершину (1, 1)
        fig.add_trace(go.Scatter(
            x=[0, 1, 2], 
            y=[1, 1, 1], 
            mode='lines+markers+text',
            text=["", "180°", ""],
            textposition="top center",
            line=dict(color='indigo', width=3),
            marker=dict(size=[0, 8, 0], color='indigo'),
            name="Развернутый"
        ))
        fig.add_annotation(x=1, y=0.7, text="Развернутый угол", showarrow=False, font=dict(size=12))

        # --- Прямой угол ---
        # Вершина в точке (4, 1), лучи вверх и вправо
        fig.add_trace(go.Scatter(
            x=[4, 4, 5], 
            y=[2.5, 1, 1], 
            mode='lines+markers+text',
            text=["", "90°", ""],
            textposition="bottom left",
            line=dict(color='crimson', width=3),
            marker=dict(size=[0, 8, 0], color='crimson'),
            name="Прямой"
        ))
        
        # Квадратный символ прямого угла
        fig.add_shape(
            type="rect",
            x0=4, y0=1, x1=4.2, y1=1.2,
            line=dict(color="crimson", width=1)
        )
        fig.add_annotation(x=4.5, y=0.7, text="Прямой угол", showarrow=False, font=dict(size=12))

        # Настройка осей для отображения двух фигур
        fig.update_xaxes(range=[-0.5, 6])
        fig.update_yaxes(range=[0, 4])
        
    elif topic == "Равнобедренный треугольник":
        ax, ay, bx, by, cx, cy = 0, 0, 4, 0, 2, 4
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ax], y=[ay, by, cy, ay], mode='lines', line=dict(color='black', width=3)))
        fig.add_trace(go.Scatter(x=[2, 2], y=[4, 0], mode='lines', line=dict(color='blue', width=2)))
        fig.add_annotation(x=0.8, y=2.2, text="//", showarrow=False, textangle=60)
        fig.add_annotation(x=3.2, y=2.2, text="//", showarrow=False, textangle=-60)
        fig.add_annotation(x=5, y=3, text="<b>Свойства:</b><br>— Боковые стороны равны<br>— Медиана = Высота = Биссектриса", showarrow=False, xanchor="left", align="left")
        fig.update_xaxes(range=[-0.5, 9])

    elif topic == "Луч и угол":
        # Отрисовка угла (два луча из одной вершины)
        # Луч 1: из (3,0) горизонтально вправо
        # Луч 2: из (3,0) под углом вверх
        fig.add_trace(go.Scatter(
            x=[5, 3, 4.5], 
            y=[0, 0, 2.5], 
            mode='lines+markers+text', 
            text=["", "вершина", ""],
            textposition="bottom center",
            line=dict(color='indigo', width=3),
            marker=dict(size=[0, 10, 0], color='indigo'),
            name="Угол"
        ))

        # Дуга для обозначения угла (сектор)
        t = np.linspace(0, 0.8, 20) # Параметры для небольшого изгиба
        fig.add_trace(go.Scatter(
            x=3 + 0.5 * np.cos(t),
            y=0.5 * np.sin(t),
            mode='lines',
            line=dict(color='orange', width=2)
        ))

        # Подписи сторон (лучей)
        fig.add_annotation(x=4.2, y=0.2, text="луч 1", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=4, y=1.8, text="луч 2", showarrow=False, font=dict(size=12))

        # Фиксация области видимости вокруг вершины (3,0)
        fig.update_xaxes(range=[2, 6])
        fig.update_yaxes(range=[-1, 4])

    elif topic == "Смежные и вертикальные углы":
        # --- Смежные углы ---
        # Горизонтальная прямая и луч, выходящий вверх
        fig.add_trace(go.Scatter(
            x=[0, 2, 4, 2, 1], 
            y=[1, 1, 1, 1, 3], 
            mode='lines+markers',
            line=dict(color='indigo', width=3),
            marker=dict(size=[0, 8, 0, 0, 0]),
            name="Смежные"
        ))
        fig.add_annotation(x=1.5, y=1.3, text="α", showarrow=False, font=dict(size=18))
        fig.add_annotation(x=2.5, y=1.3, text="β", showarrow=False, font=dict(size=18))
        fig.add_annotation(x=2, y=0.5, text="α + β = 180°", showarrow=False, font=dict(size=14, color="indigo"))

        # --- Вертикальные углы ---
        # Две пересекающиеся прямые в точке (7, 2)
        # Прямая 1
        fig.add_trace(go.Scatter(x=[5, 9], y=[1, 3], mode='lines', line=dict(color='crimson', width=3)))
        # Прямая 2
        fig.add_trace(go.Scatter(x=[5, 9], y=[3, 1], mode='lines', line=dict(color='crimson', width=3)))
        
        # Обозначение равенства дугами или буквами
        fig.add_annotation(x=6.2, y=2, text="1", showarrow=False, font=dict(size=16, color="crimson"))
        fig.add_annotation(x=7.8, y=2, text="1", showarrow=False, font=dict(size=16, color="crimson"))
        fig.add_annotation(x=7, y=2.6, text="2", showarrow=False, font=dict(size=16, color="black"))
        fig.add_annotation(x=7, y=1.4, text="2", showarrow=False, font=dict(size=16, color="black"))
        
        fig.add_annotation(x=7, y=0.5, text="Углы 1 равны, Углы 2 равны", showarrow=False, font=dict(size=14))

        # Настройка осей для размещения двух чертежей
        fig.update_xaxes(range=[-0.5, 9.5])
        fig.update_yaxes(range=[0, 4])

    elif topic == "Окружность":
        import numpy as np
        
        # Параметры окружности
        center_x, center_y = 0, 0
        radius = 3
        
        # Генерируем точки окружности
        t = np.linspace(0, 2*np.pi, 100)
        x_circ = center_x + radius * np.cos(t)
        y_circ = center_y + radius * np.sin(t)
        
        # 1. Отрисовка самой окружности
        fig.add_trace(go.Scatter(
            x=x_circ, y=y_circ, 
            mode='lines', 
            line=dict(color='black', width=3),
            name="Окружность"
        ))
        
        # 2. ДИАМЕТР AB (красный) — проходит СТРОГО через центр (0,0)
        fig.add_trace(go.Scatter(
            x=[-radius, radius], 
            y=[0, 0], 
            mode='lines+markers+text',
            text=["A", "B"],
            textposition=["middle left", "middle right"],
            line=dict(color='crimson', width=3),
            marker=dict(size=8, color='crimson'),
            name="Диаметр"
        ))
        
        # 3. РАДИУС OC (синий) — от центра вверх под углом
        angle = np.pi / 3 # 60 градусов
        fig.add_trace(go.Scatter(
            x=[0, radius * np.cos(angle)], 
            y=[0, radius * np.sin(angle)], 
            mode='lines+markers+text',
            text=["O", "C"],
            textposition=["bottom center", "top right"],
            line=dict(color='blue', width=3),
            name="Радиус"
        ))

        # --- Описание рядом ---
        fig.add_annotation(
            x=4.5, y=2, text="<b>Элементы:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=4.5, y=1.2, text="— Диаметр AB (красный)", 
            showarrow=False, xanchor="left", font=dict(color="crimson", size=14)
        )
        fig.add_annotation(
            x=4.5, y=0.5, text="— Радиус OC (синий)", 
            showarrow=False, xanchor="left", font=dict(color="blue", size=14)
        )
        fig.add_annotation(
            x=4.5, y=-0.2, text="— Центр O (пересечение)", 
            showarrow=False, xanchor="left", font=dict(size=14)
        )

        # Центрирование и фиксация пропорций
        fig.update_xaxes(range=[-4, 10], scaleanchor="y", scaleratio=1)
        fig.update_yaxes(range=[-4, 4])

    elif topic == "Прямоугольный треугольник":
        # Координаты вершин: A(0,0) - прямой угол, B(4,0), C(0,3)
        ax, ay = 0, 0
        bx, by = 4, 0
        cx, cy = 0, 3

        # 1. Отрисовка треугольника
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, ax], y=[ay, by, cy, ay], 
            mode='lines', line=dict(color='black', width=3),
            name="Δ ABC"
        ))

        # 2. Значок ПРЯМОГО УГЛА (красный квадратик в вершине A)
        fig.add_trace(go.Scatter(
            x=[0, 0.3, 0.3, 0], y=[0.3, 0.3, 0, 0], 
            mode='lines', line=dict(color='red', width=2),
            fill="toself", fillcolor="rgba(255, 0, 0, 0.1)",
            showlegend=False
        ))

        # --- Подписи сторон (Катеты и Гипотенуза) ---
        # Катет a (вертикальный)
        fig.add_annotation(x=-0.4, y=1.5, text="Катет <i>a</i>", showarrow=False, textangle=-90, font=dict(color="blue", size=14))
        # Катет b (горизонтальный)
        fig.add_annotation(x=2, y=-0.4, text="Катет <i>b</i>", showarrow=False, font=dict(color="blue", size=14))
        # Гипотенуза c
        fig.add_annotation(x=2.2, y=1.7, text="Гипотенуза <i>c</i>", showarrow=False, textangle=-37, font=dict(color="crimson", size=14, weight="bold"))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=6, y=3, text="<b>Основные свойства:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=6, y=2.2, text="1. ∠A = 90°", 
            showarrow=False, xanchor="left", font=dict(color="red", size=14)
        )
        fig.add_annotation(
            x=6, y=1.7, text="2. Теорема Пифагора:<br>   a² + b² = c²", 
            showarrow=False, xanchor="left", font=dict(size=15, weight="bold")
        )
        fig.add_annotation(
            x=6, y=0.8, text="3. Сумма острых углов:<br>   ∠B + ∠C = 90°", 
            showarrow=False, xanchor="left", font=dict(size=13, color="gray")
        )

        fig.update_xaxes(range=[-1, 12])
        fig.update_yaxes(range=[-1, 4])

    elif topic == "Перпендикулярные прямые":
        # Прямая 1 (горизонтальная)
        fig.add_trace(go.Scatter(x=[-1, 4], y=[1, 1], mode='lines', line=dict(color='indigo')))
        # Прямая 2 (вертикальная)
        fig.add_trace(go.Scatter(x=[1.5, 1.5], y=[-1, 4], mode='lines', line=dict(color='crimson')))
        
        # Значок перпендикулярности (маленький квадрат в точке 1.5, 1)
        # Рисуем уголок: (1.5, 1.3) -> (1.8, 1.3) -> (1.8, 1)
        fig.add_trace(go.Scatter(
            x=[1.5, 1.8, 1.8], 
            y=[1.3, 1.3, 1], 
            mode='lines', 
            line=dict(color='black', width=2),
            showlegend=False
        ))
        
        # Добавим математический символ для наглядности
        fig.add_annotation(x=1.5, y=-0.5, text="a ⊥ b", showarrow=False, font=dict(size=20))
        
        fig.update_xaxes(range=[-1, 4])
        fig.update_yaxes(range=[-1, 4])
    
    elif topic == "Признаки параллельности":
        # Прямая a (сверху, y=3)
        fig.add_trace(go.Scatter(x=[0, 6], y=[3, 3], mode='lines', line=dict(color='indigo', width=3), name="Прямая a"))
        
        # Прямая b (снизу, y=1)
        fig.add_trace(go.Scatter(x=[0, 6], y=[1, 1], mode='lines', line=dict(color='indigo', width=3), name="Прямая b"))
        
        # Секущая c (проходит через (2,1) и (4,3))
        fig.add_trace(go.Scatter(x=[1, 5], y=[0, 4], mode='lines', line=dict(color='gray', width=2, dash='dot'), name="Секущая c"))

        # --- Точные координаты углов ---
        # Накрест лежащие: ∠1 (справа-сверху от пересечения) и ∠2 (слева-снизу)
        fig.add_annotation(x=4.4, y=3.3, text="∠1", showarrow=False, font=dict(size=16, color="crimson"))
        fig.add_annotation(x=1.6, y=0.7, text="∠2", showarrow=False, font=dict(size=16, color="crimson"))

        # Соответственные: ∠3 (на нижней прямой в той же позиции, что ∠1 на верхней)
        fig.add_annotation(x=2.4, y=1.3, text="∠3", showarrow=False, font=dict(size=16, color="green"))

        # Односторонние: ∠4 (внутренний угол рядом с ∠2)
        fig.add_annotation(x=2.3, y=0.7, text="∠4", showarrow=False, font=dict(size=16, color="orange"))

        # --- Описание признаков ---
        fig.add_annotation(
            x=7, y=3.5, text="<b>Прямые параллельны (a || b), если:</b>", 
            showarrow=False, xanchor="left", font=dict(size=14)
        )
        fig.add_annotation(
            x=7, y=2.5, text="1. Накрест лежащие углы равны (∠1 = ∠2)", 
            showarrow=False, xanchor="left", font=dict(color="crimson", size=13)
        )
        fig.add_annotation(
            x=7, y=1.8, text="2. Соответственные углы равны (∠1 = ∠3)", 
            showarrow=False, xanchor="left", font=dict(color="green", size=13)
        )
        fig.add_annotation(
            x=7, y=1.1, text="3. Сумма односторонних углов = 180° (∠3 + ∠1)", 
            showarrow=False, xanchor="left", font=dict(color="orange", size=13)
        )

        fig.update_xaxes(range=[-0.5, 13]) # Увеличил отступ для текста
        fig.update_yaxes(range=[-0.5, 4.5])

    elif topic == "Аксиома параллельных прямых":
        # 1. Основная прямая a (сплошная синяя)
        fig.add_trace(go.Scatter(
            x=[0.5, 6.5], y=[1, 1], 
            mode='lines', 
            line=dict(color='indigo', width=3),
            name="Прямая a"
        ))
        fig.add_annotation(x=6.3, y=0.7, text="a", showarrow=False, font=dict(size=18, style="italic"))

        # 2. Единственная параллельная прямая b (красный пунктир)
        fig.add_trace(go.Scatter(
            x=[0.5, 6.5], y=[3, 3], 
            mode='lines', 
            line=dict(color='crimson', width=2, dash='dashdot'),
            name="Прямая b"
        ))
        fig.add_annotation(x=6.3, y=3.3, text="b", showarrow=False, font=dict(size=18, color="crimson", style="italic"))

        # 3. Точка M (3, 3) - лежит на прямой b
        mx, my = 3, 3
        fig.add_trace(go.Scatter(
            x=[mx], y=[my], 
            mode='markers+text',
            text=["M"],
            textposition="top center",
            marker=dict(size=10, color='black', line=dict(width=2, color='white')),
            showlegend=False
        ))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=7.5, y=3, text="<b>Аксиома Евклида:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=7.5, y=2.2, text="Через точку <b>M</b>, не лежащую на прямой <b>a</b>,", 
            showarrow=False, xanchor="left", font=dict(size=14)
        )
        fig.add_annotation(
            x=7.5, y=1.7, text="можно провести <i>только одну</i> прямую <b>b</b>,", 
            showarrow=False, xanchor="left", font=dict(size=14)
        )
        fig.add_annotation(
            x=7.5, y=1.2, text="такую, что <b>b || a</b>.", 
            showarrow=False, xanchor="left", font=dict(size=14, color="crimson")
        )

        # Настройка лимитов осей
        fig.update_xaxes(range=[-0.5, 14])
        fig.update_yaxes(range=[0, 4.5])

    elif topic == "Углы при параллельных и секущей":
        # Две параллельные прямые a и b
        fig.add_trace(go.Scatter(x=[0, 6], y=[3, 3], mode='lines', line=dict(color='indigo', width=3), name="Прямая a"))
        fig.add_trace(go.Scatter(x=[0, 6], y=[1, 1], mode='lines', line=dict(color='indigo', width=3), name="Прямая b"))
        
        # Секущая c (проходит через (2,1) и (4,3))
        fig.add_trace(go.Scatter(x=[1, 5], y=[0, 4], mode='lines', line=dict(color='black', width=2), name="Секущая c"))

        # --- Нумерация всех 8 углов ---
        # Углы при верхней прямой (центр в точке 4, 3)
        fig.add_annotation(x=3.6, y=3.3, text="1", showarrow=False, font=dict(size=14, color="blue", weight="bold"))
        fig.add_annotation(x=4.4, y=3.3, text="2", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=4.4, y=2.7, text="3", showarrow=False, font=dict(size=14, color="blue", weight="bold"))
        fig.add_annotation(x=3.6, y=2.7, text="4", showarrow=False, font=dict(size=14))

        # Углы при нижней прямой (центр в точке 2, 1)
        fig.add_annotation(x=1.6, y=1.3, text="5", showarrow=False, font=dict(size=14, color="blue", weight="bold"))
        fig.add_annotation(x=2.4, y=1.3, text="6", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=2.4, y=0.7, text="7", showarrow=False, font=dict(size=14, color="blue", weight="bold"))
        fig.add_annotation(x=1.6, y=0.7, text="8", showarrow=False, font=dict(size=14))

        # --- Легенда/Классификация справа ---
        descriptions = [
            ("<b>Накрест лежащие:</b>", "black"),
            ("3 и 5, 4 и 6 (равны)", "blue"),
            ("<b>Соответственные:</b>", "black"),
            ("1 и 5, 2 и 6... (равны)", "green"),
            ("<b>Односторонние:</b>", "black"),
            ("4 и 5, 3 и 6 (сумма 180°)", "orange")
        ]
        
        for i, (txt, clr) in enumerate(descriptions):
            fig.add_annotation(
                x=7, y=3.5 - (i * 0.5), text=txt, 
                showarrow=False, xanchor="left", font=dict(color=clr, size=13)
            )

        fig.update_xaxes(range=[-0.5, 13])
        fig.update_yaxes(range=[-0.5, 4.5])
    
    elif topic == "Сумма углов треугольника":
        # Координаты вершин: A(0,0), B(5,0), C(1.5,3.5)
        ax, ay = 0, 0
        bx, by = 5, 0
        cx, cy = 1.5, 3.5

        # 1. Основной треугольник
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, ax], y=[ay, by, cy, ay], 
            mode='lines', line=dict(color='black', width=3),
            name="Δ ABC"
        ))

        # --- Обозначение углов внутри треугольника ---
        # Угол A (синий)
        fig.add_annotation(x=0.5, y=0.3, text="∠1", showarrow=False, font=dict(color="blue", size=14, weight="bold"))
        # Угол B (зеленый)
        fig.add_annotation(x=4.2, y=0.3, text="∠2", showarrow=False, font=dict(color="green", size=14, weight="bold"))
        # Угол C (оранжевый)
        fig.add_annotation(x=1.5, y=2.8, text="∠3", showarrow=False, font=dict(color="orange", size=14, weight="bold"))
    
    elif topic == "Внешний угол":
        # Координаты вершин: A(0,0), B(4,0), C(1,3)
        ax, ay = 0, 0
        bx, by = 4, 0
        cx, cy = 1, 3
        
        # 1. Стороны треугольника (AC и BC)
        fig.add_trace(go.Scatter(x=[ax, cx, bx], y=[ay, cy, by], 
                                 mode='lines', line=dict(color='black', width=3), showlegend=False))
        
        # 2. Основание AB с продолжением вправо (для образования внешнего угла)
        fig.add_trace(go.Scatter(x=[ax, 6], y=[ay, ay], 
                                 mode='lines', line=dict(color='black', width=3), name="Основание с продолжением"))

        # --- Обозначение внутренних углов ---
        # Угол A (∠1)
        fig.add_annotation(x=0.6, y=0.3, text="∠1", showarrow=False, font=dict(color="blue", size=14, weight="bold"))
        # Угол C (∠2)
        fig.add_annotation(x=1.1, y=2.5, text="∠2", showarrow=False, font=dict(color="green", size=14, weight="bold"))
        # Смежный внутренний угол B (∠3)
        fig.add_annotation(x=3.4, y=0.3, text="∠3", showarrow=False, font=dict(color="gray", size=12))

        # --- ВНЕШНИЙ УГОЛ (∠4) ---
        fig.add_annotation(x=4.6, y=0.4, text="∠4", showarrow=False, 
                           font=dict(color="crimson", size=18, weight="bold"))
        # Дуга внешнего угла (схематично)
        fig.add_trace(go.Scatter(x=[4.5, 4.7, 4.5], y=[0.1, 0.4, 0.7], 
                                 mode='lines', line=dict(color='crimson', width=2), showlegend=False))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=7, y=3, text="<b>Свойство внешнего угла:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=7, y=2.2, text="∠4 = ∠1 + ∠2", 
            showarrow=False, xanchor="left", font=dict(size=20, color="crimson", weight="bold")
        )
        fig.add_annotation(
            x=7, y=1.2, text="Внешний угол равен сумме двух<br>внутренних углов треугольника,<br>не смежных с ним.", 
            showarrow=False, xanchor="left", font=dict(size=13, color="black")
        )

        fig.update_xaxes(range=[-0.5, 13])
        fig.update_yaxes(range=[-0.5, 4.5])

    elif topic == "Многоугольники":
        # Координаты вершин выпуклого пятиугольника
        px = [1, 4, 5, 3, 0, 1]
        py = [0, 0, 2, 4, 3, 0]
        
        # 1. Отрисовка контура многоугольника
        fig.add_trace(go.Scatter(
            x=px, y=py, 
            mode='lines+markers', 
            line=dict(color='indigo', width=3),
            marker=dict(size=10, color='black'),
            name="Многоугольник"
        ))

        # 2. ДИАГОНАЛИ (пунктирные линии из одной вершины)
        # Проведем диагонали из вершины (0, 3) к другим вершинам
        fig.add_trace(go.Scatter(
            x=[0, 4, None, 0, 5], 
            y=[3, 0, None, 3, 2], 
            mode='lines', 
            line=dict(color='gray', width=1.5, dash='dot'),
            name="Диагонали"
        ))

        # --- Обозначение элементов ---
        # Вершины
        vertices = ['A', 'B', 'C', 'D', 'E']
        fig.add_trace(go.Scatter(
            x=[1, 4, 5.3, 3, -0.3], 
            y=[-0.3, -0.3, 2, 4.3, 3], 
            mode='text',
            text=vertices,
            textfont=dict(size=16, weight="bold"),
            showlegend=False
        ))

        # Внутренний угол (дуга схематично у вершины A)
        fig.add_annotation(x=1.3, y=0.4, text="α", showarrow=False, font=dict(color="orange", size=18))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=7, y=3.5, text="<b>Элементы и свойства:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=7, y=2.7, text="— n - число вершин (сторон)", 
            showarrow=False, xanchor="left", font=dict(size=14)
        )
        fig.add_annotation(
            x=7, y=2.0, text="— Сумма внутренних углов:<br>   <b>S = (n - 2) × 180°</b>", 
            showarrow=False, xanchor="left", font=dict(color="indigo", size=15)
        )
        fig.add_annotation(
            x=7, y=1.0, text="— Количество диагоналей:<br>   d = n(n - 3) / 2", 
            showarrow=False, xanchor="left", font=dict(size=14, color="gray")
        )

        fig.update_xaxes(range=[-1, 14])
        fig.update_yaxes(range=[-1, 5])

    elif topic == "Параллелограмм":
        # Вершины параллелограмма: A(0,0), B(4,0), C(5,3), D(1,3)
        ax, ay = 0, 0
        bx, by = 4, 0
        cx, cy = 5, 3
        dx, dy = 1, 3

        # 1. Отрисовка контура
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, dx, ax], y=[ay, by, cy, dy, ay], 
            mode='lines', line=dict(color='indigo', width=3),
            name="Параллелограмм"
        ))

        # 2. ДИАГОНАЛИ (пунктирные)
        # AC
        fig.add_trace(go.Scatter(x=[ax, cx], y=[ay, cy], mode='lines', 
                                 line=dict(color='gray', width=1.5, dash='dash'), showlegend=False))
        # BD
        fig.add_trace(go.Scatter(x=[bx, dx], y=[by, dy], mode='lines', 
                                 line=dict(color='gray', width=1.5, dash='dash'), showlegend=False))

        # 3. Точка пересечения диагоналей O (2.5, 1.5)
        fig.add_trace(go.Scatter(x=[2.5], y=[1.5], mode='markers+text', 
                                 text=["O"], textposition="top center",
                                 marker=dict(size=8, color='black'), showlegend=False))

        # --- Обозначение равенства сторон ---
        # Боковые стороны (одна черта)
        fig.add_annotation(x=0.4, y=1.5, text="/", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=4.6, y=1.5, text="/", showarrow=False, font=dict(size=14))
        # Основания (две черты)
        fig.add_annotation(x=2, y=-0.2, text="//", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=3, y=3.2, text="//", showarrow=False, font=dict(size=12))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=6.5, y=3, text="<b>Свойства:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=6.5, y=2.2, text="1. Противоположные стороны равны<br>   и параллельны (AB || CD, AD || BC)", 
            showarrow=False, xanchor="left", font=dict(color="indigo", size=13)
        )
        fig.add_annotation(
            x=6.5, y=1.3, text="2. Диагонали точкой пересечения (O)<br>   делятся пополам", 
            showarrow=False, xanchor="left", font=dict(color="black", size=13)
        )
        fig.add_annotation(
            x=6.5, y=0.5, text="3. Противоположные углы равны", 
            showarrow=False, xanchor="left", font=dict(color="gray", size=13)
        )

        fig.update_xaxes(range=[-0.5, 13])
        fig.update_yaxes(range=[-1, 4.5])
    
    elif topic == "Трапеция":
        # Вершины трапеции: A(0,0), B(6,0), C(4,3), D(1,3)
        ax, ay = 0, 0
        bx, by = 6, 0
        cx, cy = 4, 3
        dx, dy = 1, 3

        # 1. Отрисовка контура трапеции
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, dx, ax], y=[ay, by, cy, dy, ay], 
            mode='lines', line=dict(color='indigo', width=3),
            name="Трапеция"
        ))

        # 2. ВЫСОТА h (красная, пунктирная)
        fig.add_trace(go.Scatter(
            x=[1, 1], y=[3, 0], 
            mode='lines', line=dict(color='red', width=2, dash='dash'),
            name="Высота h"
        ))
        # Значок прямого угла у высоты
        fig.add_trace(go.Scatter(x=[1, 1.2, 1.2], y=[0.2, 0.2, 0], mode='lines', line=dict(color='red', width=1), showlegend=False))

        # 3. СРЕДНЯЯ ЛИНИЯ m (зеленая)
        # Середина AD: (0.5, 1.5), Середина BC: (5, 1.5)
        fig.add_trace(go.Scatter(
            x=[0.5, 5], y=[1.5, 1.5], 
            mode='lines', line=dict(color='green', width=2),
            name="Средняя линия m"
        ))

        # --- Подписи оснований ---
        fig.add_annotation(x=2.5, y=3.3, text="Основание <b>b</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=3, y=-0.4, text="Основание <b>a</b>", showarrow=False, font=dict(size=14))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=7.5, y=3.5, text="<b>Элементы и свойства:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=7.5, y=2.7, text="— Основания параллельны (a || b)", 
            showarrow=False, xanchor="left", font=dict(color="indigo", size=13)
        )
        fig.add_annotation(
            x=7.5, y=2.0, text="— Средняя линия m = (a + b) / 2", 
            showarrow=False, xanchor="left", font=dict(color="green", size=14, weight="bold")
        )
        fig.add_annotation(
            x=7.5, y=1.2, text="— Площадь S = m × h", 
            showarrow=False, xanchor="left", font=dict(color="red", size=14, weight="bold")
        )
        fig.add_annotation(
            x=7.5, y=0.5, text="— Сумма углов при боковой<br>   стороне равна 180°", 
            showarrow=False, xanchor="left", font=dict(color="gray", size=12)
        )

        fig.update_xaxes(range=[-0.5, 15])
        fig.update_yaxes(range=[-1, 4.5])
    
    elif topic == "Прямоугольник, ромб, квадрат":
        from plotly.subplots import make_subplots
        
        # Создаем 3 подграфика в одну строку
        fig = make_subplots(rows=1, cols=3, 
                            subplot_titles=("Прямоугольник", "Ромб", "Квадрат"),
                            horizontal_spacing=0.1)

        # --- 1. ПРЯМОУГОЛЬНИК (Все углы 90°, диагонали равны) ---
        fig.add_trace(go.Scatter(x=[0, 3, 3, 0, 0], y=[0, 0, 2, 2, 0], 
                                 mode='lines', line=dict(color='blue', width=3), name="Прямоугольник"), row=1, col=1)
        # Диагонали
        fig.add_trace(go.Scatter(x=[0, 3, None, 0, 3], y=[0, 2, None, 2, 0], 
                                 mode='lines', line=dict(color='gray', width=1, dash='dot'), showlegend=False), row=1, col=1)

        # --- 2. РОМБ (Все стороны равны, диагонали перпендикулярны) ---
        fig.add_trace(go.Scatter(x=[1.5, 3, 1.5, 0, 1.5], y=[0, 1.5, 3, 1.5, 0], 
                                 mode='lines', line=dict(color='crimson', width=3), name="Ромб"), row=1, col=2)
        # Диагонали
        fig.add_trace(go.Scatter(x=[1.5, 1.5, None, 0, 3], y=[0, 3, None, 1.5, 1.5], 
                                 mode='lines', line=dict(color='gray', width=1, dash='dot'), showlegend=False), row=1, col=2)
        # Квадратик прямого угла в центре ромба
        fig.add_trace(go.Scatter(x=[1.5, 1.7, 1.7], y=[1.7, 1.7, 1.5], mode='lines', line=dict(color='black', width=1), showlegend=False), row=1, col=2)

        # --- 3. КВАДРАТ (Идеал: углы 90° + стороны равны) ---
        fig.add_trace(go.Scatter(x=[0, 2, 2, 0, 0], y=[0, 0, 2, 2, 0], 
                                 mode='lines', line=dict(color='indigo', width=3), name="Квадрат"), row=1, col=3)
        # Диагонали
        fig.add_trace(go.Scatter(x=[0, 2, None, 0, 2], y=[0, 2, None, 2, 0], 
                                 mode='lines', line=dict(color='gray', width=1, dash='dot'), showlegend=False), row=1, col=3)

        # --- ОБЩЕЕ ОПИСАНИЕ (Аннотации под фигурами) ---
        fig.add_annotation(x=1.5, y=-0.5, text="d₁ = d₂", showarrow=False, xref="x1", yref="y1", font=dict(color="blue"))
        fig.add_annotation(x=1.5, y=-0.5, text="d₁ ⊥ d₂, AB=BC", showarrow=False, xref="x2", yref="y2", font=dict(color="crimson"))
        fig.add_annotation(x=1, y=-0.5, text="Все свойства сразу", showarrow=False, xref="x3", yref="y3", font=dict(color="indigo"))

        fig.update_layout(showlegend=False, height=400)
        fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)

    elif topic == "Осевая и центральная симметрия":
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=1, cols=2, 
                            subplot_titles=("Осевая (зеркальная)", "Центральная (отн. точки)"),
                            horizontal_spacing=0.15)

        # --- 1. ОСЕВАЯ СИММЕТРИЯ ---
        # Линия симметрии (ось Y)
        fig.add_trace(go.Scatter(x=[0, 0], y=[-1, 3], mode='lines', 
                                 line=dict(color='black', width=2, dash='dash'), name="Ось"), row=1, col=1)
        
        # Оригинал (Синий)
        fig.add_trace(go.Scatter(x=[0.5, 2, 0.5, 0.5], y=[0.5, 1, 2, 0.5], 
                                 mode='lines+markers', line=dict(color='blue', width=2), name="Фигура"), row=1, col=1)
        # Образ (Красный пунктир - зеркальное отражение x -> -x)
        fig.add_trace(go.Scatter(x=[-0.5, -2, -0.5, -0.5], y=[0.5, 1, 2, 0.5], 
                                 mode='lines+markers', line=dict(color='crimson', width=2, dash='dot'), name="Образ"), row=1, col=1)

        # --- 2. ЦЕНТРАЛЬНАЯ СИММЕТРИЯ ---
        # Центр O (0,0)
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', text=["O"], textposition="bottom right",
                                 marker=dict(size=10, color='black', symbol='x'), showlegend=False), row=1, col=2)
        
        # Оригинал (Синий)
        # Точки: (1, 0.5), (2.5, 0.5), (1.5, 2)
        orig_x, orig_y = [1, 2.5, 1.5, 1], [0.5, 0.5, 2, 0.5]
        fig.add_trace(go.Scatter(x=orig_x, y=orig_y, 
                                 mode='lines+markers', line=dict(color='blue', width=2), showlegend=False), row=1, col=2)
        
        # Образ (Красный пунктир - инверсия x -> -x, y -> -y)
        im_x = [-x for x in orig_x]
        im_y = [-y for y in orig_y]
        fig.add_trace(go.Scatter(x=im_x, y=im_y, 
                                 mode='lines+markers', line=dict(color='crimson', width=2, dash='dot'), showlegend=False), row=1, col=2)
        
        # Тонкие линии связи через центр для наглядности
        for x, y in zip([1, 2.5, 1.5], [0.5, 0.5, 2]):
            fig.add_trace(go.Scatter(x=[x, -x], y=[y, -y], mode='lines', 
                                     line=dict(color='gray', width=0.5, dash='dash'), showlegend=False), row=1, col=2)

        # Тонкая настройка сетки
        fig.update_xaxes(range=[-3, 3], zeroline=True, zerolinewidth=1, zerolinecolor='LightGray', row=1, col=1)
        fig.update_yaxes(range=[-1, 3], row=1, col=1)
        fig.update_xaxes(range=[-3, 3], zeroline=True, zerolinewidth=1, zerolinecolor='LightGray', row=1, col=2)
        fig.update_yaxes(range=[-3, 3], row=1, col=2)

        fig.update_layout(height=400, showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

    elif topic == "Свойства площадей":
        # Координаты вершин базовой фигуры (параллелограмм)
        # A(0,0), B(3,0), C(4,2), D(1,2)
        base_x = [0, 3, 4, 1, 0]
        base_y = [0, 0, 2, 2, 0]
        
        # 1. Первая фигура (Синяя)
        fig.add_trace(go.Scatter(
            x=base_x, y=base_y, 
            fill="toself", fillcolor="rgba(0, 0, 255, 0.2)",
            mode='lines+markers', line=dict(color='blue', width=3),
            name="Фигура F1"
        ))
        fig.add_annotation(x=2, y=1, text="S₁", showarrow=False, font=dict(size=20, color="blue", weight="bold"))

        # 2. Вторая фигура (Равная первой, сдвинута вправо на 6 единиц)
        shift = 6
        fig.add_trace(go.Scatter(
            x=[x + shift for x in base_x], y=base_y, 
            fill="toself", fillcolor="rgba(255, 0, 0, 0.1)",
            mode='lines+markers', line=dict(color='crimson', width=3, dash='dash'),
            name="Фигура F2"
        ))
        fig.add_annotation(x=2 + shift, y=1, text="S₂", showarrow=False, font=dict(size=20, color="crimson", weight="bold"))

        # --- Текстовое описание свойств ---
        fig.add_annotation(
            x=0, y=3.5, text="<b>Свойства площадей:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=0, y=2.8, text="1. Равные фигуры имеют равные площади (S₁ = S₂)", 
            showarrow=False, xanchor="left", font=dict(size=14, color="indigo")
        )
        fig.add_annotation(
            x=11, y=2.2, text="Если F₁ = F₂, то S(F₁) = S(F₂)", 
            showarrow=False, xanchor="right", font=dict(size=14, style="italic")
        )
        fig.add_annotation(
            x=0, y=2.2, text="2. Если фигура составлена из нескольких частей,<br>её площадь равна сумме площадей этих частей.", 
            showarrow=False, xanchor="left", font=dict(size=13, color="gray")
        )

        fig.update_xaxes(range=[-1, 12], showgrid=False, zeroline=True)
        fig.update_yaxes(range=[-1, 4.5], showgrid=False)
        fig.update_layout(height=450, showlegend=False)

    elif topic == "Площадь квадрата и прямоугольника":
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=1, cols=2, 
                            subplot_titles=("Прямоугольник (S = a · b)", "Квадрат (S = a²)"),
                            horizontal_spacing=0.2)

        # --- 1. ПРЯМОУГОЛЬНИК (3x2) ---
        # Сетка внутри
        for i in range(4): 
            fig.add_trace(go.Scatter(x=[i, i], y=[0, 2], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=1)
        for j in range(3): 
            fig.add_trace(go.Scatter(x=[0, 3], y=[j, j], mode='lines', line=dict(color='lightgray', width=1), showlegend=False), row=1, col=1)

        fig.add_trace(go.Scatter(x=[0, 3, 3, 0, 0], y=[0, 0, 2, 2, 0], 
                                 fill="toself", fillcolor="rgba(0, 0, 255, 0.1)",
                                 mode='lines', line=dict(color='blue', width=3)), row=1, col=1)
        
        # ИСПРАВЛЕНО: textangle вынесен из font
        fig.add_annotation(x=1.5, y=-0.3, text="a = 3", showarrow=False, row=1, col=1, font=dict(size=14))
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

        fig.update_xaxes(range=[-1, 4], showticklabels=False, showgrid=False, zeroline=False)
        fig.update_yaxes(range=[-1, 3], showticklabels=False, showgrid=False, zeroline=False)
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Площадь параллелограмма":
        # Координаты: A(1,0), B(5,0), C(6,3), D(2,3)
        ax, ay = 1, 0
        bx, by = 5, 0
        cx, cy = 6, 3
        dx, dy = 2, 3

        # 1. Контур параллелограмма
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, dx, ax], y=[ay, by, cy, dy, ay], 
            fill="toself", fillcolor="rgba(106, 90, 205, 0.1)",
            mode='lines', line=dict(color='indigo', width=3),
            name="Параллелограмм"
        ))

        # 2. ВЫСОТА h (проведенная из D к стороне AB)
        fig.add_trace(go.Scatter(
            x=[2, 2], y=[3, 0], 
            mode='lines', line=dict(color='red', width=2, dash='dash'),
            name="Высота h"
        ))
        
        # Значок прямого угла у высоты
        fig.add_trace(go.Scatter(x=[2, 2.2, 2.2], y=[0.2, 0.2, 0], 
                                 mode='lines', line=dict(color='red', width=1), showlegend=False))

        # --- Подписи элементов ---
        # Основание a
        fig.add_annotation(x=3, y=-0.4, text="Основание <b>a</b>", showarrow=False, font=dict(size=14))
        # Высота h
        fig.add_annotation(x=1.7, y=1.5, text="h", showarrow=False, font=dict(color="red", size=16, weight="bold"))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=8, y=3, text="<b>Формула площади:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=8, y=2.2, text="S = a · h", 
            showarrow=False, xanchor="left", font=dict(size=22, color="indigo", weight="bold")
        )
        fig.add_annotation(
            x=8, y=1.2, text="Площадь параллелограмма равна<br>произведению его основания<br>на высоту.", 
            showarrow=False, xanchor="left", font=dict(size=13)
        )

        fig.update_xaxes(range=[0, 14])
        fig.update_yaxes(range=[-1, 4.5])
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Площадь треугольника":
        # Вершины треугольника: A(1,0), B(6,0), C(2,3)
        ax, ay = 1, 0
        bx, by = 6, 0
        cx, cy = 2, 3

        # 1. Основной треугольник (Синий)
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, ax], y=[ay, by, cy, ay], 
            fill="toself", fillcolor="rgba(0, 0, 255, 0.1)",
            mode='lines+markers', line=dict(color='blue', width=3),
            name="Δ ABC"
        ))

        # 2. Достраивание до параллелограмма (Пунктир)
        # Точка D = C + (B - A) = (2+5, 3+0) = (7, 3)
        fig.add_trace(go.Scatter(
            x=[bx, 7, cx], y=[by, 3, cy], 
            mode='lines', line=dict(color='gray', width=1.5, dash='dot'),
            showlegend=False
        ))

        # 3. ВЫСОТА h (из вершины C к стороне AB)
        fig.add_trace(go.Scatter(
            x=[2, 2], y=[3, 0], 
            mode='lines', line=dict(color='red', width=2, dash='dash'),
            name="Высота h"
        ))
        # Значок прямого угла
        fig.add_trace(go.Scatter(x=[2, 2.2, 2.2], y=[0.2, 0.2, 0], 
                                 mode='lines', line=dict(color='red', width=1), showlegend=False))

        # --- Подписи элементов ---
        fig.add_annotation(x=3.5, y=-0.4, text="Основание <b>a</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=1.7, y=1.5, text="h", showarrow=False, font=dict(color="red", size=16, weight="bold"))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=8.5, y=3, text="<b>Формула площади:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=8.5, y=2.2, text="S = ½ · a · h", 
            showarrow=False, xanchor="left", font=dict(size=22, color="blue", weight="bold")
        )
        fig.add_annotation(
            x=8.5, y=1.2, text="Площадь треугольника равна<br>половине произведения его<br>основания на высоту.", 
            showarrow=False, xanchor="left", font=dict(size=13)
        )

        fig.update_xaxes(range=[0, 15])
        fig.update_yaxes(range=[-1, 4.5])
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Площадь трапеции":
        # Вершины трапеции: A(0,0), B(7,0), C(5,3), D(1,3)
        ax, ay = 0, 0
        bx, by = 7, 0
        cx, cy = 5, 3
        dx, dy = 1, 3

        # 1. Контур трапеции (Индиго)
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, dx, ax], y=[ay, by, cy, dy, ay], 
            fill="toself", fillcolor="rgba(75, 0, 130, 0.1)",
            mode='lines', line=dict(color='indigo', width=3),
            name="Трапеция"
        ))

        # 2. ВЫСОТА h (из вершины D к основанию AB)
        fig.add_trace(go.Scatter(
            x=[1, 1], y=[3, 0], 
            mode='lines', line=dict(color='red', width=2, dash='dash'),
            name="Высота h"
        ))
        # Значок прямого угла
        fig.add_trace(go.Scatter(x=[1, 1.2, 1.2], y=[0.2, 0.2, 0], 
                                 mode='lines', line=dict(color='red', width=1), showlegend=False))

        # 3. СРЕДНЯЯ ЛИНИЯ m (Зеленая, пунктир)
        # Середина AD (0.5, 1.5), Середина BC (6, 1.5)
        fig.add_trace(go.Scatter(
            x=[0.5, 6], y=[1.5, 1.5], 
            mode='lines', line=dict(color='green', width=2, dash='dot'),
            name="Средняя линия m"
        ))

        # --- Подписи оснований и элементов ---
        fig.add_annotation(x=3, y=3.3, text="Основание <b>b</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=3.5, y=-0.4, text="Основание <b>a</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=0.7, y=1.5, text="h", showarrow=False, font=dict(color="red", size=16, weight="bold"))
        fig.add_annotation(x=3.2, y=1.2, text="m", showarrow=False, font=dict(color="green", size=14))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=9, y=3, text="<b>Формулы площади:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=9, y=2.2, text="S = ½ · (a + b) · h", 
            showarrow=False, xanchor="left", font=dict(size=20, color="indigo", weight="bold")
        )
        fig.add_annotation(
            x=9, y=1.2, text="S = m · h", 
            showarrow=False, xanchor="left", font=dict(size=18, color="green", weight="bold")
        )
        fig.add_annotation(
            x=9, y=0.2, text="где <i>m</i> — средняя линия.", 
            showarrow=False, xanchor="left", font=dict(size=12, color="gray")
        )

        fig.update_xaxes(range=[-0.5, 16])
        fig.update_yaxes(range=[-1, 4.5])
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Определение подобия":
        # Координаты первого треугольника (малый)
        x1, y1 = [0.5, 2.5, 1, 0.5], [0.5, 0.5, 2, 0.5]
        # Координаты второго треугольника (подобный, k=2)
        # Сдвиг по x на 5 единиц
        k = 2
        shift = 5
        x2 = [x * k + shift for x in x1]
        y2 = [y * k for y in y1]

        # 1. Отрисовка треугольника F1 (Синий)
        fig.add_trace(go.Scatter(x=x1, y=y1, fill="toself", fillcolor="rgba(0, 0, 255, 0.1)",
                                 mode='lines+markers', line=dict(color='blue', width=2), name="F1"))
        fig.add_annotation(x=1.3, y=1, text="F₁", showarrow=False, font=dict(size=18, color="blue"))

        # 2. Отрисовка треугольника F2 (Красный)
        fig.add_trace(go.Scatter(x=x2, y=y2, fill="toself", fillcolor="rgba(255, 0, 0, 0.1)",
                                 mode='lines+markers', line=dict(color='crimson', width=2), name="F2"))
        fig.add_annotation(x=1.3*k + shift, y=1*k, text="F₂", showarrow=False, font=dict(size=18, color="crimson"))

        # --- Обозначение сторон для понимания пропорции ---
        # Сторона малого треугольника
        fig.add_annotation(x=1.5, y=0.2, text="a", showarrow=False, font=dict(size=12))
        # Сторона большого треугольника
        fig.add_annotation(x=1.5*k + shift, y=0.2*k, text="ka", showarrow=False, font=dict(size=14, weight="bold"))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=12, y=3.5, text="<b>Подобные фигуры:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=12, y=2.8, text="1. Соответственные углы равны", 
            showarrow=False, xanchor="left", font=dict(size=13)
        )
        fig.add_annotation(
            x=12, y=2.2, text="2. Стороны пропорциональны:<br>   <b>a' / a = b' / b = c' / c = k</b>", 
            showarrow=False, xanchor="left", font=dict(size=14, color="indigo")
        )
        fig.add_annotation(
            x=12, y=1.2, text="k — коэффициент подобия", 
            showarrow=False, xanchor="left", font=dict(size=12, style="italic")
        )

        fig.update_xaxes(range=[-1, 22], showticklabels=False, showgrid=False, zeroline=True)
        fig.update_yaxes(range=[-1, 5], showticklabels=False, showgrid=False)
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Признаки подобия":
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=1, cols=3, 
                            subplot_titles=("I признак (по 2 углам)", "II признак (по 2 сторонам и ∠)", "III признак (по 3 сторонам)"),
                            horizontal_spacing=0.1)

        # Функция для создания треугольника
        def get_tri(x_shift, scale=1):
            return [0+x_shift, 1.5*scale+x_shift, 0.5*scale+x_shift, 0+x_shift], [0, 0, 1.5*scale, 0]

        # --- 1. ПЕРВЫЙ ПРИЗНАК (Углы α и β) ---
        x1, y1 = get_tri(0, 0.8)
        x2, y2 = get_tri(2, 1.2)
        fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines', line=dict(color='blue', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', line=dict(color='crimson', width=2)), row=1, col=1)
        # Обозначение углов
        fig.add_annotation(x=0.2, y=0.15, text="α", showarrow=False, row=1, col=1, font=dict(color="orange"))
        fig.add_annotation(x=2.2, y=0.15, text="α", showarrow=False, row=1, col=1, font=dict(color="orange"))
        fig.add_annotation(x=1, y=0.15, text="β", showarrow=False, row=1, col=1, font=dict(color="green"))
        fig.add_annotation(x=3.5, y=0.15, text="β", showarrow=False, row=1, col=1, font=dict(color="green"))

        # --- 2. ВТОРОЙ ПРИЗНАК (Стороны a, b и угол γ) ---
        x3, y3 = get_tri(0, 0.8)
        x4, y4 = get_tri(2.5, 1.2)
        fig.add_trace(go.Scatter(x=x3, y=y3, mode='lines', line=dict(color='blue', width=2)), row=1, col=2)
        fig.add_trace(go.Scatter(x=x4, y=y4, mode='lines', line=dict(color='crimson', width=2)), row=1, col=2)
        # Подписи сторон
        fig.add_annotation(x=0.4, y=-0.2, text="a", showarrow=False, row=1, col=2)
        fig.add_annotation(x=3.2, y=-0.2, text="ka", showarrow=False, row=1, col=2)
        fig.add_annotation(x=0.1, y=0.4, text="b", showarrow=False, row=1, col=2, textangle=-70)
        fig.add_annotation(x=2.6, y=0.7, text="kb", showarrow=False, row=1, col=2, textangle=-70)

        # --- 3. ТРЕТИЙ ПРИЗНАК (Три стороны) ---
        x5, y5 = get_tri(0, 0.8)
        x6, y6 = get_tri(2.5, 1.2)
        fig.add_trace(go.Scatter(x=x5, y=y5, mode='lines', line=dict(color='blue', width=2)), row=1, col=3)
        fig.add_trace(go.Scatter(x=x6, y=y6, mode='lines', line=dict(color='crimson', width=2)), row=1, col=3)
        fig.add_annotation(x=1.2, y=1.2, text="a, b, c", showarrow=False, row=1, col=3, font=dict(size=10))
        fig.add_annotation(x=4, y=1.8, text="ka, kb, kc", showarrow=False, row=1, col=3, font=dict(size=10, weight="bold"))

        fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
        fig.update_layout(height=350, showlegend=False)

    elif topic == "Средняя линия треугольника":
        # Вершины треугольника: A(0,0), B(6,0), C(2,4)
        ax, ay = 0, 0
        bx, by = 6, 0
        cx, cy = 2, 4

        # 1. Основной треугольник ABC (Индиго)
        fig.add_trace(go.Scatter(
            x=[ax, bx, cx, ax], y=[ay, by, cy, ay], 
            mode='lines', line=dict(color='indigo', width=3),
            name="Δ ABC"
        ))

        # 2. СРЕДНЯЯ ЛИНИЯ MN
        # Точка M — середина AC: ((0+2)/2, (0+4)/2) = (1, 2)
        # Точка N — середина BC: ((6+2)/2, (0+4)/2) = (4, 2)
        mx, my = 1, 2
        nx, ny = 4, 2

        fig.add_trace(go.Scatter(
            x=[mx, nx], y=[my, ny], 
            mode='lines+markers', 
            line=dict(color='red', width=4),
            marker=dict(size=8, color='red'),
            name="Средняя линия"
        ))

        # --- Обозначение равенства отрезков на боковых сторонах ---
        # Сторона AC (M делит пополам) - по одной черте
        fig.add_annotation(x=0.5, y=1, text="/", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=1.5, y=3, text="/", showarrow=False, font=dict(size=14))
        # Сторона BC (N делит пополам) - по две черты
        fig.add_annotation(x=4, y=3, text="//", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=5, y=1, text="//", showarrow=False, font=dict(size=12))

        # --- Подписи вершин и линии ---
        fig.add_annotation(x=0.8, y=2.2, text="M", showarrow=False, font=dict(size=14, weight="bold"))
        fig.add_annotation(x=4.2, y=2.2, text="N", showarrow=False, font=dict(size=14, weight="bold"))
        fig.add_annotation(x=3, y=-0.5, text="Основание <b>a</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=2.5, y=2.3, text="<b>½ a</b>", showarrow=False, font=dict(color="red", size=14))

        # --- Текстовый блок справа ---
        fig.add_annotation(
            x=8, y=3.5, text="<b>Свойства средней линии:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=8, y=2.7, text="1. Соединяет середины двух сторон", 
            showarrow=False, xanchor="left", font=dict(size=13)
        )
        fig.add_annotation(
            x=8, y=2.0, text="2. MN || AB (параллельна основанию)", 
            showarrow=False, xanchor="left", font=dict(size=14, color="indigo")
        )
        fig.add_annotation(
            x=8, y=1.3, text="3. MN = ½ AB (в 2 раза меньше)", 
            showarrow=False, xanchor="left", font=dict(size=15, color="red", weight="bold")
        )
        fig.add_annotation(
            x=8, y=0.5, text="4. Отсекает треугольник,<br>подобный данному (k = 0.5)", 
            showarrow=False, xanchor="left", font=dict(size=12, color="gray")
        )

        fig.update_xaxes(range=[-1, 15], showgrid=False, zeroline=True)
        fig.update_yaxes(range=[-1, 5], showgrid=False)
        fig.update_layout(height=400, showlegend=False)

    elif topic == "Замечательные точки треугольника":
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=2, cols=2, 
                            subplot_titles=("Ортоцентр (Высоты)", "Медианы (Центроид)", 
                                            "Биссектрисы (Инцентр)", "Серединные перпендикуляры"),
                            horizontal_spacing=0.15, vertical_spacing=0.2)

        # Базовый треугольник: A(0,0), B(4,0), C(1,3)
        def add_base_tri(row, col):
            fig.add_trace(go.Scatter(x=[0, 4, 1, 0], y=[0, 0, 3, 0], 
                                     mode='lines', line=dict(color='black', width=2), showlegend=False), row=row, col=col)

        # --- 1. ОРТОЦЕНТР (H) ---
        add_base_tri(1, 1)
        # Высоты (упрощенно)
        fig.add_trace(go.Scatter(x=[1, 1, None, 0, 1.8, None, 4, 0.3], y=[3, 0, None, 0, 2.4, None, 0, 1], 
                                 mode='lines', line=dict(color='red', width=1, dash='dot'), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=[1], y=[0.75], mode='markers', marker=dict(color='red', size=8), name="H"), row=1, col=1)

        # --- 2. ЦЕНТРОИД (M) ---
        add_base_tri(1, 2)
        # Медианы (к серединам сторон)
        fig.add_trace(go.Scatter(x=[0, 2.5, None, 4, 0.5, None, 1, 2], y=[0, 1.5, None, 0, 1.5, None, 3, 0], 
                                 mode='lines', line=dict(color='blue', width=1, dash='dot'), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=[1.66], y=[1], mode='markers', marker=dict(color='blue', size=8), name="M"), row=1, col=2)

        # --- 3. ИНЦЕНТР (I) ---
        add_base_tri(2, 1)
        # Биссектрисы и вписанная окружность (схематично)
        fig.add_trace(go.Scatter(x=[0, 2.2, None, 4, 0.6, None, 1, 1.4], y=[0, 1.3, None, 0, 1.8, None, 3, 0], 
                                 mode='lines', line=dict(color='green', width=1, dash='dot'), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[1.2], y=[0.8], mode='markers', marker=dict(color='green', size=8), name="I"), row=2, col=1)

        # --- 4. ЦЕНТР ОПИСАННОЙ ОКРУЖНОСТИ (O) ---
        add_base_tri(2, 2)
        # Серединные перпендикуляры
        fig.add_trace(go.Scatter(x=[2, 2, None, 0.5, 2.5, None, 2.5, 0.5], y=[-0.5, 3, None, 1.5, 0.5, None, 1.5, 2.5], 
                                 mode='lines', line=dict(color='orange', width=1, dash='dot'), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[2], y=[0.83], mode='markers', marker=dict(color='orange', size=8), name="O"), row=2, col=2)

        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(height=600, margin=dict(t=50, b=20))

    elif topic == "Касательная к окружности":
        import numpy as np
        
        # 1. ОКРУЖНОСТЬ (Центр в 0,0, радиус R=3)
        theta = np.linspace(0, 2*np.pi, 100)
        r = 3
        cx = r * np.cos(theta)
        cy = r * np.sin(theta)
        
        fig.add_trace(go.Scatter(x=cx, y=cy, mode='lines', 
                                 line=dict(color='indigo', width=2), name="Окружность"))

        # 2. ТОЧКА КАСАНИЯ A (под углом 45 градусов)
        angle = np.pi / 4
        ax, ay = r * np.cos(angle), r * np.sin(angle)
        
        # Точка A
        fig.add_trace(go.Scatter(x=[ax], y=[ay], mode='markers+text', 
                                 text=["A"], textposition="top right",
                                 marker=dict(size=10, color='red'), name="Точка касания"))

        # 3. РАДИУС OA
        fig.add_trace(go.Scatter(x=[0, ax], y=[0, ay], mode='lines', 
                                 line=dict(color='red', width=2), name="Радиус R"))
        
        # Центр O
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', 
                                 text=["O"], textposition="bottom left",
                                 marker=dict(size=8, color='black'), showlegend=False))

        # 4. КАСАТЕЛЬНАЯ (Перпендикулярна OA)
        # Направление касательной (-sin, cos)
        tx = [-2, 5]
        # Уравнение касательной: x*cos(a) + y*sin(a) = r
        # Для визуализации проведем линию через A
        length = 4
        dx, dy = -np.sin(angle), np.cos(angle)
        line_x = [ax - dx*length, ax + dx*length]
        line_y = [ay - dy*length, ay + dy*length]
        
        fig.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', 
                                 line=dict(color='black', width=3), name="Касательная"))

        # 5. ЗНАЧОК ПРЯМОГО УГЛА
        # Маленький квадрат у точки A
        s = 0.3
        # Векторы для квадрата
        v1_x, v1_y = -np.cos(angle)*s, -np.sin(angle)*s
        v2_x, v2_y = -np.sin(angle)*s, np.cos(angle)*s
        
        fig.add_trace(go.Scatter(
            x=[ax+v1_x, ax+v1_x+v2_x, ax+v2_x], 
            y=[ay+v1_y, ay+v1_y+v2_y, ay+v2_y], 
            mode='lines', line=dict(color='red', width=1), showlegend=False))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=6, y=4, text="<b>Свойства касательной:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=6, y=3, text="1. Имеет с окружностью ровно<br>оду общую точку (A).", 
            showarrow=False, xanchor="left", font=dict(size=13)
        )
        fig.add_annotation(
            x=6, y=1.5, text="2. Радиус в точку касания<br>перпендикулярен ей (OA ⊥ l).", 
            showarrow=False, xanchor="left", font=dict(color="red", size=14, weight="bold")
        )
        fig.add_annotation(
            x=6, y=0, text="3. Расстояние от центра до прямой<br>равно радиусу (d = R).", 
            showarrow=False, xanchor="left", font=dict(size=13, color="gray")
        )

        fig.update_xaxes(range=[-4, 12], scaleanchor="y", scaleratio=1)
        fig.update_yaxes(range=[-4, 5])
        fig.update_layout(height=500, showlegend=False)

    elif topic == "Центральные и вписанные углы":
        import numpy as np
        
        # 1. ОКРУЖНОСТЬ (R=3, Центр 0,0)
        theta = np.linspace(0, 2*np.pi, 100)
        r = 3
        fig.add_trace(go.Scatter(x=r*np.cos(theta), y=r*np.sin(theta), 
                                 mode='lines', line=dict(color='lightgray', width=2), name="Окружность"))

        # 2. ТОЧКИ НА ОКРУЖНОСТИ
        # Дуга AB (основание углов)
        ang_a, ang_b = -np.pi/4, np.pi/4 # -45° и 45°
        ang_c = 5*np.pi/6 # 150° (точка на окружности для вписанного угла)
        
        ax, ay = r*np.cos(ang_a), r*np.sin(ang_a)
        bx, by = r*np.cos(ang_b), r*np.sin(ang_b)
        cx, cy = r*np.cos(ang_c), r*np.sin(ang_c)
        ox, oy = 0, 0

        # 3. ЦЕНТРАЛЬНЫЙ УГОЛ AOB (Синий)
        fig.add_trace(go.Scatter(x=[ax, ox, bx], y=[ay, oy, by], 
                                 mode='lines+markers', line=dict(color='blue', width=3), name="Центральный"))
        
        # 4. ВПИСАННЫЙ УГОЛ ACB (Красный)
        fig.add_trace(go.Scatter(x=[ax, cx, bx], y=[ay, cy, by], 
                                 mode='lines+markers', line=dict(color='crimson', width=3, dash='dash'), name="Вписанный"))

        # --- Подписи точек ---
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ox], y=[ay, by, cy, oy], mode='text',
                                 text=["A", "B", "C", "O"], textposition=["bottom right", "top right", "top left", "bottom left"],
                                 showlegend=False))

        # --- Текстовое описание справа ---
        fig.add_annotation(
            x=5, y=3.5, text="<b>Свойства углов:</b>", 
            showarrow=False, xanchor="left", font=dict(size=16)
        )
        fig.add_annotation(
            x=5, y=2.5, text="1. Центральный угол (∠AOB)<br>равен градусной мере дуги AB.", 
            showarrow=False, xanchor="left", font=dict(color="blue", size=13)
        )
        fig.add_annotation(
            x=5, y=1.2, text="2. Вписанный угол (∠ACB)<br>равен половине центрального,<br>опирающегося на ту же дугу.", 
            showarrow=False, xanchor="left", font=dict(color="crimson", size=14, weight="bold")
        )
        fig.add_annotation(
            x=5, y=0, text="<b>∠ACB = ½ ∠AOB</b>", 
            showarrow=False, xanchor="left", font=dict(size=18, color="black")
        )

        fig.update_xaxes(range=[-4, 12], scaleanchor="y", scaleratio=1)
        fig.update_yaxes(range=[-4, 4])
        fig.update_layout(height=450, showlegend=False)

    elif topic == "Вписанная и описанная окружности":
        from plotly.subplots import make_subplots
        import numpy as np
        
        fig = make_subplots(rows=1, cols=2, 
                            subplot_titles=("Вписанная (Центр — биссектрисы)", "Описанная (Центр — сер. перпендикуляры)"),
                            horizontal_spacing=0.15)

        # Координаты треугольника ABC: A(0,0), B(4,0), C(1,3)
        ax, ay = 0, 0
        bx, by = 4, 0
        cx, cy = 1, 3
        tri_x, tri_y = [ax, bx, cx, ax], [ay, by, cy, ay]

        # --- 1. ВПИСАННАЯ ОКРУЖНОСТЬ ---
        # Расчет инцентра (I) и радиуса (r) для этого треугольника
        # a=BC=sqrt(3^2+3^2)=4.24, b=AC=sqrt(1^2+3^2)=3.16, c=AB=4
        in_x, in_y, in_r = 1.35, 0.82, 0.82 # Приблизительные значения для наглядности
        
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ax], y=[ay, by, cy, ay], mode='lines', line=dict(color='black', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=in_x + in_r*np.cos(theta), y=in_y + in_r*np.sin(theta), 
                                 mode='lines', line=dict(color='crimson', width=2), name="Вписанная"), row=1, col=1)
        fig.add_trace(go.Scatter(x=[in_x], y=[in_y], mode='markers', marker=dict(color='crimson', size=6), name="Инцентр"), row=1, col=1)

        # --- 2. ОПИСАННАЯ ОКРУЖНОСТЬ ---
        # Расчет центра (O) и радиуса (R)
        out_x, out_y, out_r = 2.0, 0.83, 2.17
        
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ax], y=[ay, by, cy, ay], mode='lines', line=dict(color='black', width=2)), row=1, col=2)
        fig.add_trace(go.Scatter(x=out_x + out_r*np.cos(theta), y=out_y + out_r*np.sin(theta), 
                                 mode='lines', line=dict(color='blue', width=2), name="Описанная"), row=1, col=2)
        fig.add_trace(go.Scatter(x=[out_x], y=[out_y], mode='markers', marker=dict(color='blue', size=6), name="Центр"), row=1, col=2)

        # Настройка осей (важно сохранить пропорции круга)
        fig.update_xaxes(range=[-1, 5], scaleanchor="y", scaleratio=1, showticklabels=False, showgrid=False)
        fig.update_yaxes(range=[-1, 4], showticklabels=False, showgrid=False)
        fig.update_layout(height=400, showlegend=False)
    
    else:
        # Заглушка для тем без специфической графики
        fig.add_annotation(x=2, y=2, text="Визуализация в процессе разработки", showarrow=False, font=dict(size=14, color="gray"))

    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_tree():
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

app.layout = dmc.MantineProvider(
    children=dmc.Container([
        dmc.Grid([
            dmc.GridCol([
                dmc.Paper([
                    dmc.Title("Геометрия 7-9", order=2, mb="md", ta="center"),
                    dmc.Accordion(variant="contained", children=create_tree()),
                ], p="md", withBorder=True, radius="md", shadow="sm")
            ], span=5),
            
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
                    # Скрытый div для принудительного рендеринга MathJax
                    html.Div(id="mathjax-trigger", style={"display": "none"})
                ], withBorder=True, p="xl", radius="md", shadow="md", style={"backgroundColor": "#fafafa"})
            ], span=7)
        ], gutter="xl")
    ], size="lg", mt="xl")
)

@app.callback(
    Output("material-content", "children"),
    Input({"type": "topic-link", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def display_material(n_clicks):
    triggered = ctx.triggered_id
    if not triggered or not any(n_clicks):
        return dash.no_update
    
    topic_name = triggered['index']
    content = materials_db.get(topic_name, "Материал скоро появится.")
    
    return html.Div([
        dmc.Title(topic_name, order=4, mb="xs", c="indigo"),
        dmc.Text(content, size="lg", mb="xl", style={"lineHeight": "1.6"}),
        dmc.Divider(label="Интерактивная модель", labelPosition="center", mb="md"),
        get_plot(topic_name),
        # Костыль для MathJax: скрипт сработает при вставке в DOM
        html.Script("if(window.MathJax){MathJax.Hub.Queue(['Typeset', MathJax.Hub]);}")
    ])

# Для Render нужно указать server
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
