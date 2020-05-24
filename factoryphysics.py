import plotly.graph_objects as go
import pandas as pd
import numpy as np


class ProductionLine:
    """A class used to represent a production line.
    
    Methods can be called to describe the 
    characteristics of the production line using
    Factory Physics laws and definitions.
    
    Parameters
    ----------
    r_b : number
        The bottleneck rate. It is the rate of the 
        workstation having the highest long-term utilization. 
        Uses units of parts per unit time.
    T_0 : number
        The natural process time. It is the sum of the 
        long-term average process times of each workstation in 
        the line. Uses units of time.
    """
    
    def __init__(self, r_b, T_0, name=None):
        self.r_b = r_b
        self.T_0 = T_0
        self.W_0 = r_b * T_0
        self._name = name

    @property
    def name(self):
        return self._name

    def CT_best(self, w):
        """Returns the minimum cycle time for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a perfect line with no variability.

        Factory Physics 3e, p.241
        
        Parameters
        ----------
        
        """
        if w <= self.W_0:
            return self.T_0
        else:
            return w / self.r_b


    def TH_best(self, w):
        """Returns the maximum throughput for a given WIP level w.
        
        Describes the relationship between WIP and cycle time
        for a perfect line with no variability.
        
        Factory Physics 3e, p.241
        """
        
        if w <= self.W_0:
            return w / self.T_0
        else:
            return self.r_b


    # Law (Worst-Case Performance) p.243
    def CT_worst(self, w):
        """Returns the worst-case cycle time for a given WIP level w.
        
        Describes the relationship between WIP and cycle time
        for a line with maximum variability.
        
        Factory Physics 3e, p.243
        """
        
        return w * self.T_0


    def TH_worst(self):
        """Returns the worst-case throughput for a given WIP level w.
        
        Describes the relationship between WIP and cycle time
        for a line with maximum variability.
        
        Factory Physics 3e, p.243
        """
        
        return 1 / self.T_0


    # Definition (Practical Worst-Case Performance) p.247
    def CT_PWC(self, w):
        """Returns the practical worst-case cycle time for a given WIP level w.
        
        Describes the relationship between WIP and cycle time
        for a line with "maximum randomness".
        
        Factory Physics 3e, p.247
        """
        
        return self.T_0 + (w - 1) / self.r_b


    def TH_PWC(self, w):
        """Returns the practical worst-case throughput for a given WIP level w.
        
        Describes the relationship between WIP and cycle time
        for a line with "maximum randomness".
        
        Factory Physics 3e, p.247
        """
        
        return  (w / (self.W_0 + w - 1)) * self.r_b


def df_scenarios(ProductionLine,max_wip):
    """Creates a DataFrame of the best case, worst case, and practical worst case 
    of throughput and cycle time for the ProductionLine object provided.
    """
    df = pd.DataFrame(index=np.arange(1,max_wip+1)) # +1 is to include the WIP level entered.
    df['WIP'] = df.index
    df['TH Best Case'] = df['WIP'].apply(ProductionLine.TH_best)
    df['TH Worst Case'] = ProductionLine.TH_worst()
    df['TH Practical Worst Case'] = df['WIP'].apply(ProductionLine.TH_PWC)
    df['CT Best Case'] = df['WIP'].apply(ProductionLine.CT_best)
    df['CT Worst Case'] = df['WIP'].apply(ProductionLine.CT_worst)
    df['CT Practical Worst Case'] = df['WIP'].apply(ProductionLine.CT_PWC)
    return df

def plot_scenarios(ProductionLine,max_wip):
    df = df_scenarios(ProductionLine,max_wip)
    fig = go.Figure()
    
    # Horizontal line for r_b
    fig.add_shape(type="line",x0=0,y0=ProductionLine.r_b,x1=df['WIP'].max(),y1=ProductionLine.r_b,line=dict(color="black",width=1,dash="dash",))

    # Horizontal line for T_0
    fig.add_shape(type="line",x0=0,y0=1/ProductionLine.T_0,x1=df['WIP'].max(),y1=1/ProductionLine.T_0,line=dict(color="black",width=1,dash="dash",))

    # Create and style traces
    fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Practical Worst Case'], name='Practical Worst Case'))
    fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Worst Case'], name='Worst Case'))
    fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Best Case'], name = 'Best Case'))

    # Set axes ranges
    fig.update_xaxes(range=[0, df['WIP'].max()])
    fig.update_yaxes(range=[0, 0.5])

    # Edit the layout
    fig.update_layout(title=f'Throughput Time vs WIP for {ProductionLine._name}',
                    xaxis_title='WIP',
                    yaxis_title='Throughput (parts/unit time)')

    fig.update_layout(
        showlegend=True,
        annotations=[
            dict(
                x=2.5,
                y=ProductionLine.r_b,
                xref="x",
                yref="y",
                text="Bottleneck Rate (r_b)",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40)])

    return fig.show()