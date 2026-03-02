import plotly.graph_objects as go

def risk_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "System Risk Level"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0,30], 'color': "green"},
                {'range': [30,60], 'color': "yellow"},
                {'range': [60,85], 'color': "orange"},
                {'range': [85,100], 'color': "red"},
            ],
        }
    ))

    fig.update_layout(height=350)

    return fig